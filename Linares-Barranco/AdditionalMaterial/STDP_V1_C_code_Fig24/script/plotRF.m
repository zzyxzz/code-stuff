figure
% load weight
N=sqrt(size(weight,1)/2); % RF size

n = 6; % number of row and col

for i=1:size(weight,2)
    subplot(n,2*n,2*i-1)
    hist(weight(:,i))
    title([int2str(i) ' - nW=' int2str(sum(weight(:,i)>.5))])
    set(gca,'XTickLabel',{})
    set(gca,'YTickLabel',{})
    axis([0 1 0 40])
    axis 'auto y'
    
    subplot(n,2*n,2*i)
        for x = 1:N
            for y = 1:N
                if weight( x + (y-1)*N, i )>.5
                    plot(x,y,'o','MarkerSize',4);
                    hold on
                end
                if weight( x + (y-1)*N + N^2, i )>.5
                    plot(x,y,'r+','MarkerSize',4);
                    hold on
                end
            end
        end
         set(gca,'XTick',[])
         set(gca,'YTick',[])
        axis([.5 N+.5 .5 N+.5])
        
    
end
