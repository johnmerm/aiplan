clear;

dist = 1.5;
turn = 2*pi / 34.0;
measurement_noise = 0.05*dist;
steps = 200;
init = [2.1; 4.3; 0.5];


trajectory = zeros(steps,5);
measurements  = zeros(steps,2); 
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
    trajectory(i,:) = x_vec;
    measurements(i,:) = normrnd(h(x_vec),measurement_noise);
    x_vec = f(x_vec);
end


%EKF estimation
estimates = [0 0 2*pi*rand 2*rand 2*pi*rand];
syms x y t s dt real

x_sym = [x y t s dt]';

x_vec = zeros(5,1);
F = jacobian(f(x_sym),x_sym);
H = jacobian(h(x_sym),x_sym);

P = 10000*eye(5);
R = 3*measurement_noise*eye(2);
error = zeros(steps,1);

for i = 1:steps
    
    
    Fv = eval(subs(F,x_sym,x_vec));
    x_vec = f(x_vec);
    P = Fv*P*Fv';
    

    z = measurements(i,:)';
    Hv = eval(subs(H,x_sym,x_vec));
    y_vec = z-h(x_vec);
    S = Hv*P*Hv' + R;
    K = P*Hv'*pinv(S);
    x_vec = x_vec + K*y_vec;
    P = (eye(5) - K*Hv)*P;
    
    
    
    estimates(i,:) = x_vec;
    error(i) = sqrt((trajectory(i,1)-estimates(i,1))^2 + (trajectory(i,2)-estimates(i,2))^2);
end


subplot(3,2,1),
plot(trajectory(:,1),trajectory(:,2),measurements(:,1),measurements(:,2),estimates(:,1),estimates(:,2));
subplot(3,2,2),
plot(1:steps,trajectory(:,3),1:steps,estimates(:,3));
subplot(3,2,3),
plot(1:steps,trajectory(:,4),1:steps,estimates(:,4));
subplot(3,2,4),
plot(1:steps,trajectory(:,5),1:steps,estimates(:,5));

subplot(3,2,5),plot(error);

