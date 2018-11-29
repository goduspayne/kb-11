import os
import pygame
from pygame.locals import *
import mainfile
import pygameMenu
from pygameMenu.locals import *


# Constants and global variables
pygameMenu.__author__ = "Python Childs"
pygameMenu.__version__ = "Helloween Spirit"
pygameMenu.__email__ = "PythonChildCompany@gmail.com"
ABOUT = ['Project {0}'.format(pygameMenu.__version__),
            'Author: {0}'.format(pygameMenu.__author__),
            PYGAMEMENU_TEXT_NEWLINE,
            'Email: {0}'.format(pygameMenu.__email__)]
COLOR_BLUE = (12, 12, 200)
COLOR_BACKGROUND = [128, 0, 128]
COLOR_WHITE = (255, 255, 255)
FPS = 60
H_SIZE = 600  # Height of window size
HELP = ['Press ESC to enable/disable Menu',
        'Press ENTER to access a Sub-Menu or use an option',
        'Press UP/DOWN to move through Menu']

W_SIZE = 800  # Width of window size

# -----------------------------------------------------------------------------
# Init pygame
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Write help message on console
for m in HELP:
    print(m)

# Create window
surface = pygame.display.set_mode((W_SIZE, H_SIZE))
pygame.display.set_caption('PygameMenu example')



def mainmenu_background():
    surface.fill((140, 0, 40))

# Start menu
start_menu = pygameMenu.Menu(surface,
                                 dopause=False,
                                 font=pygameMenu.fonts.FONT_NEVIS,
                                 menu_alpha=85,
                                 menu_color=(0, 0, 0),  # Background color
                                 menu_color_title=(0, 0, 0),
                                 menu_height=int(H_SIZE / 2),
                                 menu_width=600,
                                 onclose=PYGAME_MENU_RESET,  # If this menu closes (press ESC) back to main
                                 title='Start the game',
                                 title_offsety=5,  # Adds 5px to title vertical position
                                 window_height=H_SIZE,
                                 window_width=W_SIZE
                                 )



# -----------------------------------------------------------------------------
# Help menu
help_menu = pygameMenu.TextMenu(surface,
                                    dopause=False,
                                    font=pygameMenu.fonts.FONT_FRANCHISE,
                                    menu_color=(30, 50, 107),  # Background color
                                    menu_color_title=(120, 45, 30),
                                    onclose=PYGAME_MENU_DISABLE_CLOSE,  # Pressing ESC button does nothing
                                    title='Help',
                                    window_height=H_SIZE,
                                    window_width=W_SIZE
                                    )
help_menu.add_option('Return to Menu', PYGAME_MENU_BACK)
for m in HELP:
    help_menu.add_line(m)

# -----------------------------------------------------------------------------
# About menu
about_menu = pygameMenu.TextMenu(surface,
                                     dopause=False,
                                     font=pygameMenu.fonts.FONT_NEVIS,
                                     font_size_title=30,
                                     font_title=pygameMenu.fonts.FONT_8BIT,
                                     menu_color_title=COLOR_BLUE,
                                     onclose=PYGAME_MENU_DISABLE_CLOSE,  # Disable menu close (ESC button)
                                     text_fontsize=20,
                                     title='About',
                                     window_height=H_SIZE,
                                     window_width=W_SIZE
                                     )
about_menu.add_option('Return to Menu', PYGAME_MENU_BACK)
for m in ABOUT:
    about_menu.add_line(m)
about_menu.add_line(PYGAMEMENU_TEXT_NEWLINE)

# -----------------------------------------------------------------------------
# Main menu, pauses execution of the application
menu = pygameMenu.Menu(surface,
                           bgfun=mainmenu_background,
                           #enabled=False,
                           font=pygameMenu.fonts.FONT_NEVIS,
                           menu_alpha=90,
                           onclose=PYGAME_MENU_CLOSE,
                           title='Main Menu',
                           title_offsety=5,
                           window_height=H_SIZE,
                           window_width=W_SIZE
                           )
menu.add_option(start_menu.get_title(),start_menu)  # Add start submenu
menu.add_option(help_menu.get_title(), help_menu) # Add help submenu
menu.add_option(about_menu.get_title(), about_menu)  # Add about submenu
menu.add_option('Exit', PYGAME_MENU_EXIT)  # Add exit function

# -----------------------------------------------------------------------------
# Main loop
while True:



    # Paint background
    surface.fill(COLOR_BACKGROUND)

    # Application events
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                menu.enable()



    # Execute main from principal menu if is enabled
    menu.mainloop(events)

    # Flip surface
    pygame.display.flip()

