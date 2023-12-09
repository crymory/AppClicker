import pyautogui as pt
import tkinter as tk
from tkinter import ttk
from threading import Thread
from time import sleep
import keyboard

class ClickerApp:
    def __init__(self, master, target_images, clicker_speed, start_hotkey, stop_hotkey):
        self.master = master
        self.master.title("Auto Clicker")
        #self.master.attributes('-toolwindow', True)  # Set tool window attributes
        self.running = False
        self.clicker_speed = tk.StringVar(value=str(clicker_speed))
        self.start_hotkey = tk.StringVar(value=start_hotkey)
        self.stop_hotkey = tk.StringVar(value=stop_hotkey)

        self.clicker = None
        self.clicker_thread = None

        self.start_button = ttk.Button(self.master, text="Старт", command=self.start_clicker)
        self.start_button.grid(row=0, column=0, padx=10, pady=10)

        self.stop_button = ttk.Button(self.master, text="Стоп", command=self.stop_clicker, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.master, text="Скорость кликов (в кликах в секунду):").grid(row=1, column=0, columnspan=2)
        self.speed_entry = ttk.Entry(self.master, textvariable=self.clicker_speed)
        self.speed_entry.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        ttk.Label(self.master, text="Горячая клавиша Старт:").grid(row=3, column=0, columnspan=2)
        self.start_hotkey_entry = ttk.Entry(self.master, textvariable=self.start_hotkey)
        self.start_hotkey_entry.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        ttk.Label(self.master, text="Горячая клавиша Паузы:").grid(row=5, column=0, columnspan=2)
        self.stop_hotkey_entry = ttk.Entry(self.master, textvariable=self.stop_hotkey)
        self.stop_hotkey_entry.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

        # Добавление текстового статуса
        self.status_label = ttk.Label(self.master, text="Статус: Остановлен", foreground="red")
        self.status_label.grid(row=7, column=0, columnspan=2, pady=5)


    def start_clicker(self):
        if not self.running:
            self.running = True
            self.start_button["state"] = tk.DISABLED
            self.stop_button["state"] = tk.NORMAL
            self.status_label["text"] = "Статус: Запущен"
            self.status_label["foreground"] = "green"


            clicker_speed = float(self.clicker_speed.get())
            start_hotkey = self.start_hotkey.get()
            stop_hotkey = self.stop_hotkey.get()

            self.clicker = Clicker(target_images, clicker_speed, start_hotkey, stop_hotkey, self)
            
            self.clicker_thread = Thread(target=self.clicker.run)
            self.clicker_thread.start()

    def stop_clicker(self):
        if self.running:
            self.running = False
            self.start_button["state"] = tk.NORMAL
            self.stop_button["state"] = tk.DISABLED
            self.status_label["text"] = "Статус: Остановлен"
            self.status_label["foreground"] = "red"

            
            if self.clicker_thread:
                self.clicker.stop()
                self.clicker_thread.join()

class Clicker:
    def __init__(self, target_images, speed, start_hotkey, stop_hotkey, app):
        self.target_images = target_images
        self.speed = speed
        self.paused = False
        self.stopped = False
        self.start_hotkey = start_hotkey
        self.stop_hotkey = stop_hotkey
        pt.FAILSAFE = True
        self.app = app

    def toggle_pause(self):
        self.paused = not self.paused

    def nav_to_image(self, target_png):
            print(f"     ____        __ _  __")
            print(f"(   / __ )____  / /| |/ /")
            print(f"  / __  / __ \/ __/   / ")
            print(f" / /_/ / /_/ / /_/   | ")
            print(f"/_____/\____/\__/_/|_|     v1.1")
        try:
            position = pt.locateOnScreen(target_png, confidence=0.8)
            if position:
                #print(f"Image {target_png} found at position: {position}")
                image_center_x = position[0] + position[2] // 2
                image_center_y = position[1] + position[3] // 2

                pt.click(x=image_center_x, y=image_center_y, button='left')
                return True

            else:
                #print(f"Image {target_png} not found.")
                return False

        except Exception as e:
            #print(f'Error occurred while searching for image: {e}')
            return False

    def run(self):
        sleep(2)

        while not self.stopped:
            for target_png in self.target_images:
                if keyboard.is_pressed(self.stop_hotkey):
                    self.paused = True
                    self.app.status_label["text"] = "Статус: На паузе"
                    self.app.status_label["foreground"] = "orange"
                    print("Script paused. Press Start hotkey to resume.")
                    while self.paused:
                        if keyboard.is_pressed(self.start_hotkey):
                            self.paused = False
                            self.app.status_label["text"] = "Статус: Запущен"
                            self.app.status_label["foreground"] = "green"
                            print("Script resumed.")
                            break
                        sleep(0.1)

                if self.paused:
                    continue

                if self.nav_to_image(target_png):
                    sleep(self.speed)

    def stop(self):
        self.stopped = True

if __name__ == '__main__':
    target_images = [
        "resources/grey.png", "resources/grey2.png", "resources/grey3.png",
        "resources/greyBlue.png", "resources/greyBlue2.png", "resources/greyBlue3.png",
        "resources/greyGrey.png", "resources/greyGrey2.png", "resources/greyGrey3.png",
        "resources/violetGrey.png", "resources/violetGrey2.png", "resources/violetGrey3.png"
    ]

    root = tk.Tk()
    app = ClickerApp(root, target_images, clicker_speed=0.0001, start_hotkey="F9", stop_hotkey="F10")
    root.mainloop()
