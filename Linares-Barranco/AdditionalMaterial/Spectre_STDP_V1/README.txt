The files in this directory correspond to simulating in spectre (with components macro models)
a simplified V1 visual cortex layer, as described in Section 8.3 of the paper:

Camunas-Mesa L, Zamarreno-Ramos C, Perez-Carrasco JA, Masquelier T,Serrano-Gotarredona T, and Linares-Barranco B. On Spike-Timing-Dependent-Plasticity, Memristive Devices, and building a Self-Learning Visual Cortex. Frontiers in Neuromorphic Engineering, inaugural issue article.


-----------------------------------------
Specific Instructions for this directory:

PART 1: Prepare stimulus data
------------------------------
We are using AER events produced by an AER temporal contrast retina.
Specifically, we are using a 521 sec recording with 20.5 million
events, which can be downloaded from:

``Driving in pasadena to the post office'' available at http://sourceforge.net/apps/trac/jaer/wiki/AER\%20data

Download the file and rename it to "postoffice.dat".
You can visualize this video by using the free jAER software from http://sourceforge.net/apps/trac/jaer/wiki

Place postoffice.dat in the present folder, and run in MATLAB 'postoffice'.
This will place in folder po7x7 a set of .mat files. Each includes the events of a 7x7 patch of the full
128x128 pixel array of the retina.

After this, execute in MATLAB 'write_po7x7_files'. This will place in folder 'stims' 49x2 text files,
each describing the time waveform of the sequence of spikes needed as stimulus for one pixel/neuron (as
shown in fig. 26 of the paper).
The script selects only one of the 324 7x7 patches in folder po7x7.

Copy/move folder 'stims' to SimDIR/netlist. We are now ready to simulate in Spectre.


PART 2: Run simulation in spectre (tested for IC 5.1.41 HF122)
--------------------------------------------------------------

<The spectre input netlist is in SimDIR/netlist/input.scs>

1) create a new working directory and copy folders SimDIR, RPSfiles, RNSfiles and file getGpGn.m in it.

2) go to SimDIR/netlist and execute script runSimulation (tested with spectre version 7.0.1.076 25Aug2008)
   This runs a 600sec simulation, but only some top level nodes are saved, and they are saved
   for every 1000ms (by setting strobeperiod=1000ms). You may want to erase this parameter if you
   just want to run the simulation for a short initial time only.
   This is a one iteration monte carlo simulation (skipping the nominal iteration by setting donominal=no),
   because memristor synapses are initialized to random values close to Rmin.

3) go back to your working directory and start Cadence DFWII without any design kit (type 'icfb')

4) On the icfb window: Tools->Analog Environment->Simulation

5) On the simulation window: Results->Select

6) On the new window: Browse-> select your working directory & hit ok

7) On the previous new window: highlight SimDIR & hit ok

8) Optionally you can visualize simulation results. Go to the icfb window:
   8.1) Tools->Analog Environment->Results Browser
   8.2) open folder mc1_tran-montecarlo
   8.3) double click on variable to plot in graph window



PART 2: Export data and process with MATLAB
-------------------------------------------

9)  At the icfb window dialog box type
    ocnPrint( VT("/Rp<1:784>") ?output "./Rp.dat" ?precision 16 ?numberNotation 'none)

    This generates text file "Rp.dat" containing the evolution in time of the positive synapse resistances
    (in Mega ohms) in 1s steps. File "Rp.dat" will be of size 20MB.
    Place this file in the RPSfiles folder. At the unix prompt, go to the RPSfile folder and type:

    split -d -a 3 -l 607 Rp.dat

    This splits Rp.dat into 784 smaller files. You may erase Rp.dat.
   
10) Let's repeat 9) for the the Rn nodes.
    At the icfb window dialog box type
    ocnPrint( VT("/Rn<1:784>") ?output "./Rn.dat" ?precision 16 ?numberNotation 'none)

    This generates text file "Rn.dat" containing the evolution in time of the negative synapse resistances
    (in Mega ohms) in 1s steps. File "Rn.dat" will be of size 20MB.
    Place this file in the RNSfiles folder. At the unix prompt, go to the RNSfile folder and type:

    split -d -a 3 -l 607 Rn.dat

    This splits Rn.dat into 784 smaller files. You may erase Rn.dat.

11) open MATLAB and run "getGpGn".
    This generates Fig. 25 of the paper.
