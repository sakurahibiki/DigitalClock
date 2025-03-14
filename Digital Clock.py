import customtkinter
from tkinter import *
from datetime import datetime
from PIL import Image
from threading import Thread, Lock

mutex = Lock()


SUN_IMAGE = "./images/sun.png"
MOON_IMAGE = "./images/moon.png"
CLOCK_ICON = "./images/clock-icon.ico"

class Clock:
    def __init__(self, hours = 12, minutes=0, seconds = 0, meridiem = "AM"):
        self.meridiem = meridiem
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.root = customtkinter.CTk() #init
        self.root.iconbitmap(CLOCK_ICON)
        self.my_sun_image = customtkinter.CTkImage(light_image=Image.open(SUN_IMAGE), dark_image=Image.open(SUN_IMAGE), size=(25,25))  #init
        self.my_moon_image = customtkinter.CTkImage(light_image=Image.open(MOON_IMAGE), dark_image=Image.open(MOON_IMAGE), size=(23,23)) #init
        self.frame_clicked = True
        self.dst_clicked = True
        self.main_window()


    def update_clock(self):
        with mutex:
            # time.sleep(1)
            self.seconds += 1
            if self.seconds % 60 == 0:
                if self.seconds != 0:
                    self.seconds = 0
                    self.minutes += 1
            if self.minutes % 60 == 0:
                if self.minutes != 0:
                    self.minutes = 0
                    self.seconds = 0
                    self.hours += 1
            if self.hours % 12 == 0 and self.minutes % 60 == 0 and self.seconds % 60 == 0:
                self.meridiem = "PM" if self.meridiem == "AM" else "AM"
            if self.hours % 13 == 0:
                self.minutes = 0
                self.seconds = 0
                self.hours = 1
            
            curr_time = f"{self.hours}:{self.minutes:02}:{self.seconds:02} {self.meridiem}"
            return curr_time
           
    def main_window(self):
        customtkinter.set_appearance_mode("light") #main window
        customtkinter.set_default_color_theme("blue") #main window
        self.root.title("Digital Clock") #main window
        self.root.geometry("360x200") #main window
        self.root.resizable(width=False,height=False) #main window
        self.frame = customtkinter.CTkFrame(self.root, width=200, height=125, corner_radius=10, fg_color=("white", "black")) #main window
        self.frame.pack(pady=20) #main window
        self.label = customtkinter.CTkLabel(self.frame, font=("arial", 48, "bold"), fg_color=("white", "black")) #main window
        self.label.pack(padx=10,pady=20) #main window
        self.label.bind("<Button-1>", self.on_frame_click)
        self.switch_value = customtkinter.StringVar(value="on") #main window
        self.switch = customtkinter.CTkSwitch(master=self.root, command=self.set_mode, text="", variable=self.switch_value, onvalue="on", offvalue="off") #main window
        self.switch.pack(padx=155, pady=10) #main window
        self.button = customtkinter.CTkButton(master = self.root, command=self.daylight_savings, text="DST")
        self.button.pack(padx=170, pady=10)
        self.sun_image = customtkinter.CTkLabel(master=self.root, image=self.my_sun_image, text="") #main window
        self.sun_image.place(x=198, y=143) #main window
        self.moon_image = customtkinter.CTkLabel(master=self.root, image=self.my_moon_image, text="") #main window
        self.moon_image.place(x=130, y=143) #main window

    def set_mode(self): #self method
        if self.switch_value.get() == "on":
            customtkinter.set_appearance_mode("light")
        else:
            customtkinter.set_appearance_mode("dark")

    def run_clock(self): #self method
        current_time = self.update_clock()
        self.label.configure(text=current_time)
        self.root.after(1000, self.run_clock)
    
    def run(self):
        #run
        self.run_clock()
        self.root.mainloop()
    
    def on_frame_click(self, event):
        if self.frame_clicked == True: 
            self.hours -= 12
            self.frame_clicked = False
        else:
            self.hours += 12
            self.frame_clicked = True
    
    def daylight_savings(self, event):
        if self.dst_clicked == True:
            self.hours += 1
            self.dst_clicked = False
        else:
            self.hours += 1
            self.dst_clicked = True







       


#main function
if __name__ == "__main__":
    current_time = str(datetime.now().time())
    time_string = current_time.split('.')[0]
    time_parts = time_string.split(':')
    hours = int(time_parts[0])
    minutes = int(time_parts[1])
    seconds = int(time_parts[2])
    meridiem = str(datetime.now().strftime("%p"))
    clock = Clock(hours, minutes, seconds, meridiem)
    clock.run()




    