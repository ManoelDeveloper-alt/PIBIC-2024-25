import I2C_LCD_driver
import time

lcdi2c = I2C_LCD_driver.lcd() # instancia o lcd
lcdi2c.lcd_display_string("EXEMPLO", 1, 0) #linha 1 coluna 1
lcdi2c.lcd_display_string("LCD", 2, 5) #linha 2 coluna 6

try:
	while True:
		lcdi2c.backlight(0) # apaga luz de fundo
		time.sleep(1)
		lcdi2c.backlight(1) # acende luz de fundo
		time.sleep(2)
except KeyboardInterrupt:
	lcdi2c.lcd_display_string("                ", 1, 0) # apaga o conteudo da linha 1
	lcdi2c.lcd_display_string("                ", 2, 0) # apaga o conteudo da linha 2
	lcdi2c.backlight(0)
