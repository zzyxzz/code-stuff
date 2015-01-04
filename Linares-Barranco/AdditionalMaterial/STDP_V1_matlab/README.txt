The files in this directory correspond to some of the results or indications given in the paper:

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

PART 2: Run the simulation
--------------------------
Within MATLAB run "sptr_sim"
