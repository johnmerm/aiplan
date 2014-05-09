% traj =[...
%     2.1000 4.3000;...
%     3.2618  5.2488;...
%     4.2295 6.3949;...
%     4.9701 7.6993;...
%     5.4585 9.1176;...
%     5.6779 10.6014;...
%     5.6209 12.1004;...
%     5.2895 13.5633;...
%     4.6948 14.9404;...
%     3.8573 16.1848;...
%     2.8054   17.2541];
% 
% m = traj;
% m = normrnd(traj,0.5);



clear;

dist = 1.5;
turn = 2*pi / 34.0;
measurement_noise = dist;
steps = 5*35;
init = [2.1; 4.3; 0.5];


traj = zeros(steps,2);
m  = zeros(steps,2); 
last = init;


% Extended Kalman Filter




f = @(x)[x(1)+x(4)*cos(x(3)+x(5));...
         x(2)+x(4)*sin(x(3)+x(5));...
         x(3)+x(5);...
         x(4);...
         x(5);...
        ];

h = @(x)[x(1);x(2)];

x_vec = [init;dist;turn];
for i=1:steps
    traj(i,:) = h(x_vec);
    m(i,:) = traj(i,:);
    m(i,:) = normrnd(h(x_vec),measurement_noise);
    
    x_vec = f(x_vec);
end



s = zeros(steps,1);
s_avg = zeros(steps,1);
a = zeros(steps,1);



for i =2:steps
    dx = m(i,1)-m(i-1,1);
    dy = m(i,2)-m(i-1,2);
    s(i) = sqrt(dx^2 + dy^2);
    s_avg(i) = sum(s(2:i))/(i-1);
    a(i) = atan2(dy,dx);    
    
    while abs(a(i)-a(i-1))>pi
        a(i) = 2*pi+a(i);
    end
end


da = zeros(steps,1);
th = zeros(steps,1);
da_avg = zeros(steps,1);
th_avg = zeros(steps,1);
for i = 3:steps
    da(i) = a(i)-a(i-1);
    th(i) = a(i) - (i-1)*da(i);
    
    da_avg(i) = sum(da(3:i))/(i-2);
    th_avg(i) = sum(th(3:i))/(i-2);
end

x_predict = zeros(steps,2);
x_est = zeros(steps,2);
error_measurement = zeros(steps,1);
error_predict = zeros(steps,1);
error_est = zeros(steps,1);

for i =1:steps
    if i<3
        x_est(i,:) = m(i,:);
        x_predict(i,:) = m(i,:);
    else
        x_predict(i,1) = x_est(i-1,1)+s_avg(i-1)*cos(th_avg(i-1)+(i-1)*da_avg(i-1));
        x_predict(i,2) = x_est(i-1,2)+s_avg(i-1)*sin(th_avg(i-1)+(i-1)*da_avg(i-1));
        
        
        %measure - update
        x_est(i,1) = (x_predict(i,1)+m(i,1))/2;
        x_est(i,2) = (x_predict(i,2)+m(i,2))/2;
        
    end
    error_measurement(i) = sqrt((m(i,1)-traj(i,1))^2 +(m(i,2)-traj(i,2))^2);
    error_predict(i) = sqrt((x_predict(i,1)-traj(i,1))^2 +(x_predict(i,2)-traj(i,2))^2);
    error_est(i) = sqrt((x_est(i,1)-traj(i,1))^2 +(x_est(i,2)-traj(i,2))^2);
end

subplot(2,2,1),plot([2:steps],s(2:steps),[2:steps],s_avg(2:steps))
subplot(2,2,2),plot([3:steps],th(3:steps),[3:steps],th_avg(3:steps))
subplot(2,2,3),plot([1:steps],error_measurement,[1:steps],error_predict,[1:steps],error_est)
subplot(2,2,4),plot(m(:,1),m(:,2),x_predict(:,1),x_predict(:,2),traj(:,1),traj(:,2))
