import tkinter as tk
from tkinter import PhotoImage, Canvas
import ctypes
import pyautogui
import random
import os
import sys

class Gatito:
    
    def __init__(self, scene, x = 0, y = 0):
        
        dir_path = os.path.dirname(os.path.realpath(__file__))

        # Construye la ruta al archivo de imagen
        image_path = os.path.join(dir_path, 'assets', 'gatito.png')
        dust_path = os.path.join(dir_path, 'assets', 'dust.png')
        
        print(image_path)
        print(dust_path)
        
        self.scene = scene
        self.image = PhotoImage(file = image_path)
        self.image = self.image.subsample(16)
        self.imageRef = scene.canvas.create_image(x, y, image=self.image)
        self.image_dust = PhotoImage(file = dust_path)
        self.image_dust = self.image_dust.subsample(8)
        self.dust_status = False

    def update(self):
        x, y = pyautogui.position()
        cat_x, cat_y = self.scene.canvas.coords(self.imageRef)
        dist = (abs(x - cat_x) + abs(y - cat_y))
        
        # explosion de polvo
        if self.dust_status:
            self.scene.canvas.move(
                self.imageRef, 
                random.choice([-100, 100]),
                random.choice([-100, 100]),
            )
            self.scene.canvas.itemconfig(self.imageRef, image=self.image)
            
            if len(self.scene.gatitos) <= 100:
                self.scene.new_gatito(
                    random.randint(0, self.scene.screen_width),
                    random.randint(0, self.scene.screen_height)
                )
            self.dust_status = False
        
        elif dist < 5:
            self.scene.canvas.itemconfig(self.imageRef, image=self.image_dust)
            self.dust_status = True

        else:
            num = random.choice((1, 2))
            self.scene.canvas.move(
                self.imageRef, 
                num if x > cat_x else -num,
                num if y > cat_y else -num
            )


class Scene:
    
    def __init__(self, window: tk.Tk):
        self.screen_width = window.winfo_screenwidth()
        self.screen_height = window.winfo_screenheight()
        self.canvas = Canvas(
            window, 
            width=self.screen_width, 
            height=self.screen_height,
            highlightthickness=0,
            bg='white'
        )
        self.canvas.pack()
        self.gatitos = list()

    def update(self):
        
        for gatito in self.gatitos:
            gatito.update()

    def new_gatito(self, x, y):
        gatito = Gatito(self)
        self.canvas.move(gatito.imageRef, x, y)
        self.gatitos.append(gatito)



class Game:
    
    def __init__(self):
        self.window = self.create_window()
        self.apply_click_through(self.window)
        self.scene = Scene(self.window)

    def update(self):
        self.scene.update()
        self.window.after(10, self.update)

    def create_window(self):
        
        # crear la ventana
        window = tk.Tk()
        
        # decirle que la ventana sea la primera en pantalla completa
        window.wm_attributes('-topmost', True)
        window.wm_attributes('-fullscreen', True)
        window.overrideredirect(True)
        
        # hacer la ventana transparente
        window.attributes('-transparentcolor', 'white')
        window.config(bg='white')
        
        return window

    def apply_click_through(self, window):
        
        # constantes de la API de Windows
        WS_EX_TRANSPARENT = 0x00000020
        WS_EX_LAYERED = 0x00080000
        GWL_EXSTYLE = -20
        
        # obtener id de la ventana
        hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
        
        # obtener estilos de la ventana
        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        
        # aplicar transparencias y capas a los estilos
        style = style | WS_EX_LAYERED | WS_EX_TRANSPARENT
        
        # aplicar los estilos a la ventana
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
        

    def start(self):
        self.update()
        self.window.mainloop()


game = Game()
game.scene.new_gatito(100, 100)
game.start()