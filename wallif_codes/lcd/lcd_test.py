import I2C_LCD_driver
import time

lcdi2c = I2C_LCD_driver.lcd()

lcdi2c.lcd_display_string("EXEMPLO", 1,0)
lcdi2c.lcd_display_string("LCD", 2, 5)

while True:
    lcdi2c.backlight(0)
    time.sleep(1)
    lcdi2c.backlight(1)
    time.sleep(2)
