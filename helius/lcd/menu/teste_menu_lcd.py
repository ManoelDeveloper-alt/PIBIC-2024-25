import I2C_LCD_driver
import smbus
import curses

lcdi2c = I2C_LCD_driver.lcd()
lcdi2c.backlight(1)

opcoes = ["Opcao 1", "Opcao 2", "Opcao 3", "Opcao 4"]

def clear_lcd():
	lcdi2c.lcd_display_string("                ",1,0)
	lcdi2c.lcd_display_string("                ",2,0)

def upmenu(indice):
    clear_lcd()
    p = 1
    next = 1
    if indice==len(opcoes)-1:
        p = 2
        next = -1
    lcdi2c.lcd_display_string("> "+str(indice)+"-"+opcoes[indice], p, 0)
    lcdi2c.lcd_display_string(str(indice+next)+"-"+opcoes[indice+next], p+next, 0)

def menu(stdscr):
    curses.curs_set(0)  # Esconde o cursor
    indice = 0

    while True:
        tecla = stdscr.getch()

        # Processa a tecla pressionada
        if tecla == curses.KEY_UP and indice > 0:
            indice-=1
            upmenu(indice)
        elif tecla == curses.KEY_DOWN and indice < len(opcoes) - 1:
            indice+=1
            upmenu(indice)
        elif tecla == 10:  # Enter pressionado
            curses.napms(1000)  # Espera 1 segundo
            break

    clear_lcd()
    lcdi2c.lcd_display_string("Selecionada:", 1, 0)
    lcdi2c.lcd_display_string(opcoes[indice], 2, 0)
    curses.napms(2000)
    clear_lcd()
    lcdi2c.backlight(0)

try:
	upmenu(0)
	curses.wrapper(menu)

except KeyboardInterrupt:
	clear_lcd()
	lcdi2c.backlight(0)
