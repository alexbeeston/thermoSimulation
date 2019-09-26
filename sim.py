import sys

#################################
### EXTENSIBLE HELP FUNCTIONS ###
#################################
def calcHeatInRate(heatInRate):
    return heatInRate
def calcRemovedHeat(heatOutRate):
    return -heatOutRate
def calcWeightedAverage(mass1, temp1, mass2, temp2):
    return (mass1 * temp1 + mass2 * temp2) / (mass1 + mass2)

###################
### ENTRY POINT ###
###################

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

# Define Thermodynamic Constants
specificHeatWater = 4.184 # kJ/(kg * C)
densityWater = 1000 # kg/m^3

# Generate Run-Time Parameters
fidelity = stepSize * massFlow # kg
iterations = duration * massFlow / fidelity # unitless
heaterMass = heaterVolume * densityWater # kg
tankMass = tankVolume * densityWater #kg

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
headers = "iteration,timeStamp,Q_in,temp_1,Q_out,temp_2"
log.write(headers)

# Run Simulation
for i in range(int(iterations)):
    row = [str(i), str(i * stepSize)]
    # step 1: mix water from pipe with water in heater.
    hotTemp = calcWeightedAverage(fidelity, coldTemp, heaterMass - fidelity, hotTemp)

    # step 2: add heat to ALL  water in heater
    addedHeat = calcHeatInRate(heatInRate) * stepSize
    hotTemp = hotTemp + addedHeat / (heaterMass * specificHeatWater)

    # step 3: add warm water to tank
    coldTemp = calcWeightedAverage(fidelity, hotTemp, tankMass - fidelity, coldTemp)

    # step 4: remove heat from ALL water in tank
    addedHeat = -heatOutRate * stepSize
    coldTemp = coldTemp + addedHeat / (tankMass * specificHeatWater)

    # report


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