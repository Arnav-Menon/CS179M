from tkinter import *


class Container:
    def __init__(self, master, row, column, name):
        self.master = master
        self.row = row
        self.column = column
        self.name = name
        self.selected = False
        self.color = 'black' if self.name == 'NAN' else 'white'
        self.rect = self.master.create_rectangle(self.column*50, self.row*50, (self.column+1)*50, (self.row+1)*50, fill=self.color)

    def select(self):
        self.selected = True
        self.master.itemconfig(self.rect, fill='red')

    def deselect(self):
        self.selected = False
        self.color = 'black' if self.name == 'NAN' else 'white'
        self.master.itemconfig(self.rect, fill=self.color)

def animate(containers, paths, current_path, index):
    tempPath = paths[current_path]
    current_container = containers[tempPath[index][0]][tempPath[index][1]]
    current_container.select()
    root.after(1000, current_container.deselect)
    index = (index + 1) % len(tempPath)
    if index == 0:
        animate_button_text = animate_button["text"]
        if animate_button_text == "Stop":
            # animation_id = 
            root.after(1000, animate, containers, paths, current_path, index)
    else:
        # animation_id = 
        root.after(1000, animate, containers, paths, current_path, index)
    # next_button.config(state=DISABLED)
    
    # Store the animation ID in a global variable so that it can be cancelled later
    # return animation_id

def start_animation():
    global animation_id, animation_running
    animation_running = False
    if not animation_running:
        animate_button.config(text='Stop', command=stop_animation)
        animation_running = True
        animation_id = animate(containers, paths, current_path, index)

def stop_animation():
    global animation_id, animation_running
    animate_button.config(text='Animate', command=start_animation)
    # print("Before cancelling animation_id:", animation_id)
    # root.after_cancel(animation_id)
    animation_running = False
    # print("After cancelling animation_id:", animation_id)

def next_animation():
    global current_path, animation_running
    if not animation_running:
        current_path = (current_path + 1) % len(paths)
        stop_animation()
        start_animation()


filename = "ShipCase4.txt"

root = Tk()
root.title("Grid Animation")

canvas = Canvas(root, width=1000, height=600, bg='white')
canvas.pack()

with open(filename, "r") as f:
    max_row = 8
    containers = [[] for _ in range(max_row)]
    for line in f:
        line = line.strip()
        if line:
            parts = line.split(", ")
            row, col = map(int, parts[0].strip()[1:-1].split(","))
            name = parts[2].strip()
            container = Container(canvas, max_row - row, col, name)
            containers[max_row - row].append(container)


paths = [[(1,0), (0,1), (0,2), (1,2), (2,2), (2,1), (2,0), (1,0)],
         [(3,3), (3,4), (3,5), (4,5), (5,5), (5,4), (5,3), (4,3)],
         [(0,1), (0,2), (0,3), (1,3)]]
max_row = 7
paths = [[(max_row - row, col) for row, col in path] for path in paths]
print(paths)

current_path = 0
index = 0
animation_id = None

animate_button = Button(root, text='Animate', command=start_animation)
animate_button.pack()

next_button = Button(root, text='Next', command=next_animation)
next_button.pack()


root.mainloop()