try
    t = tcpclient('localhost', 12345);  
    fopen(t);
    disp('Connection Successful')
    while true
        message = receive_message(t);
        if ~isempty(message) && strcmp(message, 'exit')
            disp('Script has ended')
            delete(t)
            break
        end
        if numel(message) > 0
            data_struct = jsondecode(message);
            x_value = data_struct.x;
            y_value = data_struct.y;
            z_value = data_struct.z;
            joint_angles = inverse_kinematics(x_value, y_value, z_value);
            json_str = jsonencode(joint_angles);
            write(t, json_str);
        end
    end
catch
    disp('Connection Failed')
end

function configSoln_degrees = inverse_kinematics(x, y, z)
    dhparams = [0   	pi/2	5  	    0;
                10	    0       0       0
                12.5	0	    0	    0;
                8   	pi/2	0	    pi/2;
                0       0	    3   	 0];
    
    % empty container defining the strcuture and kinematics of the robot
    robot = rigidBodyTree; 
    
    % First link (revolute joint) and its associated dh parameters (first
    % row) used to specify the transformation matrix of the joint (relationship
    % between joint angle and its parent/child links. 
    body1 = rigidBody('body1');
    jnt1 = rigidBodyJoint('jnt1','revolute');
    setFixedTransform(jnt1,dhparams(1,:),'dh');
    
    % Attach joint to body and body to base of robot
    body1.Joint = jnt1;
    addBody(robot,body1,'base')
    
    % Repeat for all other links/joints
    body2 = rigidBody('body2');
    jnt2 = rigidBodyJoint('jnt2','revolute');
    body3 = rigidBody('body3');
    jnt3 = rigidBodyJoint('jnt3','revolute');
    body4 = rigidBody('body4');
    jnt4 = rigidBodyJoint('jnt4','revolute');
    body5 = rigidBody('body5');
    jnt5 = rigidBodyJoint('jnt5','revolute');
    
    setFixedTransform(jnt2,dhparams(2,:),'dh');
    setFixedTransform(jnt3,dhparams(3,:),'dh');
    setFixedTransform(jnt4,dhparams(4,:),'dh');
    setFixedTransform(jnt5,dhparams(5,:),'dh');
    
    body2.Joint = jnt2;
    body3.Joint = jnt3;
    body4.Joint = jnt4;
    body5.Joint = jnt5;
    
    addBody(robot,body2,'body1')
    addBody(robot,body3,'body2')
    addBody(robot,body4,'body3')
    addBody(robot,body5,'body4')
    
    % Initializes robot angles at random (provides initial guess)
    randConfig = robot.randomConfiguration;
    user_tform = [1 0 0 x; 0 1 0 y; 0 0 -1 z; 0 0 0 1];
    tform = getTransform(robot,randConfig,"body5","body1");
%     showdetails(robot)
    
    % Calculate the Inverse Kinematics
    ik = inverseKinematics("RigidBodyTree",robot);
    weights = [0.25 0.25 0.25 1 1 1];
    initialguess = homeConfiguration(robot);
    
    % Inverse kinematics solved for body6
    [configSoln,solnInfo] = ik("body5",user_tform,weights,initialguess);
    configSoln_degrees = rad2deg([configSoln.JointPosition]);
    
    % Display on Graph
%     show(robot,configSoln);
%     hold on 
%     plot3(x, y, z, 'r.', 'MarkerSize', 10)
%     xlabel('X-axis');
%     ylabel('Y-axis');
%     zlabel('Z-axis');
%     title('Robot Arm with Desired Point');
%     grid on
    
    % Display joint angles
%     disp("Joint Angles:");
%     disp(configSoln_degrees);
end

function received_message = receive_message(t)
    if t.BytesAvailable > 0
        data_received = fread(t, t.BytesAvailable);
        received_message = char(data_received');
        disp(['Received message from Python: ' received_message])
    else
        received_message = ''; 
    end
end