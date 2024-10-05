function gas_mode () {
    if (pins.digitalReadPin(DigitalPin.P1) == 0) {
        music.ringTone(131)
        basic.pause(200)
        music.stopAllSounds()
        basic.pause(1000)
        gas = 0
        I2C_LCD1602.clear()
    }
}
function auto_LED () {
    if (pins.digitalReadPin(DigitalPin.P15) == 1) {
        pins.digitalWritePin(DigitalPin.P16, 1)
    } else {
        pins.digitalWritePin(DigitalPin.P16, 0)
    }
    serial.writeValue("PIR signal", pins.digitalReadPin(DigitalPin.P15))
    basic.pause(500)
}
input.onButtonPressed(Button.A, function () {
    passwd_enter = "" + passwd_enter + "."
    serial.writeString(passwd_enter)
    serial.writeLine("")
    I2C_LCD1602.ShowString(passwd_enter, 0, 1)
})
function fan () {
    if (Temp >= 30) {
        pins.analogWritePin(AnalogPin.P12, 500)
        pins.analogWritePin(AnalogPin.P13, 1023)
        strip.showColor(neopixel.colors(NeoPixelColors.Black))
    } else {
        pins.analogWritePin(AnalogPin.P12, 0)
        pins.analogWritePin(AnalogPin.P13, 0)
        strip.showColor(neopixel.colors(NeoPixelColors.White))
    }
}
input.onButtonPressed(Button.AB, function () {
    I2C_LCD1602.clear()
    if (passwd_enter == password) {
        basic.showLeds(`
            . . # . .
            . # . # .
            . . . # .
            # # # # #
            # # # # #
            `)
        I2C_LCD1602.ShowString("Successful", 0, 0)
        I2C_LCD1602.ShowString("Welcome home", 0, 1)
        basic.pause(1000)
        I2C_LCD1602.clear()
        pins.servoWritePin(AnalogPin.P8, 180)
        strip.setBrightness(100)
        strip.showColor(neopixel.colors(NeoPixelColors.White))
        strip.show()
        Auth = 1
    } else {
        I2C_LCD1602.ShowString("Wrong password", 0, 0)
        I2C_LCD1602.ShowString("Enter again", 0, 1)
        basic.showLeds(`
            # . . . #
            . # . # .
            . . # . .
            . # . # .
            # . . . #
            `)
        passwd_enter = ""
        basic.pause(1000)
        I2C_LCD1602.clear()
        basic.clearScreen()
        I2C_LCD1602.ShowString("Enter password", 0, 0)
    }
})
function AutoMode () {
    auto_window()
    gas_mode()
    auto_LED()
    fan()
}
input.onButtonPressed(Button.B, function () {
    passwd_enter = "" + passwd_enter + "-"
    serial.writeString(passwd_enter)
    serial.writeLine("")
    I2C_LCD1602.ShowString(passwd_enter, 0, 1)
})
function auto_window () {
    water_val = pins.analogReadPin(AnalogReadWritePin.P0)
    if (water_val > 190) {
        pins.servoWritePin(AnalogPin.P9, 0)
        basic.pause(2000)
        I2C_LCD1602.clear()
    } else {
        pins.servoWritePin(AnalogPin.P9, 100)
    }
}
input.onLogoEvent(TouchButtonEvent.Pressed, function () {
    Auth = 0
    passwd_enter = ""
    pins.servoWritePin(AnalogPin.P8, 0)
    basic.pause(1000)
    basic.showLeds(`
        . . # . .
        . # # # .
        . # . # .
        # # # # #
        # # # # #
        `)
    strip.clear()
    strip.show()
    I2C_LCD1602.ShowString("Goodbye", 0, 0)
    basic.pause(1000)
    I2C_LCD1602.clear()
    control.reset()
})
let Humidity = 0
let water_val = 0
let Temp = 0
let strip: neopixel.Strip = null
let passwd_enter = ""
let password = ""
let gas = 0
let Auth = 0
basic.pause(1000)
serial.redirectToUSB()
Auth = 0
gas = 0
I2C_LCD1602.LcdInit(39)
I2C_LCD1602.clear()
basic.pause(500)
dht11_dht22.queryData(
DHTtype.DHT11,
DigitalPin.P2,
true,
false,
false
)
pins.servoWritePin(AnalogPin.P9, 100)
pins.digitalWritePin(DigitalPin.P16, 0)
password = ".-.-"
passwd_enter = ""
strip = neopixel.create(DigitalPin.P14, 4, NeoPixelMode.RGB)
strip.clear()
strip.show()
for (let index = 0; index < 1; index++) {
    I2C_LCD1602.ShowString("Enter password", 0, 0)
}
music.ringTone(988)
basic.pause(100)
music.stopAllSounds()
basic.showLeds(`
    . . # . .
    . # # # .
    . # . # .
    # # # # #
    # # # # #
    `)
basic.forever(function () {
    if (Auth == 1) {
        Temp = dht11_dht22.readData(dataType.temperature)
        Humidity = dht11_dht22.readData(dataType.humidity)
        serial.writeValue("Temp", Temp)
        serial.writeValue("Humidity", Humidity)
        I2C_LCD1602.ShowString("Teplota", 0, 0)
        I2C_LCD1602.ShowNumber(Math.round(Temp), 8, 0)
        I2C_LCD1602.ShowString("Vlhkost", 0, 1)
        I2C_LCD1602.ShowNumber(Humidity, 8, 1)
        I2C_LCD1602.ShowString("%", 10, 1)
        basic.pause(1000)
        I2C_LCD1602.clear()
    }
})
basic.forever(function () {
    if (Auth == 1) {
        AutoMode()
    }
})
