import RPi.GPIO as GPIO
import Adafruit_PCA9685


def angle_to_servo_data(angle):
    return 4096 * ((angle * 11) + 500) // 20000


class WheelsManager:
    def __init__(self, motor_sensitivity=10,
                 motor_lu_pin1=5, motor_lu_pin2=6, motor_lu_pwm_pin=22,
                 motor_ru_pin1=13, motor_ru_pin2=19, motor_ru_pwm_pin=26,
                 motor_ld_pin1=23, motor_ld_pin2=24, motor_ld_pwm_pin=25,
                 motor_rd_pin1=20, motor_rd_pin2=16, motor_rd_pwm_pin=12,
                 servo_channel=0, servo_range=12, servo_sensitivity=2):
        GPIO.setmode(GPIO.BCM)
        self.motor_speed = 0
        self.motor_sensitivity = motor_sensitivity
        self.servo_sensitivity = servo_sensitivity
        self.motor_lu_pin1 = motor_lu_pin1
        self.motor_lu_pin2 = motor_lu_pin2
        self.motor_lu_pwm_pin = motor_lu_pwm_pin
        self.motor_ru_pin1 = motor_ru_pin1
        self.motor_ru_pin2 = motor_ru_pin2
        self.motor_ru_pwm_pin = motor_ru_pwm_pin
        self.motor_ld_pin1 = motor_ld_pin1
        self.motor_ld_pin2 = motor_ld_pin2
        self.motor_ld_pwm_pin = motor_ld_pwm_pin
        self.motor_rd_pin1 = motor_rd_pin1
        self.motor_rd_pin2 = motor_rd_pin2
        self.motor_rd_pwm_pin = motor_rd_pwm_pin
        self.init_setup()
        self.motor_lu_pwm = GPIO.PWM(motor_lu_pwm_pin, 100)
        self.motor_ru_pwm = GPIO.PWM(motor_ru_pwm_pin, 100)
        self.motor_ld_pwm = GPIO.PWM(motor_ld_pwm_pin, 100)
        self.motor_rd_pwm = GPIO.PWM(motor_rd_pwm_pin, 100)
        self.init_pwm()
        self.servo = Adafruit_PCA9685.PCA9685()
        self.servo_channel = servo_channel
        self.servo_pos = 90
        self.servo_max = self.servo_pos + servo_range
        self.servo_min = self.servo_pos - servo_range
        self.init_servo()

    def init_setup(self):
        GPIO.setup(self.motor_lu_pin1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.motor_lu_pin2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.motor_ru_pin1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.motor_ru_pin2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.motor_ld_pin1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.motor_ld_pin2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.motor_rd_pin1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.motor_rd_pin2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.motor_lu_pwm_pin, GPIO.OUT)
        GPIO.setup(self.motor_ru_pwm_pin, GPIO.OUT)
        GPIO.setup(self.motor_ld_pwm_pin, GPIO.OUT)
        GPIO.setup(self.motor_rd_pwm_pin, GPIO.OUT)

    def init_pwm(self):
        self.motor_lu_pwm.start(0)
        self.motor_lu_pwm.ChangeDutyCycle(0)
        self.motor_ru_pwm.start(0)
        self.motor_ru_pwm.ChangeDutyCycle(0)
        self.motor_ld_pwm.start(0)
        self.motor_ld_pwm.ChangeDutyCycle(0)
        self.motor_rd_pwm.start(0)
        self.motor_rd_pwm.ChangeDutyCycle(0)

    def init_servo(self):
        self.servo.set_pwm_freq(50)
        self.servo.set_pwm(self.servo_channel, 0, angle_to_servo_data(self.servo_pos))

    def stop(self):
        GPIO.cleanup()

    def forward(self):
        GPIO.output(self.motor_lu_pin1, GPIO.HIGH)
        GPIO.output(self.motor_lu_pin2, GPIO.LOW)
        GPIO.output(self.motor_ru_pin1, GPIO.HIGH)
        GPIO.output(self.motor_ru_pin2, GPIO.LOW)
        GPIO.output(self.motor_ld_pin1, GPIO.HIGH)
        GPIO.output(self.motor_ld_pin2, GPIO.LOW)
        GPIO.output(self.motor_rd_pin1, GPIO.HIGH)
        GPIO.output(self.motor_rd_pin2, GPIO.LOW)

    def backward(self):
        GPIO.output(self.motor_lu_pin1, GPIO.LOW)
        GPIO.output(self.motor_lu_pin2, GPIO.HIGH)
        GPIO.output(self.motor_ru_pin1, GPIO.LOW)
        GPIO.output(self.motor_ru_pin2, GPIO.HIGH)
        GPIO.output(self.motor_ld_pin1, GPIO.LOW)
        GPIO.output(self.motor_ld_pin2, GPIO.HIGH)
        GPIO.output(self.motor_rd_pin1, GPIO.LOW)
        GPIO.output(self.motor_rd_pin2, GPIO.HIGH)

    def accelerate(self):
        if self.motor_speed + self.motor_sensitivity <= 100:
            self.motor_speed += self.motor_sensitivity
            self.change_speed()

    def decelerate(self):
        if self.motor_speed - self.motor_sensitivity >= -100:
            self.motor_speed -= self.motor_sensitivity
            self.change_speed()

    def left(self):
        if self.servo_pos - self.servo_sensitivity >= self.servo_min:
            self.servo_pos -= self.servo_sensitivity
            self.servo.set_pwm(self.servo_channel, 0, angle_to_servo_data(self.servo_pos))

    def right(self):
        if self.servo_pos + self.servo_sensitivity <= self.servo_max:
            self.servo_pos += self.servo_sensitivity
            self.servo.set_pwm(self.servo_channel, 0, angle_to_servo_data(self.servo_pos))

    def change_speed(self):
        print(self.motor_speed)
        speed = abs(self.motor_speed)
        self.motor_lu_pwm.ChangeDutyCycle(speed)
        self.motor_ru_pwm.ChangeDutyCycle(speed)
        self.motor_ld_pwm.ChangeDutyCycle(speed)
        self.motor_rd_pwm.ChangeDutyCycle(speed)
        if self.motor_speed > 0:
            self.forward()
        else:
            self.backward()
