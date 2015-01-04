The files in this directory correspond to some of the results or indications given in the paper:

Camunas-Mesa L, Zamarreno-Ramos C, Perez-Carrasco JA, Masquelier T,Serrano-Gotarredona T, and Linares-Barranco B. On Spike-Timing-Dependent-Plasticity, Memristive Devices, and building a Self-Learning Visual Cortex. Frontiers in Neuromorphic Engineering.


-----------------------------------------
Specific Instructions for this directory:


./mat contains data

./script contains the code:
	prepareData.m prepares the input spike trains, and save them in ./mat. You need to run it only once.
        The particular retina recording data file used for fig.24 in the paper, can be downloaded from
        http://sourceforge.net/apps/trac/jaer/wiki/AER%20data  (look for 'Driving in pasadena to the post office').
	main.m runs one full iteration the simulation. All the parameters are gathered in param.m
	You should compile the mex files first (type "mex STDPContinuous.c" and "mex pspKernel.c" from within matlab)
        main.m executes one iteration. To execute 5 iterations (as in the paper) just execute it again 5 times. It
        will as initial weights those saved from the previous run.
        generateFig24 draws the sub figures of Fig.24 in the paper.

Tested on Windows and Linux, with Matlab R2007b and R2010a
