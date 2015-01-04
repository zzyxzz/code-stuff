The files in this directory correspond to some of the results or indications given in the paper:

Camunas-Mesa L, Zamarreno-Ramos C, Perez-Carrasco JA, Masquelier T,Serrano-Gotarredona T, and Linares-Barranco B. On Spike-Timing-Dependent-Plasticity, Memristive Devices, and building a Self-Learning Visual Cortex. Frontiers in Neuromorphic Engineering.


-----------------------------------------
Specific Instructions for this directory:


SimDIR contains spectre netlist files to simulate the results in Fig.7

1) Create a working directory for Cadence DFWII and initialize your environment (without design kit)

2) go to SimDIR/netlist and execute runSimulation from the unix prompt

3) go back to SimDIR and open DFWII (icfb)

4) Tools->Result Browser

5) double click on tran-tran to see available variables:

     R is memristor resistance in time (in mega ohms)
     vm is memristor voltage
     V1 is a voltage source whose current is memristor current

6) double click on variable to graph them

The spectre netlist file is in SimDIR/netlist/input.scs
