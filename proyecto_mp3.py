# /// @file proyecto_mp3.py
# Proyecto en Python
# Marianne Escalante B72710
# Luis Diego Madrigal B94453
# Katherine Vargas B88198

'''
El presente codigo es el correspondiente a un reproductor mp3, en el cual se
colocaran y escucharan las canciones que el usuario tenga descargadas en su
maquina y las agregue al reproductor mp3.
El reproductor presenta una interfaz grafica de facil uso y entendimiento.
El menu se encuentra en la esquina superior izquierda del reproductor, en donde
se podran agregar y eliminar las canciones que se deseen escuchar.
Los botones se mostraran debajo de la caja que contiene el nombre de las
canciones subidas y listas para reproducir. Cada uno de estos botones tiene
una funcion especifica, como: pausar, reproducir, adelantar, retroceter o
detener la reproduccion de las canciones.
Debajo de los botones del reproductor se encontrara una barra de sonido, a la
cual cuando se le mueva de izquierda a derecha el sonido ira aumentando, si se
mueve de derecha a izquierda el sonido ira disminuyendo. Tambien, dependiendo
de la intensidad del sonido, las imagenes que lo representan ira cambiando.
'''

#Tener en cuenta que se debe de tener descargada la carpeta de las
#imagenes (tener cuidado con la ubicación de la misma).
#Así también, la dirección de las canciones descargadas.Cada usuario debe 
#cambiar el nombre de la carpeta donde se encuentren si fuera necesario.

# Se insertan las bibliotecas a usar.

from tkinter import *
from tkinter import filedialog
from ttkthemes import themed_tk as tk
import tkinter as tk
# from tkinter import ttk
import pygame
# import time
import tkinter.messagebox
# import os
# from mutagen.mp3 import MP3
from pygame import mixer
from tkinter import ACTIVE, END, ANCHOR, VERTICAL, RIGHT, Y, HORIZONTAL
from tkinter import Listbox, Frame, Menu, Scrollbar

# Este bloque se encarga de mostrar la interface del reproductor
window = tkinter.Tk()
window.title('Reproductor de musica')
window.geometry("1280x720")
window.config(background="gray20")

# El pygame mixer se activa
pygame.mixer.init()


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                        CAJAS Y MARGENES
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
frame1 = Frame(window)
scrollbar = Scrollbar(frame1, orient=VERTICAL)

'''
En el siguiente bloque, se creara la playlist box que tendra todas las
canciones que el usuario suba desde su directorio.
'''
# Esto es lo que se encarga de crear la playlist box.
ventana = Listbox(
                frame1, bg="snow3",
                fg="black", width=120,
                selectbackground="DarkSeaGreen4",
                selectforeground="white",
                bd=10,
                font="Candara",
                yscrollcommand=scrollbar.set
                )
ventana.pack(pady=10)
tk

scrollbar.config(command=ventana.yview)
scrollbar.pack(side=RIGHT, fill=Y)
frame1.pack()
# Se define el margen que poseera la ventana
margen_controles = Frame(window)
margen_controles.pack()

margen_controles_2 = Frame(window)
margen_controles_2.pack()

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    FUNCIONES PARA EL MENU PRINCIPAL
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def add_cancion():
    '''
    Esta funcion se encarga de agregar las canciones una por una, a como las
    vaya agregando el usuario.

    Esta funcion no posee parametros.
    '''
    # Le indica al usuario solo subir archivo en .mp3
    cancion = filedialog.askopenfilename(
        initialdir='/home/louisdieou/Downloads',
        title="Escoja una canción",
        filetypes=(("mp3 Files", "*.mp3"),))

    # Modifica la ventana para que muestre el nombre de la cancion
    cancion = cancion.replace("/home/louisdieou/Downloads/", "")
    cancion = cancion.replace(".mp3", "")

    # Cada que se añada una cancion esta se pone al final del reproductor
    ventana.insert(END, cancion)


def add_canciones():
    '''
    Esta funcion añade todas las canciones que el usuario quiera agregar.

    Esta funcion no posee parametros.
    '''
    #  Le indica al usuario solo subir archivo en .mp3
    canciones = filedialog.askopenfilenames(
                initialdir='/home/louisdieou/Downloads',
                title="Escoja una canción",
                filetypes=(("mp3 Files", "*.mp3"),))

    # Se crea un ciclo de lista de canciones y reemplaza la informacion
    for cancion in canciones:
        cancion = cancion.replace("/home/louisdieou/Downloads/", "")
        cancion = cancion.replace(".mp3", "")
        # Cada que se añada una cancion esta se pone al final del reproductor
        ventana.insert(END, cancion)


def eliminar_cancion():
    '''
    Esta funcion se encarga de eliminar la cancion que se seleccione.

    Esta funcion no posee parametros.
    '''
    ventana.delete(ANCHOR)
    pygame.mixer.music.stop()


def eliminar_todas_canciones():
    '''
    Esta funcion elimina todas las canciones presentes.

    Esta funcion no posee parametros.
    '''
    ventana.delete(0, END)
    pygame.mixer.music.stop()


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                        MENU PRINCIPAL
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

'''
Se creo el menu en donde se seleccionaran las canciones a añadir o eliminar
desde el directorio del usuario.
'''

# Se crea el menu
menubar = Menu(window)
window.config(menu=menubar)

menu_principal = Menu(menubar)
menubar.add_cascade(label="Menu principal", menu=menu_principal)

sub_menu_1 = Menu(menu_principal)
sub_menu_2 = Menu(menu_principal)

menu_principal.add_cascade(label="Añadir", menu=sub_menu_1)
menu_principal.add_cascade(label="Eliminar", menu=sub_menu_2)


# Se encarga de añadir una cancion
sub_menu_1.add_command(
                             label='Añadir una canción a la playlist',
                             command=add_cancion
                             )

# Se encarga de añadir varias canciones a la vez
sub_menu_1.add_command(
                        label='Añadir varias canciones a la playlist',
                        command=add_canciones
                        )

# Se encarga de eliminar una cancion
sub_menu_2.add_command(
                        label="Remover Una Canción Del Playlist",
                        command=eliminar_cancion
                        )

# Se encarga de eliminar varias canciones a la vez
sub_menu_2.add_command(
                        label="Remover Todas Las Canciones Del Playlist",
                        command=eliminar_todas_canciones
                        )

"""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                FUNCIONES BOTONES PLAY, STOP, PAUSE, NEXT, BACK
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# Esta variable se refiere a la global de pausa.
global pausado
pausado = False


def play():
    """
    Esta funcion recibe la direccion de la cancion que el usuario haya
    seleccionado y con pygame.mixer se reproduce el archivo de la cancion.

    Esta funcion no posee parametros.
    """
    # Se agarra el archivo .mp3 de la cancion seleccionada.
    cancion = ventana.get(ACTIVE)

    # Se cambia la direccion de la cancion y la reproduce pygame.mixer
    cancion = f'/home/louisdieou/Downloads/{cancion}.mp3'

    # Se cambia la direccion de la cancion y la reproduce pygame.mixer
    pygame.mixer.music.load(cancion)
    pygame.mixer.music.play(loops=0)


def detener():
    '''
    Esta funcion se encarga de recibir la direccion de la cancion que el
    usuario ha seleccionado y pygame.mixer lo detiene.

    Esta funcion no posee parametros.
    '''
    pygame.mixer.music.stop()
    ventana.selection_clear(ACTIVE)


def pausa(esta_pausado):
    '''
    Esta funcion recibe la variable mencionada anteriormente, la variable
    global determina si la cancion suena o esta en pausa.

    La variable presente es 'esta_pausando', la cual se refiere a que si se
    hace uso de ese boton, la cancion se detendra.
    '''
    global pausado
    pausado = esta_pausado

    if pausado is True:
        # Se reproduce
        pygame.mixer.music.unpause()
        pausado = False
    else:
        # Se pausa
        pygame.mixer.music.pause()
        pausado = True


def siguiente():
    '''
    Esta función reproduce la cancion siguiente en el playlist.

    Esta función no posee parametros.
    '''
    # Se situa sobre la cancion que suena actualmente
    siguiente = ventana.curselection()

    # La variable se corre a la siguiente cancion sumando uno
    siguiente = siguiente[0]+1

    # Agarra el titulo presente de la playlist
    cancion = ventana.get(siguiente)

    # El argumento de la cancion se modifica para que pueda ser reproducida
    cancion = f'/home/louisdieou/Downloads/{cancion}.mp3'

    # La direccion de la cancion se envia para que sea reproducida con exito
    pygame.mixer.music.load(cancion)
    pygame.mixer.music.play(loops=0)

    # Se le modifica la ubicacion a la barra de seleccion
    ventana.selection_clear(0, END)
    ventana.activate(siguiente)
    ventana.selection_set(siguiente, last=None)


def atras():
    '''
    Esta funcion se encarga de reproducir al cancion anterior a la que suena.

    Esta función no posee parametros.
    '''
    # Se situa sobre la cancion que suena actualmente
    previa = ventana.curselection()

    # La variable se corre a la cancion anterior restando uno
    previa = previa[0]-1

    # Agarra el titulo presente de la playlist
    cancion = ventana.get(previa)

    # La direccion de la cancion se envia para que sea reproducida con exito
    cancion = f'/home/louisdieou/Downloads/{cancion}.mp3'

    # Se le modifica la ubicacion a la barra de seleccion
    pygame.mixer.music.load(cancion)
    pygame.mixer.music.play(loops=0)

    # Se le modifica la ubicacion a la barra de seleccion
    ventana.selection_clear(0, END)
    ventana.activate(previa)
    ventana.selection_set(previa, last=None)


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                        FUNCIONES PARA EL VOLUMEN
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def update_volume(val):
    '''
    Modifica el volumen y las imagenes conforme se suba o baje el volumen de la
    cancion.

    Presenta un parametro, el cual es 'val'. Este se encarga de tomar el valor
    que tenga el volumen puesto por el usuario al momento de reproducir
    canciones.
    Conforme vaya aumentando este valor cambiara el volumen y las
    imagenes que lo representan tambien lo haran.
    '''
    global is_muted
    global volume
    volume = float(val) / 100
    mixer.music.set_volume(volume)
    if volume == 0:
        button_mute["image"] = img_button_vol_none
    elif volume < 0.34:
        is_muted = False
        button_mute["image"] = img_button_vol_low
        is_muted = False
    elif volume < 0.67:
        button_mute["image"] = img_button_vol_mid
        is_muted = False
    else:
        button_mute["image"] = img_button_vol_high
        is_muted = False


def toggle_mute():
    '''
    Esta funcion se encarga de guardar la informacion del volumen en caso de
    que este haya sido muteado. Por ejemplo, que si se muteo con un 50% del
    volumen, al momento de quitar el mute, el sonido volvera al 50%.

    Esta función no posee parametros.
    '''
    global is_muted
    global volume
    global volume_saved
    if is_muted:
        mixer.music.set_volume(volume_saved)
        volume_scale.set(int(volume_saved * 100))
        if volume < 0.34:
            button_mute["image"] = img_button_vol_low
        elif volume < 0.67:
            button_mute["image"] = img_button_vol_mid
        else:
            button_mute["image"] = img_button_vol_high
        is_muted = False
    else:
        volume_saved = volume
        mixer.music.set_volume(0)
        volume_scale.set(0)
        button_mute["image"] = img_button_vol_none
        is_muted = True


# De nuevo, se presentan las variables globales.

is_muted = False

try:
    with open("config.cfg", "r") as f:
        volume = float(f.read())
        mixer.music.set_volume(volume)
except:
    volume = 0.5  # Volumen al cual inicia el programa.
    volume_saved = 0.5  # Se guarda el volumen al cual estaba en caso de mutear


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                            BOTONES
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

'''
El siguiente bloque se encarga de subir las imagenes que tendran los
distintos botones para el reproductor musical.
'''

# Se enlistan los botones para el reproductor
img_button_back = tk.PhotoImage(file='./imagenes/back.png')
img_button_next = tk.PhotoImage(file='./imagenes/next.png')
img_button_play = tk.PhotoImage(file='./imagenes/play.png')
img_button_pausa = tk.PhotoImage(file='./imagenes/pause.png')
img_button_stop = tk.PhotoImage(file='./imagenes/stop.png')
img_button_vol_none = tk.PhotoImage(file="./imagenes/none.png")
img_button_vol_low = tk.PhotoImage(file="./imagenes/low.png")
img_button_vol_mid = tk.PhotoImage(file="./imagenes/mid.png")
img_button_vol_high = tk.PhotoImage(file="./imagenes/high.png")


'''
Ahora, a los botones del reproductor se le colocan las imagenes, su posicion
correspondiente y sus comandos con pygame.
'''

# Se enlistan los controles para el reproductor
button_back = tk.Button(margen_controles, image=img_button_back,
                        borderwidth=0, command=atras)
button_next = tk.Button(margen_controles, image=img_button_next,
                        borderwidth=0, command=siguiente)
button_play = tk.Button(margen_controles, image=img_button_play,
                        borderwidth=0, command=play)
button_pausa = tk.Button(margen_controles, image=img_button_pausa,
                         borderwidth=0, command=lambda: pausa(pausado))
button_stop = tk.Button(margen_controles, image=img_button_stop,
                        borderwidth=0, command=detener)
button_mute = tk.Button(margen_controles_2, image=img_button_vol_mid,
                        borderwidth=0,  command=toggle_mute)


volume_scale = tk.Scale(
                margen_controles_2,
                from_=0, to=100,
                orient=HORIZONTAL,
                command=update_volume
                )
volume_scale.set(volume*100)  # valores por defecto ya se definieron
mixer.music.set_volume(volume)  # lo mismo aqui


# Ubicaciones para los botones
button_back.grid(row=0, column=0, padx=10)
button_play.grid(row=0, column=1, padx=10)
button_pausa.grid(row=0, column=2, padx=10)
button_stop.grid(row=0, column=3, padx=10)
button_next.grid(row=0, column=4, padx=10)
button_mute.grid(row=0, column=5, padx=10)
volume_scale.grid(row=0, column=6, padx=10)


# Finalmente, el entorno de tkinter se cierra.
window.mainloop()
