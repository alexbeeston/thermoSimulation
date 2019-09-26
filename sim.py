import sys



# for numerical methods stuff
hotTemp_previous  = 10
coldTemp_previous = 10
hotTemp_converge = -1
coldTemp_converge = -1
hotTemp_converge_flag = False
coldTemp_converge_flag = False




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

stepSize = float(p["step size"]) # sec
heatIn = float(p["heat in"]) # kWatts
heatOut = float(p["heat out"]) #kWatts
massFlow = float(p["mass flow rate"]) # kg / sec
hotTemp = float(p["initial hot temp"]) # Celsius (initial temperature of hot water)
coldTemp = float(p["initial cold temp"]) # Celsius (initial temperature of cold water)
heaterVolume = float(p["heating element volume"])# m^3
tankVolume = float(p["storage tank volume"]) # m^3
duration = float(p["run time"]) # sec
convergenceCriteria = float(p["converge criteria"]) # unit less

# Generate Run-Time Parameters
fidelity = stepSize * massFlow # kg
iterations = duration * massFlow / fidelity # unitless
heaterMass = heaterVolume * densityWater # kg
tankMass = tankVolume * densityWater #kg

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
    # print("Iteration " + str(i) + ":")
    # step 1: mix water from pipe with water in heater
    hotTemp = (fidelity * coldTemp + (heaterMass - fidelity) * hotTemp) / heaterMass # a weighted average, see appendix 1 for derivation, equation 1, whatever

    # step 2: add heat to ALL  water in heater
    addedHeat = heatIn * stepSize
    hotTemp = hotTemp + addedHeat / (heaterMass * specificHeatWater)
    #print("   hotTemp: " + str(hotTemp))

    # step 3: add warm water to tank
    coldTemp = (fidelity * hotTemp + (tankMass - fidelity) * coldTemp) / tankMass

    # step 4: remove heat from ALL water in tank
    addedHeat = heatOut * stepSize
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
