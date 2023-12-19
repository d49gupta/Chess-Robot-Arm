import RPi.GPIO as GPIO
import time
import socket
import threading
import ast
import matlab_communication

def setup():
    joints = [2, 3, 4, 14, 15, 18]  
    GPIO.setmode(GPIO.BCM)
    for joint in joints:
        GPIO.setup(joint, GPIO.OUT)
    pwms = [GPIO.PWM(joint, 50) for joint in joints]

    return pwms

def set_joint_angle(pwm, angle):
    duty_cycle = (angle / 18) + 2  # Convert angle to duty cycle (2 to 12)
    pwm.ChangeDutyCycle(duty_cycle)

def servo_thread(pwm, angle, sleepTime):
    set_joint_angle(pwm, angle)
    time.sleep(sleepTime) 

def stop_robot():
    print("Script has ended")
    for pwm in pwms:
        pwm.stop()
    # GPIO.cleanup()
    if client_socket:
        client_socket.close()

def main():
    global pwms, client_socket
    pwms = setup()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('192.168.1.144', 12346)

    try:
        for pwm in pwms:
            pwm.start(0)

        client_socket.connect(server_address)
        print(f'Connected to {server_address}')

        while True:
            joint_angles = matlab_communication.receive_message(client_socket)
            print(joint_angles)
            if joint_angles == 'exit':
                break
            else:
                joint_angles = ast.literal_eval(joint_angles)
                threads = []
                for index, joint_angle in enumerate(joint_angles):
                    if joint_angle < 0:
                        joint_angle += 180

                    thread = threading.Thread(target=servo_thread, args=(pwms[index], joint_angle, 10))
                    threads.append(thread)
                    thread.start()
                for thread in threads:
                    thread.join()
                
                message = 'done'
                matlab_communication.send_message(client_socket, message)
    finally:
        stop_robot()

if __name__ == "__main__":
    main()