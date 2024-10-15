from gpiozero import Motor
from time import sleep

motor_a = Motor(forward=5, backward=16)
motor_b = Motor(forward=6, backward=21)

def run_motors_forward(speed, duration):
    motor_a.forward(speed)
    motor_b.forward(speed)
    sleep(duration)
    motor_a.stop()
    motor_b.stop()

def run_motors_backward(speed, duration):
    motor_a.backward(speed)
    motor_b.backward(speed)
    sleep(duration)
    motor_a.stop()
    motor_b.stop()

def stop_motors():
    motor_a.stop()
    motor_b.stop()

try:
    print("Running motors forward...")
    run_motors_forward(0.5, 2)
    
    print("Running motors backward...")
    run_motors_backward(0.5, 2)
    
except KeyboardInterrupt:
    print("Motor control interrupted.")

finally:
    stop_motors()
    print("Motors stopped.")
