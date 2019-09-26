import sys
import matplotlib.pyplot as plt

########################
### HELPER FUNCTIONS ###
########################
def getdataFileName():
    logFileName = "data.csv"
    if len(sys.argv) > 2:
        print("Usage Error: sim.py [outPutFileName]")
        sys.exit()
    elif len(sys.argv) == 2:
        logFileName = sys.argv[1]
    return logFileName
    
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

def checkTempExtremes(max, min, temp, stepSize, iteration, portion):
    if temp > max:
        print("Error: The system overheated in the " + portion + " region on iteration " + str(iteration) + ", which maps to time = " + str(stepSize * iteration) + " seconds.")
        print("The temperature in the " + str(portion) + " region was " + str(temp) + " degrees celsius, and the maximum permissible temperature was " + str(max) + ".")
        return False
    elif temp < min:
        print("Error: The system temperature fell beneath the minimum permissible temperature in the " + portion + " region on iteration " + str(iteration) + ", which maps to time = " + str(stepSize * iteration) + " seconds.")
        print("The temperature in the " + str(portion) + " region was " + str(temp) + " degrees celsius, and the minimum permissible temperature was " + str(min) + ".")
        return False
    else:
        return True

def graphResults(times, hotTemperatures, coldTemperatures):
    try:
        plt.plot(times, hotTemperatures, label='Hot Temperatures', color='red')
        plt.plot(times, coldTemperatures, label='Cold Temperatures', color='blue')
        plt.xlabel("Time (minutes)")
        plt.ylabel("Temperature (deg celsius)")
        plt.title("Thermodynamic Simulation")
        plt.legend(loc='best')
        plt.show()
    except:
        print(
            "The graph of the data could not be generated. Try running the command \"pip install matplotlib\" to install the necessary modules")

def openDataFile():
    dataFile = open(getdataFileName(), "w")
    headers = "Iteration,Time Stamp (sec),Hot Temperature (Cel),Cold Temperature (Cel)\n"
    dataFile.write(headers)
    dataFile.write("0,0," + str(hotTemp) + "," + str(coldTemp) + "\n")
    return dataFile

def validate(stepSize, massFlow, hotTemp, coldTemp, heaterVolume, tankVolume, duration, maxTemp, minTemp, p):
    for pair in p.items():
        if float(pair[1]) < 0:
            print("Parameter Error: \"" + pair[0] + "\" must be greater than zero.")
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
    if maxTemp > 100:
        print("Parameter error: The maximum permissible temperature is greater than 100 degrees celsius. This simulation only support liquid fluids.")
        sys.exit()
    if maxTemp < minTemp:
        print("Parameter error: The maximum permissible temperature is less than the minimum permissible temperature")
        sys.exit()

def printResults(iterations, hotTemp_previous, hotConvergeIteration, coldTemp_previous, coldConvergeIteration, stepSize, p):
    print("System Configurations:")
    print("   Simulated run time: " + str(duration / 60) + " min")
    print("   Step Size: " + p["step size (sec)"] + " sec")
    print("   Heat input: " + p["heat in (kWatts)"] + " kW")
    print("   Heat output: " + p["heat out (kWatts)"] + " kW")
    print("   Mass flow rate: " + p["mass flow rate (kg/sec)"] + " kg/sec")
    print("   Initial hot temperature: " + p["initial hot temp (cel)"] + " deg C")
    print("   Initial cold temperature: " + p["initial cold temp (cel)"] + " deg C")
    print("   Volume of heating element: " + p["heating element volume (m^3)"] + " m^3")
    print("   Volume of storage tank: " + p["storage tank volume (m^3)"] + " m^3")
    print("   Convergence criteria used: " + p["converge criteria (unitless)"])
    print("   Maximum permissible temperature: " + p["maximum permissible temperature (cel)"] + " deg C")
    print("   Minimum permissible termperature: " + p["minimum permissible temperature (cel)"] + " deg C")
    if hotConvergeIteration < iterations:
        print("The warm region converged to a temperature of " + str(hotTemp_previous) + " on iteration " + str(hotConvergeIteration) + ", which maps to " + str(hotConvergeIteration * stepSize / 60) + " minutes of simulation time.")
    else:
        print("The warm region did not converge. The final temperature was " + str(hotTemp_previous) + " degrees celsius.")
    if coldConvergeIteration < iterations:
        print("The cool region converged to a temperature of " + str(coldTemp_previous) + " on iteration " + str(coldConvergeIteration) + ", which maps to " + str(coldConvergeIteration * stepSize / 60) + " minutes of simulation time.")
    else:
        print("The cool region did not converge. The final temperature was " + str(coldTemp_previous) + " degrees celsius.")
    print("See the file " + getdataFileName() + " for a complete report of the temperatures.")

###################
### ENTRY POINT ###
###################

# define thermodynamic constants
specificHeatWater = 4.184 # kJ/(kg * C)
densityWater = 1000 # kg/m^3

# parse parameter file
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
hotTemp = float(p["initial hot temp (cel)"])
coldTemp = float(p["initial cold temp (cel)"])
heaterVolume = float(p["heating element volume (m^3)"])
tankVolume = float(p["storage tank volume (m^3)"])
duration = float(p["run time (min)"]) * 60
convergenceCriteria = float(p["converge criteria (unitless)"])
maxTemp = float(p["maximum permissible temperature (cel)"])
minTemp = float(p["minimum permissible temperature (cel)"])
validate(stepSize, massFlow, hotTemp, coldTemp, heaterVolume, tankVolume, duration, maxTemp, minTemp, p)

# generate run-time parameters
fidelity = stepSize * massFlow # kg
iterations = duration * massFlow / fidelity # unitless
heaterMass = heaterVolume * densityWater # kg
tankMass = tankVolume * densityWater #kg

# define variables used for determining convergence
hotTemp_previous  = hotTemp
coldTemp_previous = hotTemp
hotConvergeIteration = -1
coldConvergeIteration = -1
hotFlag = False
coldFlag = False

# initialize simulation data, flow control variables, and open log file
times = [0]
hotTemperatures = [hotTemp]
coldTemperatures = [coldTemp]
i = 0
keepGoing = True
dataFile = openDataFile()

# Run Simulation
while i < int(iterations) and keepGoing:
    # step 1 of simulation: mix cold water into the heater
    hotTemp = calcWeightedAverage(fidelity, coldTemp, heaterMass - fidelity, hotTemp)
    keepGoing = checkTempExtremes(maxTemp, minTemp, hotTemp, stepSize, i + 1, "warm")

    # step 2 of simulation: add heat to water in the heater
    if keepGoing:
        hotTemp = addHeat(hotTemp, heatInRate * stepSize, specificHeatWater, heaterMass)
        keepGoing = checkTempExtremes(maxTemp, minTemp, hotTemp, stepSize, i + 1, "warm")

    # step 3 of simulation: mix hot water into the tank
    if keepGoing:
        coldTemp = calcWeightedAverage(fidelity, hotTemp, tankMass - fidelity, coldTemp)
        keepGoing = checkTempExtremes(maxTemp, minTemp, hotTemp, stepSize, i + 1, "cool")

    # step 4 of simulation: remove heat from water in the tank
    if keepGoing:
        coldTemp = addHeat(coldTemp, -(heatOutRate * stepSize), specificHeatWater, tankMass)
        keepGoing = checkTempExtremes(maxTemp, minTemp, hotTemp, stepSize, i + 1, "cool")

    # log data
    row = buildRowString([i + 1, (i + 1) * stepSize, hotTemp, coldTemp])
    dataFile.write(row)
    times.append(((i + 1) * stepSize) / 60)
    hotTemperatures.append(hotTemp)
    coldTemperatures.append(coldTemp)

    # check for convergence
    if abs(hotTemp_previous - hotTemp) < convergenceCriteria and not hotFlag:
        hotFlag = True
        hotConvergeIteration = i
    elif not hotFlag:
        hotTemp_previous = hotTemp
    if abs(coldTemp_previous - coldTemp) < convergenceCriteria and not coldFlag:
        coldFlag = True
        coldConvergeIteration = i
    elif not coldFlag:
        coldTemp_previous = coldTemp
    i += 1

# log and visualize data
dataFile.close()
printResults(iterations, hotTemp_previous, hotConvergeIteration, coldTemp_previous, coldConvergeIteration, stepSize, p)
graphResults(times, hotTemperatures, coldTemperatures)