% Prepare the input data for the main script
% timothee.masquelier@alum.mit.edu

% Select a retina AER file (*.dat)
% Note : example files can be downloaded from
% http://sourceforge.net/apps/trac/jaer/wiki/AER%20data
% In the paper we used: "events-2005-12-28T11-14-28-0800 drive SC postoffice.dat"
[filename,path,filterindex]=uigetfile('*.dat','Select recorded retina data file');

% extracts input spike list from dat file
dat2mat2sl

% do multiple crops and concatenate them
concatSL
