# Chess_Move_Detection
This script uses computer vision to determine a move that was made by the human given two inputs, a top down image of the board before and after the move was made. 

# Hand_Detection
This script uses the mediaPipe package to extract the before and after images from the video web stream.

# Chess_Engine
This script uses the detected move from the Chess_Move_Detection script and uses the Stockfish engine to determine the robot's next move. It then converts the robot's move to Cartesian Coordinates.

# Inverse_Kinematics
This script takes in the Cartesian coordinates of the robot's latest move and calcultes the joint angles that are required for the robot to make the move.

# Matlab_Communication
This script is used to setup socket connections between different ports and enable communication between different softwares

# Robot_Control
This script uses the calculated joint angles and moves the robot using GPIO to make the chess move possible

# Logging_Module
This script creates a logger that can be used to output messages to an excel file. Useful for debugging and troubleshooting

# How to Run
To run the system, run the Chess_Move_Detection script. Once the webcam has turned on, press enter when ready to take a picture of the empty board. From there, if the chess board was found, you can select a skill level of the Stockfish chess engine, and setup the socket
connections between the the laptop, MATLAB and the Raspberry Pi. Finally, once all of these conditions have been met, you can setup the pieces on the board and press enter when finished to start the system. Once the initial setup has been completed, all the user has to do 
is play chess normally and the system will do the rest. 

