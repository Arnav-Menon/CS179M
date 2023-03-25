import tkinter as tk
from tkinter import font
from tkinter import*
import logging
from tkinter import filedialog
from collections import namedtuple
from animation import show_animation
import tkinter.font as tkFont
from tkinter import messagebox
from main import calculate

#create a struct/tuple that can be used to store the name and coordinates of containers we want to offload
ContainersInfo = namedtuple('ContainersInfo', ['name', 'coordinates'])

with open("logfiles.txt", "r") as f:
    lines = f.readlines()
    logfile = lines[-1]
    logfile =logfile.rstrip()

logging.basicConfig(filename=logfile, level=logging.INFO, format='%(asctime)s %(message)s')

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

def select_load_file():
    filename = filedialog.askopenfilename()
    if filename:
        offloading_popup(filename)

def select_balance_file():
    filename = filedialog.askopenfilename()
    if filename:
        balance_container(filename)

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

    ok_button = tk.Button(frame, text="OK", command=lambda: loading_ok_button(containers,filename,top))
    ok_button.grid(row=len(containers) + 1, column=0, padx=5, pady=5)

    cancel_button = tk.Button(frame, text="Cancel", command=top.destroy)
    cancel_button.grid(row=len(containers) + 1, column=1, padx=5, pady=5)

    top.grid_columnconfigure(0, weight=1)
    top.grid_columnconfigure(1, weight=1)

#placeholder function that will acquire and send the coordintes and name of a container to the function that calculates
#selected_containers[x] will gives the array that holds the tuples that contains the name and coordinates
#elected_containers[x][0] will give the name of the container
#selected_containers[x][1] will give the x,y coordinates of the container
def send_container_info(containers,filename):
    selected_containers = [ContainersInfo(container.get_name(), container.get_coordinates()) for container in containers if container.selected]
    print(selected_containers) # this will be a function call to calculate the optimal path for now we hardcode path
    paths = [[[0,8],[0,7],[0,6],[0,5],[0,4],[1,4],[1,3],[2,3],[2,2],[3,2],[4,2],[5,2],[5,1],[5,0]],
             [[2,0],[2,1],[2,2],[2,3],[2,4],[3,4],[3,3],[3,2],[3,1],[3,0]],
             [[5,0],[5,1],[5,2],[4,2],[3,2],[2,2],[2,3],[1,3],[1,4],[0,4],[0,5],[0,6],[0,7],[0,8]],
             [[8,0],[8,1],[8,2],[7,2]]]
    #TODO wait for function to return paths and then call show_animation
    containerNames = ["Rat","Dog","Corn","FLY"]
    show_animation(paths,filename,containerNames)

def ok_action(entry_value, popup_window):
    logging.info({entry_value})
    popup_window.destroy()

def loading_ok_button(containers,filename,top):
    top.destroy()
    send_container_info(containers,filename)

def balance_container(filename):
    # print("Call balance function")
    # paths = [[[0,8],[0,7],[0,6],[0,5],[0,4],[1,4],[1,3],[2,3],[2,2],[3,2],[4,2],[5,2],[5,1],[5,0]],
    #          [[2,0],[2,1],[2,2],[2,3],[2,4],[3,4],[3,3],[3,2],[3,1],[3,0]],
    #          [[5,0],[5,1],[5,2],[4,2],[3,2],[2,2],[2,3],[1,3],[1,4],[0,4],[0,5],[0,6],[0,7],[0,8]],
    #          [[8,0],[8,1],[8,2],[7,2]]]
    paths,containerNames = calculate(filename)
    # containerNames = ["Rat","Dog","Corn","FLY"]
    show_animation(paths,filename,containerNames)

def newLogFile(log_popuo,logfileYear):
    logfile = "logfile" + logfileYear.get() + ".txt"
    root_logger = logging.getLogger()
    handler = logging.FileHandler(logfile)
    root_logger.addHandler(handler)
    formatter = logging.Formatter('%(asctime)s %(message)s')
    handler.setFormatter(formatter)
    print(logfile)
    with open('logfiles.txt', 'a') as f:
        f.write(logfile)
    log_popuo.destroy()

HEIGHT = 900
WIDTH = 1300

main = tk.Tk()
main.geometry("1350x900")
# set the background color of the main window
main.configure(bg='gray30')


bg_canvas = tk.Canvas(main, width=5000, height=5000, bg='gray30')
bg_canvas.place(relx=0, rely=0, anchor=tk.NW)

bg_image = tk.PhotoImage(file="crane.png")
bg_image_resized = bg_image.zoom(2)
bg_canvas.create_image(0, 0, anchor=tk.NW, image=bg_image_resized)

apr_font = tkFont.Font(family="Comic Sans MS", size=30, weight= "bold")
# create a label for the title
title_label = tk.Label(main, text="Crane Operation Optimizer", font=apr_font, bg='gray30',fg='lightcyan3')
title_label.pack(pady=(47, 0))


# button that initiates onload/offload beginning with a file select
loading_popup_button = tk.Button(main, text="onload/offload", font=("Arial Bold", 15), command=select_load_file, bg='white',width= 35, height =10)
loading_popup_button.pack(side=tk.LEFT, padx=5, pady=5, expand=True)

# button that initiates balance
balance_button = tk.Button(main, text="balance", font=("Arial Bold", 15), command=select_balance_file, bg='white',width= 35, height =10)
balance_button.pack(side=tk.LEFT, padx=5, pady=5, expand=True)

# button that will popup a window where the user can write to the log file
popup_button = tk.Button(main, text="logfile write", font=("Arial Bold", 15),command=popup_logfile, bg='white',width= 35, height =10)
popup_button.pack(side=tk.LEFT, padx=5, pady=5, expand=True)


response = messagebox.askyesno("New Logfile", "Do you want to start a new logfile?")

if response:
    log_popuo = Toplevel()
    logfileYear = tk.StringVar() 
    title_label = tk.Label(log_popuo, text="The log file has the logical year appended to its name, What year do you want the log file?")
    title_label.pack(pady=(47, 0))
    logfileYear_field = tk.Entry(log_popuo, textvariable=logfileYear, width = 100, highlightcolor="black",highlightthickness=1)
    logfileYear_field.pack()
    ok = tk.Button(log_popuo, text="OK", command=lambda: newLogFile(log_popuo,logfileYear) )
    ok.pack()

    cancel = tk.Button(log_popuo, text="Cancel", command=log_popuo.destroy)
    cancel.pack()
   

main.mainloop()
