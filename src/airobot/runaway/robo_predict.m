x_predict = zeros(steps,5);
x_predict(1,:) = estimates(1,:);
for i = 2:steps
    x_predict(i,:) = f(estimates(i-1,:));
end


    

x_hunt = zeros(steps,5);
x_hunt(1,1) = -10;
x_hunt(1,2) = -10;


plot(x_predict(:,1),x_predict(:,2),trajectory(:,1),trajectory(:,2));
hold on

for i = 1:steps-1
    plot(trajectory(i,1),trajectory(i,2),'r+');
    if i<50
        x_hunt(i+1,:)=x_hunt(i,:);
    elseif i == 50
        j=1;
        est_next = x_predict(i,:);
        dx = x_hunt(i,1)-est_next(1);
        dy = x_hunt(i,2)-est_next(2);
        step = sqrt(dx^2+dy^2);
        diff_dist = j*dist-step;
        while diff_dist<0
            j = j+1;
            est_next = f(est_next);
            dx = x_hunt(i,1)-est_next(1);
            dy = x_hunt(i,2)-est_next(2);
            step = sqrt(dx^2+dy^2);
            diff_dist = j*dist-step;

            angle = atan2(dy,dx);
            c_angle = x_hunt(i,3);
            turning = pi+ angle - x_hunt(i,3);

        end
        plot(est_next(1),est_next(2),'+');
        x_hunt(i,4) = min(step,dist);
        x_hunt(i,5)=turning;

        x_hunt_curr =  x_hunt(i,:);
        x_hunt_move = f(x_hunt_curr);
        x_hunt(i+1,:) = x_hunt_move;
    else
        
        dx = x_hunt(i,1)-est_next(1);
        dy = x_hunt(i,2)-est_next(2);
        step = sqrt(dx^2+dy^2);
        step = min(dist,step);
        
        x_hunt(i,4) = step;
        x_hunt(i,5) =0;
        
        x_hunt_curr =  x_hunt(i,:);
        x_hunt_move = f(x_hunt_curr);
        x_hunt(i+1,:) = x_hunt_move;
        plot(x_hunt_move(1),x_hunt_move(2),'.');
    end
    
    
end

