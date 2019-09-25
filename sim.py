import sys

# here we go
basis = 5 # kg of water
solarRate = 50 # kWatts
dischargeRate = -50 # kWatts
massFlow = 10 # kg / sec
temp1 = 10 # Celsius (initial temperature of hot water)
temp2 = 10 # Celsius (initial temperature of cold water)
massSolar = 20 # kg
massTank = 500 # kg
specificHeat = 4.184 # kJ/(kg * K)
duration = 10 # second

# BEGIN

for i in range(int(iterations)):  # convert to while loop later that checks for stopping criteria
    print("Iteration " + str(i) + ":")
    # step 1: heat "basis" water from solar panel
    temp1 = temp2 + (solarRate * basis) / ((massFlow*basis) * specificHeat)  # equation 1
    print("   T1 = " + str(temp1))

    # step 2: mix with the water in the first pipe


    # step 3:
    # step 2: mix water from heated pipe to tank
    massOfWaterEnteringTank = massFlow * basis
    massMix = massTank - massOfWaterEnteringTank
    temp2 = (massOfWaterEnteringTank*temp1 + massMix*temp2) / (massMix + massOfWaterEnteringTank) # equation 2
    print("   T2 = " + str(temp2))

    # step 3: discharge heat
    temp2 = temp2 + (dischargeRate * basis) / ((massFlow*basis) * specificHeat)  # equation 3
    print("   T2 = " + str(temp2))

print("For " + str(duration) + " seconds at a frequency of " + str(basis) + " htz.")








def logValues():
    pass
