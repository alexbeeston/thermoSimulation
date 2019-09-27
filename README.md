# Heat Exchanger Simulation

## Overview
This program simulates a simple heat exchanger by calculating the temperature of water after absorbing heat in a small heater and then again after giving up heat in a large storage tank. The input parameters are configured in the file "configs.txt", and the output is written to a .csv file named "data.csv" or as specified as a command line argument. 

## Run Instructions
To properly use this program, do the following:
- Install Python version 3.7 or greater.
- Install the python package matplotlib with the command "pip install matplotlib". This allows the user to visualize the results of the computation on a line chart.
- Configure the program to meet your needs by modifying the file "configs.txt". See section <i>Input</I> for more information on system configuration.
- Run the program with 0 or 1 command line arguments; with 0 arguments, the name of the output data file will default to "data.csv". With 1 argument, the data file will be named the value of the argument.
- Observe the summary of the computation printed on the command line along with the generated graphic.
- Close the program completely by exiting the graphic window.
- Do what you will with the .csv data file.

## Input
All parameters to the system are configured in the file "configs.txt". The following is an explanation of each parameter:
- step size (sec): the interval in seconds over which the calculations are made
- heat in (kW) : the rate in kilowatts at which heat enters the system from the heating element. This value is seen from the perspective of the system, so only a positive value should be used.
- heat out (k@) : the rate in kilowatts at which heat leaves the system from the storage tank. This value is seen from the perspective of the surroundings, so only positive value should be used.
- mass flow rate (kg/sec) : the rate in kilograms per second at which the fluid (water) circulates through the system
- initial warm temp (cel) : the initial temperature in celsius of the water directly after it leaves the heating element
- initial cool temp (cel) : the initial temperature in celsius of the water directly after it leaves the storage tank. The cool initial temperature is not necessarily smaller than the warm initial temperature. In fact, some interesting results are shown when the initial cool temperature is greater than the initial warm temperature, as in the configurations in "sample1.txt".
- heating element volume (m^3): the volume in cubic meters of the heating element
- storage tank volume (m^3) : the volume in cubic meters of the storage tank. The volume of the storage tank is not necessarily larger than the volume of the heating element. 
- run time (min) : the running time in minutes modeled by the program
- converge criteria (unitless) : the value at which convergence for the system is determined. Convergence is defined as the difference between the current value of the warm or cool stream and the previous value of the warm or cool stream, respectively. A system with the same rate of heat input and output will eventually converge on temperatures for the warm and cool streams.
- maximum permissible temperature (cel) : the maximum allowable temperature in celsius at which the system can operate. An error is thrown if this value exceeds 100, since the system is designed to only allow for liquid water.
- minimum permissible temperature (cel) : the minimum allowable temperature in celsius at which the system can operate. An error is thrown if this value is less than 0, since frozen water cannot flow through pipes. An error is also thrown if this value is greater than the maximum permissible temperature.

All values are validated before the computation runs, and if the program detects invalid values, an error message with instructions for correcting the bad value is provided. The default configuration file "configs.txt" provides a suggest set of configurations. Two other configuration files names "sample1.txt", and "sample2.txt" are provided in the repository. If you use one of these files, be sure to rename it to "configs.txt"

## Output
The output of this program is the .csv file, which contains rows of data that represent the system at various points in time. For each point in time, the following pieces of data are calculated:
- the iteration number
- the time stamp
- the temperature of the warm stream in celsius
- the temperature of the cool stream in celsius
- the enthalpy of the warm stream in kilojoules per kilogram
- the enthalpy of the cool steam in kilojoules per kilogram

For convenience, a brief summary of the convergence behavior of the program is also printed to the screen after the computation, along with a summary of the configurations used.

## Methodology 
The computation is performed by considering the flow of a small mass of fluid, known in the source code as the "fidelity", through the system. The fidelity is measured in kilograms and is calculated by multiplying the step size (sec) by the mass flow rate (kg/sec). During each time step, a mass of water equal to the value of "fidelity" leaves and enters both the heating element and the storage tank. In the case of the heating element, after this small amount of water leaves and is replenished by cooler water from the storage tank, the resulting temperature of the two fluids is computed by a weighted average according to the equation m_a(T_{a1} - T_{a2}) = m_b(T_{b2} - T_{b1}). Heat is then added to this mixture, and the resultant temperature is re-computed according to the equation h = m*C_p*(T_2 - T_1). These two calculations are also performed for fluid entering and leaving the tank, and the process is repeated iteratively. The program notes when the warm and cool temperatures converge and reports those values at the end of the computation.

## Assumptions
The following assumptions are employed:
- The pipes connecting the heating element and the storage tank are well-insulated such that no heat escapes from the pipes.
- The work provided by the pump only maintains the kinetic energy of the system and does alter its temperature.
- The fluid is well-mixed during all stages of the system such that the temperature is homogeneous for each stage.
- The work provided by an impeller in the storage tank only mixes the water and does not increase its temperature or otherwise provide energy to the system.

## Product Backlog
Eventually, it would be ideal to expand this project to include functionality for the following:
- Calculate the convergence of the system by the slope of the curve rather than the difference between data points. This way, the program can detect convergence for non steady-state systems.
- Terminate the simulation early when the convergence criteria is been met and copy the converge values for the rest of the simulation to save computational resources.
- Include configurations relating to fluid mechanics, such as the pipe's relative roughness, diameter, length, etc.
- Rather than assuming a constant value for the rate of heat leaving the system, calculate the rate of heat leaving the system as a function of the temperature gradient between the storage tank and the environment or target material, the coefficients of heat transfer of the material of the tank, the geometry of the tank, etc.
- Calculate the rate at which heat enters the system as a function of the efficiency of the solar panel, the area of the solar panel, the area of the heating tank, the time of day, etc.
- Model the heat sink as a object which must be maintained at a certain temperature, and then increase or decrease the solar panel's efficiency when the object's temperature needs to be raised or lowered, respectively.
