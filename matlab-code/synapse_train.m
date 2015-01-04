% synapse_train.m

clear
dt = 0.00002;   % time step size
tmax=0.5;       % maximum time

t=0:dt:tmax;    % vector of time points
Nt = tmax/dt;   % total number of time points

Nspikes = 8;        % number of spikes in train
spikegap = 0.025;   % separation of spikes in time

timestart = 0.1;    % time to start spike train

spikes=zeros(size(t)); % will contain times of spikes

for n = 1:Nspikes                                  % do for each spike in train
    ispike = round((timestart+(n-1)*spikegap)/dt); % time point for each spike
    spikes(ispike) = 1;                            % generate spike at that time 
end

D = ones(size(t));      % D is depression factor
F = ones(size(t));      % F is facilitation factor
p0 = 0.05;              % p0 is base release probability without facilitation
pr=p0*F;                % pr is vesicle release probability including facilitation
p=pr.*D;                % p is proportion of maximum possible release

Ssyn = zeros(size(t));  % Ssyn is the synaptic gating variable as a function of time

tau_syn2 = 0.002;       % determines time for synaptic current to rise
tau_syn1 = 0.020;       % decay time for synaptic current
tau_d = 0.2;            % time for recovery from depression
tau_f = 0.5;            % time for recovery from facilitation
f_f = 0.1;              % increase in pr immediately following a spike

nwidth = round(10*tau_syn1/dt); % just add current from a spike for this number of time points

spiketimes = dt*find(spikes);   % the exact time of each spike
Nspikes = length(spiketimes);   % the number of spikes
for n = 1:Nspikes
    ispike = round(spiketimes(n)/dt);   % time point number for the nth-spike
    pr(ispike) = p0*F(ispike);          % vesicle release probability for that spike
    p(ispike) = pr(ispike)*D(ispike);   % fraction of maximum possible release
    
    D(ispike+1) = D(ispike)*(1-p(ispike)); % depress by the proportion of released vesicles

    pr(ispike+1) = pr(ispike)+f_f*(1-pr(ispike));  % facilitate the probability of vesicle release  
    F(ispike+1) = pr(ispike+1)/p0;                 % update the facilitation factor
    
    p(ispike+1) = pr(ispike+1)*D(ispike+1);        % update the total release proportion

    if n < Nspikes                                 % if it is not the last spike
        nspike = round(spiketimes(n+1)/dt);        % need to update until the next spike 
    else                                           % otherwise 
        nspike = length(t);                        % update till the last time point
    end

    for i = ispike+1:nspike-1                       % set of points to update
        D(i+1) = 1 + (D(i)-1)*exp(-dt/tau_d);       % D decays back to 1 from below
        F(i+1) = 1 + (F(i)-1)*exp(-dt/tau_f);       % F decays back to 1 from above
        pr(i+1) = p0*F(i+1);                        % update vesicle release probability
        p(i+1) = D(i+1)*F(i+1);                     % update total release proportion
    end 
    
    iend = min(ispike+nwidth,length(t))             % how many points following a spike to calculate
    for i=ispike+1:iend                             % synaptic current (either nwidth or until tmax)
        tdiff = dt*(i-ispike);                      % time since the spike is tdiff
        Ssyn(i) = Ssyn(i) + ...                     % update synaptic gating variable with saturation
            p(ispike)*(1-Ssyn(ispike))*(exp(-tdiff/tau_syn1)-exp(-tdiff/tau_syn2));        
    end
end

figure(1)
subplot(4,1,1)
plot(t,spikes)
subplot(4,1,2)
plot(t,D)
subplot(4,1,3)
plot(t,F)
subplot(4,1,4)
plot(t,Ssyn)

