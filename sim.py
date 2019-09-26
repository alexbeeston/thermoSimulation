import sys

########################
### HELPER FUNCTIONS ###
########################
def calcWeightedAverage(mass1, temp1, mass2, temp2):
    return (mass1 * temp1 + mass2 * temp2) / (mass1 + mass2)

def addHeat(oldTemp, heat, specificHeat, mass):
    return oldTemp + heat / (mass * specificHeat)

def buildRowString(vals):
    row = ""
    for j in range(len(vals)):
        row += str(vals[j])
        if j != len(vals) - 1:
            row += ","
    row += "\n"
    return row

###################
### ENTRY POINT ###
###################
# Define Thermodynamic Constants
specificHeatWater = 4.184 # kJ/(kg * C)
densityWater = 1000 # kg/m^3

# Parse Parameters File
parameterFile = open("parameters.txt", "r")
p = {}
for line in parameterFile:
    words = line.strip().split(",")
    p[words[0]] = words[1]
parameterFile.close()
stepSize = float(p["step size (sec)"])
heatInRate = float(p["heat in (kWatts)"])
heatOutRate = float(p["heat out (kWatts)"])
massFlow = float(p["mass flow rate (kg/sec)"])
hotTemp = float(p["initial hot temp (C)"])
coldTemp = float(p["initial cold temp (C)"])
heaterVolume = float(p["heating element volume (m^3)"])
tankVolume = float(p["storage tank volume (m^3)"])
duration = float(p["run time (sec)"])
convergenceCriteria = float(p["converge criteria (unitless)"])
stopOnConverge_int = int(p["stop on convergence (0=false 1=true)"])
stopOnConverge = False
if stopOnConverge_int == 1:
    stopOnConverge = True

# Validate Parameters
for pair in p.items():
    if float(pair[1]) < 0:
        print("Parameter Error: \"" + pair[0] + "\" must be greater than zero.")
        sys.exit()
if not (stopOnConverge_int == 0 or stopOnConverge_int == 1):
    print("Parameter error: \"stop on convergence (0=false 1=true)\" must be set to either 0 or 1")
    sys.exit()
if stepSize * massFlow > densityWater * heaterVolume:
    print("Parameter error: The step size is too large for the size of the heater.\nThe following comparison must hold: (stepSize * massFlowRate) < (densityWater * heaterElementVolume).")
    print("Do at least one of the following:\n1) Decrease step size\n2) decrease mass flow rate\n3) increase volume of heating element")
    sys.exit()
if stepSize * massFlow > densityWater * tankVolume:
    print("Parameter error: The step size is too large for the size of the tank.\nThe following comparison must hold: (stepSize * massFlowRate) < (densityWater * storageTankVolume).")
    print("Do at least one of the following:\n1) Decrease step size\n2) decrease mass flow rate\n3) increase volume of storage tank")
    sys.exit()
if stepSize > duration:
    print("Parameter error: The step size is larger than the run time. The step size must be smaller than the runn time of the simulation")
    sys.exit()
if hotTemp > 100:
    print("Parameter error: The initial hot temp is larger than 100 degrees celsius. Enter a value in the range (0, 100)")
    sys.exit()
if coldTemp > 100:
    print("Parameter error: The initial cold temp is larger than 100 degrees celsius. Enter a value in the range (0, 100)")
    sys.exit()


'''

overheating tank throughout the simulation

'''

# Generate Run-Time Parameters
fidelity = stepSize * massFlow # kg
iterations = duration * massFlow / fidelity # unitless
heaterMass = heaterVolume * densityWater # kg
tankMass = tankVolume * densityWater #kg
print("heater mass" + str(heaterMass))
print("fidelity: " + str(fidelity))

# Define Variables for Determine Convergence
hotTemp_previous  = 10
coldTemp_previous = 10
hotTemp_converge = -1
coldTemp_converge = -1
hotTemp_converge_flag = False
coldTemp_converge_flag = False

# Open Data Output File
logFileName = "data.csv"
if len(sys.argv) > 2:
    print("Usage Error: sim.py [outPutFileName]")
    sys.exit()
elif len(sys.argv) == 2:
    logFileName = sys.argv[1]
log = open(logFileName, "w")
headers = "Iteration,Time Stamp (sec),Hot Temperature (Cel),Cold Temperature (Cel)\n"
log.write(headers)
log.write("0,0," + str(hotTemp) + "," + str(coldTemp) + "\n")

# Run Simulation
for i in range(int(iterations)):
    # step 1 of simulation: mix cold water into the heater
    hotTemp = calcWeightedAverage(fidelity, coldTemp, heaterMass - fidelity, hotTemp)

    # step 2 of simulation: add heat to water in the heater
    hotTemp = addHeat(hotTemp, heatInRate * stepSize, specificHeatWater, heaterMass)

    # step 3 of simulation: mix hot water into the tank
    coldTemp = calcWeightedAverage(fidelity, hotTemp, tankMass - fidelity, coldTemp)

    # step 4 of simulation: remove heat from water in the tank
    coldTemp = addHeat(coldTemp, -(heatOutRate * stepSize), specificHeatWater, tankMass)

    # build report
    row = buildRowString([i + 1, (i + 1) * stepSize, hotTemp, coldTemp])
    log.write(row)


    if abs(hotTemp_previous - hotTemp) < convergenceCriteria and not hotTemp_converge_flag:
        hotTemp_converge = i
        hotTemp_converge_flag = True
    else:
        hotTemp_previous = hotTemp

    if abs(coldTemp_previous - coldTemp) < convergenceCriteria and not coldTemp_converge_flag:
        coldTemp_converge = i
        coldTemp_converge_flag = True
    else:
        coldTemp_previous = coldTemp

log.close()



print("For step size = " + str(stepSize) + " (used " + str(iterations) + " iterations).")
print("Final hotTemp: " + str(hotTemp))
print("Final coldTemp: " + str(coldTemp))
if hotTemp_converge_flag:
    print("hotTemp converged after " + str(hotTemp_converge + 1) + " iterations, which maps to " + str(hotTemp_converge * stepSize) + " seconds of run time.")
else:
    print("hotTemp did not converge. Final difference: " + str(abs(hotTemp_previous - hotTemp)))

if coldTemp_converge_flag:
    print("coldTemp converged after " + str(coldTemp_converge + 1) + " iterations, which maps to " + str(coldTemp_converge * stepSize) + " seconds of run time.")
else:
    print("coldTemp did not converge. Final difference: " + str(abs(coldTemp_previous - coldTemp)))

