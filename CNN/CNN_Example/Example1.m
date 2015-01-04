%This is example which is simulated with the conditions as shown in the paper published by Chua-Yang
% In the same way, you may change with different conditions to verify the
% results. Note that, I got the results exactly presented in the paper. 
% This is done by Thang Manh Hoang, email: hmthang01@yahoo.com
% Faculty of Electronics and Telecommunications, Hanoi University of
% Technology, Hanoi, VIETNAM,

%Define
clc;
clear all;

%Template defintion

CellRow=4;% The number of row of cells
CellCol=4;% The number of colume of cells

r=1;

A=[0 1.0 0; 1.0 2.0 1.0; 0 1.0 0];
B=[0 0 0; 0 0 0; 0 0 0];

I=[0 0 0 0; 0 0 0 0; 0 0 0 0; 0 0 0 0]; % the size of independent sources/bias for Cells must be equal to that of CNN's size 
Initials=[-0.8 1.0 -1.0 -0.6; 1.0 1.0 1.0 -1.0; -1.0 0.9 -1.0 -0.8; -0.9 -1.0 -0.7 -0.8]; % Initial states

[Arow Acol]=size(A); %Size of CNN
[Brow Bcol]=size(B); %note that sizes of A and B are equal

% Set the template for CNN

for i=1:CellRow
    for j=1:CellCol
        for n=1:Arow
            for m=1:Acol
                comm=sprintf('set_param(''Cellmodel/C%d,%d/A%d,%d'',''value'',''%.3f'')',i,j,n,m,A(n,m));
                eval(comm);
                comm=sprintf('set_param(''Cellmodel/C%d,%d/B%d,%d'',''value'',''%.3f'')',i,j,n,m,B(n,m));
                eval(comm);
            end
        end
        comm=sprintf('set_param(''Cellmodel/I%d_%d'',''value'',''%.3f'')',i,j,I(i,j)); % Independent bias/sources
                eval(comm);

        comm=sprintf('set_param(''Cellmodel/C%d,%d/Integrator'',''Initial'',''%.3f'')',i,j,Initials(i,j));% Initial States to cells
                eval(comm);
    end
end

sim('Cellmodel');

% The presentation of results
% Output of CNN
disp('-----------------Template, Independent Source/bias, Initial State of CNN------------------');
disp('Template as shown in Figure 8a in the page 1265');
A
B
disp('Independent Source/bias: I');
I
disp('Initial State of CNN:');
Initials
disp('-----------------------------------------Results-----------------------------------------');
disp('The outputs of CNN');
lastpoint=max(size(out11));
Output_of_CNN=[ out11(lastpoint) out12(lastpoint) out13(lastpoint) out14(lastpoint);
                out21(lastpoint) out22(lastpoint) out23(lastpoint) out24(lastpoint);
                out31(lastpoint) out32(lastpoint) out33(lastpoint) out34(lastpoint);
                out41(lastpoint) out42(lastpoint) out43(lastpoint) out44(lastpoint)]

% Final State of CNN 
disp('Final State of CNN as shown in the Figure 9 in the page 1266');
lastpoint=max(size(s11));
Final_State_of_CNN=[    s11(lastpoint) s12(lastpoint) s13(lastpoint) s14(lastpoint);
                        s21(lastpoint) s22(lastpoint) s23(lastpoint) s24(lastpoint);
                        s31(lastpoint) s32(lastpoint) s33(lastpoint) s34(lastpoint);
                        s41(lastpoint) s42(lastpoint) s43(lastpoint) s44(lastpoint)]
disp('Plot the transient of C(2,2) as shown in Figure 9d');                    
plot(s22(1:500))
grid on;
hold on;
plot(out22(1:500));                    
disp('-----------------------------------------End of example 1-----------------------------------------');