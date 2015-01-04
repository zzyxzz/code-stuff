function HHsimplest()
% Simulates the Hodgkin-Huxley neuron for 100 millseconds. Stimulates the
% neuron with input to induce spikes and plots the membrane potential.

% initialization and constants

% HH 1952 PAPER PARAMS!!!! (give a resting potential of 0mV)
g_K = 36;
g_Na = 120;
g_leak = 0.3;
C_m = 1;
V_K = 12;        % in HH 1952 table 3 this is -12...???
V_Na = -115;     
V_leak = -10.6;  % in HH 1952 table 3 this is not specified...

sim_time = 100;          % total simulation time in milliseconds
t_step = 0.01;           % timestep in milliseconds
N = 1 + sim_time/t_step; % total number of timesteps

V = zeros(1,N);
n = zeros(1,N);
m = zeros(1,N);
h = zeros(1,N);

V_rest = 0;
V(1) = V_rest;
n(1) = alpha_n(V_rest)/(alpha_n(V_rest)+beta_n(V_rest));
m(1) = alpha_m(V_rest)/(alpha_m(V_rest)+beta_m(V_rest));
h(1) = alpha_h(V_rest)/(alpha_h(V_rest)+beta_h(V_rest));

time = 0:t_step:sim_time;   % time array

% set input current from 10 to 90 milliseconds
Iext = zeros(1,N);
Iext(round(10/t_step):round(90/t_step)) = -10;

% the simulation
tic;
for i = 2:N
    
    I_K = g_K*n(i-1)^4*(V(i-1)-V_K);
    I_Na = g_Na*m(i-1)^3*h(i-1)*(V(i-1)-V_Na);
    I_leak = g_leak*(V(i-1)-V_leak);
    
    deriv = (Iext(i) - (I_K + I_Na + I_leak))/C_m;
    V(i) = V(i-1) + deriv*t_step;
    
    m_deriv = alpha_m(V(i))*(1-m(i-1)) - beta_m(V(i))*m(i-1);
    m(i) = m(i-1) + m_deriv*t_step;
    n_deriv = alpha_n(V(i))*(1-n(i-1)) - beta_n(V(i))*n(i-1);
    n(i) = n(i-1) + n_deriv*t_step;
    h_deriv = alpha_h(V(i))*(1-h(i-1)) - beta_h(V(i))*h(i-1);
    h(i) = h(i-1) + h_deriv*t_step;

end
toc;

plot(time,-V)
hold on
plot(time,-Iext-22,':')
hold off

end

function result = alpha_n(V)
    result = 0.01*(V+10)/(exp((V+10)/10)-1);
end

function result = beta_n(V)
    result = 0.125*exp(V/80);
end

function result = alpha_m(V)
    result = 0.1*(V+25)/(exp((V+25)/10)-1);
end

function result = beta_m(V)
    result = 4*exp(V/18);
end

function result = alpha_h(V)
    result = 0.07*exp(V/20);
end

function result = beta_h(V)
    result = 1/(exp((V+30)/10)+1);
end
