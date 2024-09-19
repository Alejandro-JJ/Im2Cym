# Im2Cym - Draw initial states for your simulations

The package Im2Cym was designed to create initial states
of Cytosim simulations in which filaments can be distributed arbitrarily based
on input images.
This gives the user the possibility to:

* Hand draw initial states with different colours based on distinct filament populations
* Upload experimental images where distributions of filaments are in different channels

# Usage

Im2Cym is a python-based script, in which a single function 

```
3Populationgenerator.py
``` 

parses the final .cym configuration function for a simulation.
The input parameters of this function are:
* impath: string with the absolte path of an RGB image representig the initial state. Each channel in the convention (Red, Green, Blue) can represent the distribution of three distincts populations of filaments
* outputname: a string for the name of the final .cym file
* cellwidth: the window size of the simulation with periodic boundary conditions
* NT: number of filaments in each (RGB) population
* LT: length of the filaments in micrometers
* WT: display width of the filaments in micrometer
* simtime: the simulated time before and after the appearance of docking sites

For the script to properly work, the .cym template "ThreePopulations_template.txt" needs to be in the same folder where the user is working. This template will be formatted and re-saved with the provided outputname.

Ongoin work!
