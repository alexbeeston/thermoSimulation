import sys

stepSize = 1 # sec
heatRate = 1000 # kWatts - separate into two
massFlow = 5 # kg / sec
temp1 = 20 # Celsius (initial temperature of hot water)
temp2 = 12 # Celsius (initial temperature of cold water)
massSolar = 25 # kg
massTank = 750 # kg
specificHeat = 4.184 # kJ/(kg * C)
duration = 5000 # sec
convergeCriteria = .001 # unit less

# for numerical methods stuff
temp1_previous  = 10
temp2_previous = 10
temp1_converge = -1
temp2_converge = -1
temp1_converge_flag = False
temp2_converge_flag = False

# BEGIN
fidelity = stepSize * massFlow # kg
iterations = duration * massFlow / fidelity # unit less
log = open("log.txt", "w")
headers = "iteration,timeStamp,Q_in,temp_1,Q_out,temp_2"
for i in range(int(iterations)):
    # print("Iteration " + str(i) + ":")
    # step 1: mix water from pipe with water in heater
    temp1 = (fidelity * temp2 + (massSolar - fidelity) * temp1) / massSolar # a weighted average, see appendix 1 for derivation, equation 1, whatever

    # step 2: add heat to ALL  water in heater
    addedHeat = heatRate * stepSize
    temp1 = temp1 + addedHeat / (massSolar * specificHeat)
    #print("   temp1: " + str(temp1))

    # step 3: add warm water to tank
    temp2 = (fidelity * temp1 + (massTank - fidelity) * temp2) / massTank

    # step 4: remove heat from ALL water in tank
    addedHeat = -heatRate * stepSize
    temp2 = temp2 + addedHeat / (massTank * specificHeat)

    # report


    if abs(temp1_previous - temp1) < convergeCriteria and not temp1_converge_flag:
        temp1_converge = i
        temp1_converge_flag = True
    else:
        temp1_previous = temp1

    if abs(temp2_previous - temp2) < convergeCriteria and not temp2_converge_flag:
        temp2_converge = i
        temp2_converge_flag = True
    else:
        temp2_previous = temp2

print("For step size = " + str(stepSize) + " (used " + str(iterations) + " iterations).")
print("Final temp1: " + str(temp1))
print("Final temp2: " + str(temp2))
if temp1_converge_flag:
    print("temp1 converged after " + str(temp1_converge + 1) + " iterations, which maps to " + str(temp1_converge * stepSize) + " seconds of run time.")
else:
    print("temp1 did not converge. Final difference: " + str(abs(temp1_previous - temp1)))

if temp2_converge_flag:
    print("temp2 converged after " + str(temp2_converge + 1) + " iterations, which maps to " + str(temp2_converge * stepSize) + " seconds of run time.")
else:
    print("temp2 did not converge. Final difference: " + str(abs(temp2_previous - temp2)))
log.close()

'''
BUG:
- monitor the fidelity does not divide the mass flow rate

'''