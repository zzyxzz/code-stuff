The files in this directory correspond to some of the results or indications given in the paper:

Camunas-Mesa L, Zamarreno-Ramos C, Perez-Carrasco JA, Masquelier T,Serrano-Gotarredona T, and Linares-Barranco B. On Spike-Timing-Dependent-Plasticity, Memristive Devices, and building a Self-Learning Visual Cortex. Frontiers in Neuromorphic Engineering.


-----------------------------------------
Specific Instructions for this directory:

SimDIR contains spectre netlist files to simulate the results in Fig.19.
This simulation uses MOS, Resistors, Capacitors, and Diode models provided by some vendor.
These models are not provided in these directories, and you need to specify the paths corresponding
to the models provided by your vendor. Please include them in the corresponding space holder
in file input.scs.

1) Create a working directory for Cadence DFWII and initialize your environment (without design kit)

2) go to SimDIR/netlist and execute runSimulation from the unix prompt

3) go back to SimDIR and open DFWII (icfb)

4) Tools->Result Browser

5) double click on tran-tran to see available variables:

     mos threshold "weight" values are indexed rij

6) double click on variables to graph them

The spectre netlist file is in SimDIR/netlist/input.scs
