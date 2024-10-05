def gas_mode():
    global gas
    if pins.digital_read_pin(DigitalPin.P1) == 0:
        I2C_LCD1602.show_string("Danger", 0, 0)
        music.ring_tone(131)
        basic.pause(200)
        music.stop_all_sounds()
        basic.pause(1000)
        gas = 0
        I2C_LCD1602.clear()
    else:
        pass
def auto_LED():
    if FanRun == 0:
        if pins.digital_read_pin(DigitalPin.P15) == 1:
            pins.digital_write_pin(DigitalPin.P16, 1)
        else:
            pins.digital_write_pin(DigitalPin.P16, 0)
        serial.write_value("PIR signal", pins.digital_read_pin(DigitalPin.P15))
        basic.pause(500)
    else:
        pass
def fan_switch():
    if Temp >= 30:
        fan_spin()

def on_logo_long_pressed():
    fan_spin()
input.on_logo_event(TouchButtonEvent.LONG_PRESSED, on_logo_long_pressed)

def on_button_pressed_a():
    global passwd_enter
    passwd_enter = "" + passwd_enter + "."
    serial.write_string(passwd_enter)
    serial.write_line("")
    I2C_LCD1602.show_string(passwd_enter, 0, 1)
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_button_pressed_ab():
    global Auth, passwd_enter
    I2C_LCD1602.clear()
    if passwd_enter == password:
        basic.show_leds("""
            . . # . .
            . # . # .
            . . . # .
            # # # # #
            # # # # #
            """)
        I2C_LCD1602.show_string("Successful", 0, 0)
        I2C_LCD1602.show_string("Welcome home", 0, 1)
        basic.pause(1000)
        I2C_LCD1602.clear()
        pins.servo_write_pin(AnalogPin.P8, 180)
        strip.set_brightness(100)
        strip.show_color(neopixel.colors(NeoPixelColors.WHITE))
        strip.show()
        Auth = 1
    else:
        I2C_LCD1602.show_string("Wrong password", 0, 0)
        I2C_LCD1602.show_string("Enter again", 0, 1)
        basic.show_leds("""
            # . . . #
            . # . # .
            . . # . .
            . # . # .
            # . . . #
            """)
        passwd_enter = ""
        basic.pause(1000)
        I2C_LCD1602.clear()
        basic.clear_screen()
        I2C_LCD1602.show_string("Enter password", 0, 0)
input.on_button_pressed(Button.AB, on_button_pressed_ab)

def AutoMode():
    auto_window()
    auto_LED()
    gas_mode()
    fan_switch()

def on_button_pressed_b():
    global passwd_enter
    passwd_enter = "" + passwd_enter + "-"
    serial.write_string(passwd_enter)
    serial.write_line("")
    I2C_LCD1602.show_string(passwd_enter, 0, 1)
input.on_button_pressed(Button.B, on_button_pressed_b)

def auto_window():
    global water_val
    water_val = pins.analog_read_pin(AnalogPin.P0)
    if water_val > 190:
        pins.servo_write_pin(AnalogPin.P9, 0)
        I2C_LCD1602.show_string("rainin", 0, 0)
        basic.pause(2000)
        I2C_LCD1602.clear()
    else:
        pins.servo_write_pin(AnalogPin.P9, 100)
def fan_spin():
    global FanRun
    FanRun = 1
    if FanRun == 1:
        pins.analog_write_pin(AnalogPin.P12, 500)
        pins.analog_write_pin(AnalogPin.P13, 1023)
        strip.show_color(neopixel.colors(NeoPixelColors.BLACK))
        basic.pause(2000)
    else:
        FanRun = 0
        pins.analog_write_pin(AnalogPin.P12, 0)
        pins.analog_write_pin(AnalogPin.P13, 0)
        strip.show_color(neopixel.colors(NeoPixelColors.WHITE))

def on_logo_pressed():
    global Auth, passwd_enter
    Auth = 0
    passwd_enter = ""
    pins.servo_write_pin(AnalogPin.P8, 0)
    basic.pause(1000)
    basic.show_leds("""
        . . # . .
        . # # # .
        . # . # .
        # # # # #
        # # # # #
        """)
    strip.clear()
    strip.show()
    I2C_LCD1602.show_string("Goodbye", 0, 0)
    basic.pause(1000)
    I2C_LCD1602.clear()
    control.reset()
input.on_logo_event(TouchButtonEvent.PRESSED, on_logo_pressed)

Humidity = 0
water_val = 0
Temp = 0
FanRun = 0
strip: neopixel.Strip = None
passwd_enter = ""
password = ""
gas = 0
Auth = 0
basic.pause(1000)
serial.redirect_to_usb()
Auth = 0
gas = 0
I2C_LCD1602.lcd_init(39)
I2C_LCD1602.clear()
basic.pause(500)
dht11_dht22.query_data(DHTtype.DHT11, DigitalPin.P2, True, False, False)
pins.servo_write_pin(AnalogPin.P9, 100)
pins.digital_write_pin(DigitalPin.P16, 0)
password = ".-.-"
passwd_enter = ""
strip = neopixel.create(DigitalPin.P14, 4, NeoPixelMode.RGB)
strip.clear()
strip.show()
for index in range(1):
    I2C_LCD1602.show_string("Enter password", 0, 0)
music.ring_tone(988)
basic.pause(100)
music.stop_all_sounds()
basic.show_leds("""
    . . # . .
    . # # # .
    . # . # .
    # # # # #
    # # # # #
    """)

def on_forever():
    global Temp, Humidity
    if Auth == 1:
        if FanRun == 0:
            Temp = dht11_dht22.read_data(dataType.TEMPERATURE)
            Humidity = dht11_dht22.read_data(dataType.HUMIDITY)
            serial.write_value("Temp", Temp)
            serial.write_value("Humidity", Humidity)
            I2C_LCD1602.show_string("Temp", 0, 1)
            I2C_LCD1602.show_number(Math.round(Temp), 5, 1)
            I2C_LCD1602.show_string("HMD", 9, 1)
            I2C_LCD1602.show_number(Humidity, 13, 1)
            basic.pause(2000)
            I2C_LCD1602.clear()
        else:
            pass
basic.forever(on_forever)

def on_forever2():
    if Auth == 1:
        AutoMode()
basic.forever(on_forever2)
