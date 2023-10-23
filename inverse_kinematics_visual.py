import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math

def find_joint_angles(destination_point, link_lengths):
    x = destination_point[0]
    y = destination_point[1]
    z = destination_point[2]

    theta1 = math.atan(x/y)
    r = math.sqrt(pow(x,2)+ pow(y,2))
    r_squared = pow(r, 2)
    s = z - link_lengths[0]
    s_squared = pow(s, 2)

    theta3 = math.acos((r_squared + s_squared - pow(link_lengths[1], 2) - pow(link_lengths[2], 2))/(r_squared + s_squared))
    theta2 = math.asin(((link_lengths[1] + link_lengths[2]*math.cos(theta3))*s - link_lengths[2]*math.sin(theta3)*r)/(2*link_lengths[1]*link_lengths[2]))
    theta4 = -1*math.asin(math.sin(theta1)*math.cos(theta2-theta3)/math.cos(theta1))
    theta5 = math.acos(math.sin(theta1))

    joint_angles = [theta1, theta2, theta3, theta4, theta5]
    return joint_angles
    
def plot_graph(joint_angles, link_lengths, destination_point):
    origin = np.array([0, 0, 0])
    joint_positions = [origin]

    # Calculate joint positions based on the joint angles and link lengths
    for i in range(len(joint_angles)): # Adjust the math to calculate 3D point based off your robot
        angle = joint_angles[i]
        length = link_lengths[i]
        x = joint_positions[-1][0] + length * np.cos(angle)
        y = joint_positions[-1][1] + length * np.sin(angle)
        z = joint_positions[-1][2] + length * np.sin(angle)  # Adjust for 3D
        joint_positions.append(np.array([x, y, z]))

    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the links of the robot arm
    for i in range(1, len(joint_positions)):
        x_values = [joint_positions[i - 1][0], joint_positions[i][0]]
        y_values = [joint_positions[i - 1][1], joint_positions[i][1]]
        z_values = [joint_positions[i - 1][2], joint_positions[i][2]]
        ax.plot(x_values, y_values, z_values, 'b-o')

    # Plot the comparison point and origin
    ax.scatter(origin[0], origin[1], origin[2], c='green', marker='o', label='Origin')
    ax.scatter(destination_point[0], destination_point[1], destination_point[2], c='red', marker='o', label='Comparison Point')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Robot Arm Configuration in 3D')
    ax.legend()
    plt.show()

def main():
    link_lengths = [5, 10, 12.5, 8, 3]
    destination_point = [10, 10, 10]

    joint_angles = find_joint_angles(destination_point, link_lengths)

    plot_graph(joint_angles, link_lengths, destination_point)

if __name__ == "__main__":
    main()