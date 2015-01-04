weight = zeros(PARAM.nAfferent,PARAM.nNeuron);
for n=1:PARAM.nNeuron
    weight(:,n) = neuron(n).weight';
end
disp([num2str(mean(sum(weight>0.5))) ' synapses selected on avg' ])


plotRF

figure
colors = get(gcf,'DefaultAxesColorOrder');
subplot(3,1,1)
for n=1:PARAM.nNeuron
    if neuron(n).nFiring>0
        [b, x] = hist(neuron(n).firingTime(1:neuron(n).nFiring),100);
        plot(x,b/(x(2)-x(1)),'Color',colors(mod(n-1,7)+1,:))
        hold on
    end
end
%axis([0 1 .5 PARAM.nNeuron+.5])
%axis 'auto x'

subplot(3,1,2)
maxTime = 0;
for n=1:PARAM.nNeuron
    if neuron(n).nFiring>0
        maxTime = max(maxTime,neuron(n).firingTime(neuron(n).nFiring));
        plot(neuron(n).firingTime(1:neuron(n).nFiring),n*ones(1,neuron(n).nFiring),'.')
        hold on
    end
end
axis([maxTime-10 maxTime .5 PARAM.nNeuron+.5])

subplot(3,1,3)
for n=1:PARAM.nNeuron
    plot(neuron(n).firingTime(1:neuron(n).nFiring),n*ones(1,neuron(n).nFiring),'.')
    hold on
end
axis([0 10 .5 PARAM.nNeuron+.5])

disp(['Avg firing rate =' num2str(mean([neuron(:).nFiring])/maxTime) ])
