from gpiozero import Motor, RotaryEncoder, MCP3008
from time import sleep

motor_a = Motor(forward=18, backward=19)
motor_b = Motor(forward=20, backward=21)
encoder_a = RotaryEncoder(16, 20)
encoder_b = RotaryEncoder(23, 24)
adc = MCP3008(channel=0)  # Assuming voltage divider is connected to MCP3008

target_speed = 60
Kp = 1.2
Ki = 0.4
Kd = 0.1

prev_error_a = 0
integral_a = 0
prev_error_b = 0
integral_b = 0

def read_voltage():
    return adc.value * 3.3 * 9 / 3.3  # Adjust for voltage divider circuit

def pid_control(encoder, target, prev_error, integral):
    pulses = encoder.steps
    speed = pulses * (60 / 700)
    error = target - speed
    integral += error
    derivative = error - prev_error
    control_signal = Kp * error + Ki * integral + Kd * derivative
    prev_error = error
    return control_signal, prev_error, integral

while True:
    battery_voltage = read_voltage()
    if battery_voltage < 7.0:
        target_speed = 50  # Adjust target speed based on low battery voltage

    control_signal_a, prev_error_a, integral_a = pid_control(encoder_a, target_speed, prev_error_a, integral_a)
    control_signal_b, prev_error_b, integral_b = pid_control(encoder_b, target_speed, prev_error_b, integral_b)

    motor_a.forward(min(max(control_signal_a, 0), 1))
    motor_b.forward(min(max(control_signal_b, 0), 1))

    sleep(0.1)
from gpiozero import Motor, RotaryEncoder, MCP3008
from time import sleep

motor_a = Motor(forward=5, backward=6)
motor_b = Motor(forward=16, backward=21)
encoder_a = RotaryEncoder(5, 6)
encoder_b = RotaryEncoder(16, 21)
adc = MCP3008(channel=0)  # Assuming voltage divider is connected to MCP3008

target_speed = 60
Kp = 1.2
Ki = 0.4
Kd = 0.1

prev_error_a = 0
integral_a = 0
prev_error_b = 0
integral_b = 0

def read_voltage():
    return adc.value * 3.3 * 9 / 3.3  

def pid_control(encoder, target, prev_error, integral):
    pulses = encoder.steps
    speed = pulses * (60 / 700)
    error = target - speed
    integral += error
    derivative = error - prev_error
    control_signal = Kp * error + Ki * integral + Kd * derivative
    prev_error = error
    return control_signal, prev_error, integral

while True:
    battery_voltage = read_voltage()
    if battery_voltage < 7.0:
        target_speed = 50  

    control_signal_a, prev_error_a, integral_a = pid_control(encoder_a, target_speed, prev_error_a, integral_a)
    control_signal_b, prev_error_b, integral_b = pid_control(encoder_b, target_speed, prev_error_b, integral_b)

    motor_a.forward(min(max(control_signal_a, 0), 1))
    motor_b.forward(min(max(control_signal_b, 0), 1))

    sleep(0.1)
