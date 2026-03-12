clear

alpha_d_ini=0;
dalpha_d_ini=0;
alpha_g_ini=0;
dalpha_g_ini=0;


R=10e-2;
l=15e-2;

phi0= -(R/(2*l))*(alpha_g_ini+alpha_d_ini);

x0=0;
y0=0;
% Cm_g=2;
% Cm_d=-6;

data_v=load('data_v.mat');
data_dphi=load('data_omega.mat');



t_simu=data_v.data_v.t(end);

V.time=data_v.data_v.t';
V.signals.values=double(data_v.data_v.v');
% V.signals.dimensions=[1 859];
Phi.time=data_dphi.data_dphi.t';
Phi.signals.values=double(data_dphi.data_dphi.dphi');
% Phi.signals.dimensions=[1 859];
%plot(time,v)

