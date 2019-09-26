# thermoSimulation

## Overview
This is a cool program.
step through it function by function; mostly linear execution.

## Usage

In order to close the program, close the graph window that pops up at the end.

## Input
- the initial temperatures can cross
- suggested input files for interesting configurations
- heat out from the perspective of the environment (so only give positive values. Error if you don't)

## Output

## Assumptions
- well-mixed and insulated
- kinetic energy from mixing does not increase the temperature of the water in the tank.

## System Requirements
- spell check this thing
- Run the command "pip install matplotlib"

## Product Backlog
- make the heat transfer a function of the material, the geometry of the vessles, and efficiency of the soloar panel, etc.
- make it make decission about how much heat to let through
- give the option of discontinuing the simulation after convergence to save computation time
- set the convergence criteria to be triggered based on slop, not just a difference of 0, so that for non-steady state problems the convergence can be determined.
- Include configurations for considerations regarding fluid mechanics (relative roughness of pipe, diameter and length of pipe,
