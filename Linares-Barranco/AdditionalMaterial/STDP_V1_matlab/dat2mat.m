function [CIN]=loadaerdat_matlab(file);
%function [allAddr,allTs]=loadaerdat(file);
% loads events from a .dat file.
% allAddr are int16 raw addresses.
% allTs are int32 timestamps (1 us tick).
% noarg invocations open file browser dialog (in the case of no input argument) directly create vars allAddr, allTs in
% base workspace (in the case of no output argument).
%
% Header lines starting with '#' are ignored and printed
%
% Note: it is possible that the header parser can be fooled if the first
% data byte is the comment character '#'; in this case the header must be
% manually removed before parsing. Each header line starts with '#' and
% ends with the hex characters 0x0D 0x0A (CRLF, windows line ending).

maxEvents=30e6;

if nargin==0,
    [filename,path,filterindex]=uigetfile('*.dat','Select recorded retina data file');
    if filename==0, return; end
end
if nargin==1,
    path='';
    filename=file;
end


f=fopen([path,filename],'r');
% skip header lines
bof=ftell(f);
line=native2unicode(fgets(f))
tok='#!AER-DAT';
version=0;

while line(1)=='#',
    if strncmp(line,tok, length(tok))==1,
        version=sscanf(line(length(tok)+1:end),'%f');
    end
    fprintf('%s\n',line(1:end-2)); % print line using \n for newline, discarding CRLF written by java under windows
    bof=ftell(f);
    line=native2unicode(fgets(f)); % gets the line including line ending chars
end
version2=version
switch version,
    case 0
        fprintf('No #!AER-DAT version header found, assuming 16 bit addresses\n');
        version=1;
    case 1
        fprintf('Addresses are 16 bit\n');
    case 2
        fprintf('Addresses are 32 bit\n');
    otherwise
        fprintf('Unknown file version %g',version);
end

numBytesPerEvent=6;
switch(version)
    case 1
        numBytesPerEvent=6;
    case 2
        numBytesPerEvent=8;
end

        
fseek(f,0,'eof');
numEvents=floor((ftell(f)-bof)/numBytesPerEvent); % 6 bytes/event
if numEvents>maxEvents, 
    fprintf('clipping to %d events although there are %d events in file\n',maxEvents,numEvents);
    numEvents=maxEvents;
end

% read data
fseek(f,bof,'bof'); % start just after header
switch version,
    case 1
        allAddr=uint16(fread(f,numEvents,'uint16',4,'b')); % addr are each 2 bytes (uint16) separated by 4 byte timestamps
        fseek(f,bof+2,'bof'); % timestamps start 2 after bof
        allTs=uint32(fread(f,numEvents,'uint32',2,'b')); % ts are 4 bytes (uint32) skipping 2 bytes after each
    case 2
        allAddr=uint32(fread(f,numEvents,'uint32',4,'b')); % addr are each 4 bytes (uint32) separated by 4 byte timestamps
        fseek(f,bof+4,'bof'); % timestamps start 4 after bof
        allTs=uint32(fread(f,numEvents,'uint32',4,'b')); % ts are 4 bytes (uint32) skipping 4 bytes after each
end

fclose(f);

if nargout==0,
   assignin('base','allAddr',allAddr);
   assignin('base','allTs',allTs);
   fprintf('%d events assigned in base workspace as allAddr,allTs\n', length(allAddr));
   dt=allTs(end)-allTs(1);
   fprintf('min addr=%d, max addr=%d, Ts0=%d, deltaT=%d=%.2f s assuming 1 us timestamps\n',...
       min(allAddr), max(allAddr), allTs(1), dt,double(dt)/1e6);
end











tpo=allTs;
%tpo=allTs*1e-9;
kk=find(tpo(1:end-1)>tpo(2:end));
if ~isempty(kk)

    for i=1:length(kk)-1
        tpo(kk(i)+1:kk(i+1))=tpo(kk(i))*ones(size(tpo(kk(i)+1:kk(i+1)))) + tpo(kk(i)+1:kk(i+1));
    end
    tpo(kk(end)+1:end)=tpo(kk(end))*ones(size(tpo(kk(end)+1:end))) + tpo(kk(end)+1:end);

end
%tpo=tpo-tpo(1)*ones(size(tpo));
%tpo=tpo-tpo(1)*ones(size(tpo,2),1);
e=find(allAddr<=0);
allAddr(e)=0;
%32767
%x=bitshift(bitand(allAddr,255*256),-16)+1;
%x=bitshift(bitand(allAddr, 32767*65536),-16)+1;
%x=bitshift(bitand(allAddr, 127*256),-16)+1;
%x=bitshift(bitand(allAddr, 127*256),-8)+1;
%y=bitand(allAddr,63)+1;
%y=bitand(allAddr,32767)+1;
%y=bitand(allAddr,127)+1;
%in=find(x < 129);
%pol=bitshift(bitand(allAddr,256*64),-14);
%pol=bitshift(bitand(allAddr,64),-6);
%pol(in)=1;
%x=min(x,64);
%x=max(x,1);
%y=min(y,64);
%y=max(y,1);

retinaSizeX=128;

persistent xmask ymask xshift yshift polmask
if isempty(xmask),
    xmask = hex2dec ('fE'); % x are 7 bits (64 cols) ranging from bit 1-8
    ymask = hex2dec ('7f00'); % y are also 7 bits
    xshift=1; % bits to shift x to right
    yshift=8; % bits to shift y to right
    polmask=1; % polarity bit is LSB
end


%mask aer addresses to ON and OFF address-strings
% find spikes in frame window
% if any(addr<0), warning('negative address'); end

addr=abs(allAddr); % make sure nonnegative or an error will result from bitand (glitches can somehow result in negative addressses...)
x=retinaSizeX-1-double(bitshift(bitand(addr,xmask),-xshift)); % x addresses
y=double(bitshift(bitand(addr,ymask),-yshift)); % y addresses
pol=1-2*double(bitand(addr,polmask)); % 1 for ON, -1 for OFF

%x=bitshift(bitand(allAddr,127*256),-8)+1;

%y=bitand(allAddr,127)+1;
in=find(x < 129);
%pol=bitshift(bitand(allAddr,128),-7);
%pol(in)=1;


%x=min(x,128);
%x=max(x,1);
%y=min(y,128);
%y=max(y,1);
x=x+1;
y=y+1;
%CIN=[tpo zeros(length(x),1) -1*ones(length(x),1) x y pol];
tpo(:)=tpo(:)-tpo(1);


%x2=129-y;
%y=x;
%CIN=[tpo zeros(length(x),1) -1*ones(length(x),1) x2 y pol];
CIN=[tpo zeros(length(x),1) -1*ones(length(x),1) x y pol];
CIN=double(CIN);
CIN(:,3)=-1;
%e=find(CIN(:,6)~=0);
%CIN(e(1:10),6)=-1;
e=find(CIN(:,6)==0);
CIN(e,6)=-1;



















