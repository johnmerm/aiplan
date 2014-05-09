x_hunt = zeros(steps,5);
x_hunt(1,1) = -10;
x_hunt(1,2) = -10;
for i = 1:steps-1
    est = estimates(i,:);
    est_next = f(est);
    dx = x_hunt(i,1)-est_next(1);
    dy = x_hunt(i,2)-est_next(2);
    angle = atan2(dy,dx);
    turning = x_hunt(i,3)-angle;
    step = sqrt(dx^2+dy^2);
    step = min(dist,step);
    x_hunt(i,4) = step;
    x_hunt(i,5) =turning;
    x_hunt(i+1,:) = f(x_hunt(i,:));
end




for i = 1:steps
    plot(trajectory(i,1),trajectory(i,2),'.',measurements(i,1),measurements(i,2),estimates(i,1),estimates(i,2),x_hunt(i,1),x_hunt(i,2),'+');
    M(i) = getframe;
end
movie(M,30);