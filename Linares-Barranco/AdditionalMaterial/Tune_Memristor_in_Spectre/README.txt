The files in this directory correspond to some of the results or indications given in the paper:

Camunas-Mesa L, Zamarreno-Ramos C, Perez-Carrasco JA, Masquelier T,Serrano-Gotarredona T, and Linares-Barranco B. On Spike-Timing-Dependent-Plasticity, Memristive Devices, and building a Self-Learning Visual Cortex. Frontiers in Neuromorphic Engineering.


-----------------------------------------
Specific Instructions for this directory:


PART 1: Run simulation in spectre (tested for IC 5.1.41 HF122)
--------------------------------------------------------------

<The spectre input netlist is in SimDIR/netlist/input.scs>

1) create a new working directory and copy folder SimDIR and file compute_stdpR_cvj.m in it.

2) go to SimDIR/netlist and execute script runSimulation

3) start Cadence DFWII without any design kit (type 'icfb')

4) On the icfb window: Tools->Analog Environment->Simulation

5) On the simulation window: Results->Select

6) On the new window: Browse-> select your working directory & hit ok

7) On the new window: highlight SimDIR & hit ok

8) Optionally you can visualize simulation results. Go to the icfb window:
   8.1) Tools->Analog Environment->Results Browser
   8.2) open folder tran-tran
   8.3) double click on variable to plot in graph window



PART 2: Export data and process with MATLAB
-------------------------------------------

9) At the icfb window dialog box type
   ocnPrint( VT("/stdp<1:3>") ?output "./stdp.dat" ?precision 16 ?numberNotation 'none)

  this generates text file "stdp.dat" with 4 columns (time, stdp<1>, stdp<2>, stdp<3>)
  where stdp<1> are the post-synaptic spikes, stdp<2> are the pre-synaptic spikes, and
  stdp<3> are the memristor resistance values (im mega ohms).

10) edit the file stdp.dat and strip its header (first 4 lines).

11) open MATLAB and run "compute_stdpR_cvj".
    This generates Fig. 27 of the paper.
