import RPi.GPIO as GPIO
import time
import threading

# Define the GPIO pins to which the servos are connected
joints = [2, 3, 4, 14, 15, 18]  # Example GPIO pins

# Set up GPIO
GPIO.setmode(GPIO.BCM)
for joint in joints:
    GPIO.setup(joint, GPIO.OUT)

# Create PWM objects for all joints
pwms = [GPIO.PWM(joint, 50) for joint in joints]

# Function to set the servo angle (0 to 180 degrees)
def set_joint_angle(pwm, angle):
    duty_cycle = (angle / 18) + 2  # Convert angle to duty cycle (2 to 12)
    pwm.ChangeDutyCycle(duty_cycle)

def servo_thread(pwm, angle):
    set_joint_angle(pwm, angle)
    time.sleep(10)  # Keep the servo in this position for 10 seconds

try:
    # Start PWM for all joints
    for pwm in pwms:
        pwm.start(0)

    joint_angles = [0.0011, 26.8692, -79.7284, 76.4, 179.8238]

    threads = []

    for index, joint_angle in enumerate(joint_angles):
        thread = threading.Thread(target=servo_thread, args=(pwms[index], joint_angle))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

finally:
    # Stop PWM and clean up GPIO
    for pwm in pwms:
        pwm.stop()
    GPIO.cleanup()
