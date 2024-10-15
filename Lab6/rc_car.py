from gpiozero import Motor, Button, RotaryEncoder
from time import sleep
from signal import pause

motor_a = Motor(forward=5, backward=6)
motor_b = Motor(forward=16, backward=21)

encoder_a = RotaryEncoder(5, 6)
encoder_b = RotaryEncoder(16, 21)

stop_button = Button(17)

target_speed = 60
proportional_gain = 0.05

def emergency_stop():
    motor_a.stop()
    motor_b.stop()
    print("Emergency Stop Activated")

stop_button.when_pressed = emergency_stop

def control_motor_speed():
    while True:
        pulses_a = encoder_a.steps
        speed_a = pulses_a * (60 / 700)

        speed_error_a = target_speed - speed_a
        motor_a_speed_adjustment = proportional_gain * speed_error_a

        motor_a.forward(min(max(motor_a_speed_adjustment, 0), 1))

        pulses_b = encoder_b.steps
        speed_b = pulses_b * (60 / 700)
        speed_error_b = target_speed - speed_b
        motor_b_speed_adjustment = proportional_gain * speed_error_b
        motor_b.forward(min(max(motor_b_speed_adjustment, 0), 1))

        sleep(0.1)

try:
    print("Starting motor control...")
    control_motor_speed()

except KeyboardInterrupt:
    print("Control interrupted, stopping motors.")
    
finally:
    motor_a.stop()
    motor_b.stop()
    print("Motors stopped.")
