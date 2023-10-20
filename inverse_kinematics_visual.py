import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

joint_angles = [0.2, 0.3, 0.5, 0.7, 0.9, 1.2]
link_lengths = [1, 2, 3, 1, 2, 1]

destination_point = [3, 2, 1]
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

# Add a legend
ax.legend()

# Show the plot
plt.show()
