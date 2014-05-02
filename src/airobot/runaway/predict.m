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
measurement_noise = 0.15*dist;
steps = 55;
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
    m(i,:) = normrnd(h(x_vec),measurement_noise);
    
    x_vec = f(x_vec);
end



s = zeros(steps-1,1);
a = zeros(steps-1,1);

for i =2:steps
    dx = m(i,1)-m(i-1,1);
    dy = m(i,2)-m(i-1,2);
    s(i-1) = sqrt(dx^2 + dy^2);
    a(i-1) = atan2(dy,dx);
end

da = zeros(steps-2,1);
th = zeros(steps-2,1);
for i=2:steps-1
    da(i-1) = a(i)-a(i-1);
    th(i-1) = a(i)-i*da(i-1);
end

s_avg = zeros(steps-1,1);

for i = 1:steps-1
    s_avg(i) = sum(s(1:i))/i;
end

da_avg = zeros(steps-2,1);
th_avg = zeros(steps-2,1);
for i = 1:steps-2
    da_avg(i) = sum(da(1:i))/i;
    th_avg(i) = sum(th(1:i))/i;
end



x_est = zeros(steps,2);

for j = 1:steps
    x_est_temp = zeros(j,2);
    for i = 1:j
        if i < 3
            x_est_temp(i,:) = m(i,:);
        else
            %dx = s_avg(i-1) * cos(th_avg(i-2)+(i-1)*da_avg(i-2));
            %dy = s_avg(i-1) * sin(th_avg(i-2)+(i-1)*da_avg(i-2));

            dx = s_avg(i-1) * cos(th_avg(j-2)+(i-1)*da_avg(j-2));
            dy = s_avg(i-1) * sin(th_avg(j-2)+(i-1)*da_avg(j-2));

            x_est_temp(i,1) = (x_est_temp(i-1,1)+dx + m(i,1))/2;
            x_est_temp(i,2) = (x_est_temp(i-1,2)+dy + m(i,2))/2;
        end
    end
    x_est(j,:) = x_est_temp(j,:);
end


x_predict = zeros(steps,2);
x_predict(1:3,:) = m(1:3,:);
for i = 3:steps-1
    
    dx = s_avg(i-1) * cos(th_avg(i-2)+(i-1)*da_avg(i-2));
    dy = s_avg(i-1) * sin(th_avg(i-2)+(i-1)*da_avg(i-2));
    x_predict(i+1,1) = x_est(i,1)+dx;
    x_predict(i+1,2) = x_est(i,2)+dy;
end
plot(traj(:,1),traj(:,2),m(:,1),m(:,2),x_est(:,1),x_est(:,2),x_predict(:,1),x_predict(:,2))

error= zeros(steps,1);
for i =1:steps
    error(i) = sqrt ( (traj(i,1)-x_predict(i,1))^2+(traj(i,2)-x_predict(i,2))^2);
end

            
    
       
