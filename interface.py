import tkinter as tk
import _tkinter
from tkinter import*
import logging
from tkinter import filedialog
from collections import namedtuple

#create a struct/tuple that can be used to store the name and coordinates of containers we want to offload
ContainersInfo = namedtuple('ContainersInfo', ['name', 'coordinates'])

logging.basicConfig(filename='logfile.txt', level=logging.INFO, format='%(asctime)s %(message)s')

#create a Container for each ContainersInfo in the grid
#Each sqaure will have the row, column, name and ability to toogle the button on and off stored 
#UNUSED spaces will not be toogleable 
#NAN spaces will not be toogleable and will appear black 
class Container:
    def __init__(self, master, row, col, name):
        self.master = master
        self.row = row
        self.col = col
        self.selected = False
        self.name= name
        if self.name == "NAN":
            self.button = tk.Button(master, text=self.name, width=10, height=5, state=tk.DISABLED, bg="black")
        elif self.name == "UNUSED":
            self.button = tk.Button(master, text=self.name, width=10, height=5, state=tk.DISABLED)
        else:
            self.button = tk.Button(master, text=self.name, width=10, height=5, command=self.toggle)
        self.button.grid(row=row, column=col)
        

    def toggle(self):
        self.selected = not self.selected
        if self.selected:
            self.button.configure(bg="red", relief=tk.SUNKEN)
        else:
            self.button.configure(bg="white", relief=tk.RAISED)

    def get_coordinates(self):
        max_row = 8
        return (8-self.row +1, self.col)
    
    def get_name(self):
        return self.name


def popup_logfile():
    popup_window = tk.Toplevel()
    popup_window.title("Writing to logfile")
    popup_window.geometry("800x100")

    entry_var = tk.StringVar()  

    entry_field = tk.Entry(popup_window, textvariable=entry_var, width = 100, highlightcolor="black",highlightthickness=1)
    entry_field.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    ok_button = tk.Button(popup_window, text="OK", command=lambda: ok_action(entry_var.get(), popup_window))
    ok_button.grid(row=1, column=0, padx=5, pady=5)

    cancel_button = tk.Button(popup_window, text="Cancel", command=popup_window.destroy)
    cancel_button.grid(row=1, column=1, padx=5, pady=5)

    popup_window.grid_columnconfigure(0, weight=1)
    popup_window.grid_columnconfigure(1, weight=1)

def select_file():
    filename = filedialog.askopenfilename()
    if filename:
        offloading_popup(filename)

#This function is called once a file/manifest is selected 
#This will generate the grid of containers which the user can select the containers hat need to be offloaded
def offloading_popup(filename):
    top = tk.Toplevel(main)
    top.title("Grid")
    frame = tk.Frame(top)
    frame.grid(sticky=tk.N + tk.S + tk.E + tk.W)

    containers = []

    with open(filename, "r") as f:
        max_row = sum(1 for _ in f)  # Get the number of rows in the file
        max_row = 8
        f.seek(0)
        for line in f:
            line = line.strip()
            if line:
                parts = line.split(", ")
                row, col = map(int, parts[0].strip()[1:-1].split(","))
                name = parts[2].strip()
                container = Container(frame, max_row - row +1, col, name)
                containers.append(container)

    ok_button = tk.Button(frame, text="OK", command=lambda: send_container_info(containers))
    ok_button.grid(row=len(containers) + 1, column=0, padx=5, pady=5)

    cancel_button = tk.Button(frame, text="Cancel", command=top.destroy)
    cancel_button.grid(row=len(containers) + 1, column=1, padx=5, pady=5)

    top.grid_columnconfigure(0, weight=1)
    top.grid_columnconfigure(1, weight=1)

#placeholder function that will acquire and send the coordintes and name of a container to the function that calculates
#selected_containers[x] will gives the array that holds the tuples that contains the name and coordinates
#elected_containers[x][0] will give the name of the container
#selected_containers[x][1] will give the x,y coordinates of the container
def send_container_info(containers):
    selected_containers = [ContainersInfo(container.get_name(), container.get_coordinates()) for container in containers if container.selected]
    print(selected_containers)

def ok_action(entry_value, popup_window):
    logging.info({entry_value})
    popup_window.destroy()

#TODO clean up the main GUI where the user can select onload/offload and writing to logfile

HEIGHT = 1000
WIDTH = 1500

main = tk.Tk()

#placeholder name
greeting = tk.Label(text="Crane Operation Optimizer")
greeting.grid()

#creates the window size
canvas = tk.Canvas(main, height = HEIGHT, width=WIDTH)
canvas.grid()

#button that initiates onload/offload beginning with a file select
loading_popup_button = tk.Button(main, text="onload/offload", command=select_file)
loading_popup_button.grid()

#button that will popup a window where the user can write to the log file
popup_button = tk.Button(main, text="logfile write", command=popup_logfile)
popup_button.grid()


main.mainloop()