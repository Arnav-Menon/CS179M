from tkinter import *

animation_running = False
current_path = 0
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

def animate(containers, paths, current_path, index,animate_button,popup):
    tempPath = paths[current_path]
    current_container = containers[tempPath[index][0]][tempPath[index][1]]
    current_container.select()
    popup.after(1000, current_container.deselect)
    index = (index + 1) % len(tempPath)
    if index == 0:
        animate_button_text = animate_button["text"]
        if animate_button_text == "Stop":
            # animation_id = 
            popup.after(1000, animate, containers, paths, current_path, index,animate_button, popup)
    else:
        # animation_id = 
        popup.after(1000, animate, containers, paths, current_path, index,animate_button, popup)
    # next_button.config(state=DISABLED)
    
    # Store the animation ID in a global variable so that it can be cancelled later
    # return animation_id

def start_animation(current_path,index,animate_button,containers,paths,popup):
    global animation_id, animation_running
    animation_running = False
    if not animation_running:
        animate_button.config(text='Stop', command=lambda: stop_animation(current_path,index,animate_button,containers,paths,popup))
        animation_running = True
        animation_id = animate(containers, paths, current_path, index,animate_button,popup)

def stop_animation(current_path,index,animate_button,containers,paths,popup):
    global animation_id, animation_running
    animate_button.config(text='Animate', command=lambda: start_animation(current_path, index, animate_button, containers, paths, popup))
    animation_running = False

def next_animation( index, animate_button, containers, paths, popup):
    global current_path,animation_running
    if not animation_running:
        current_path = (current_path + 1) % len(paths)
        stop_animation(current_path, index, animate_button, containers, paths, popup)
        start_animation(current_path, index, animate_button, containers, paths, popup)


def show_animation():
    filename = "ShipCase4.txt"

    popup = Toplevel()
    popup.title("Grid Animation")

    canvas = Canvas(popup, width=1000, height=600, bg='white')
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

    # global current_path
    index = 0
    animation_id = None

    animate_button = Button(popup, text='Animate')
    animate_button.pack()
    # animate_button = Button(popup, text='Animate', command=start_animation(current_path,index,animate_button,containers,paths,popup))
    # animate_button.config(command=lambda: start_animation(current_path, index, animate_button, containers, paths, popup))
    animate_button.config(command=lambda current_path=current_path, index=index, animate_button=animate_button, containers=containers, paths=paths, popup=popup: start_animation(current_path, index, animate_button, containers, paths, popup))

    next_button = Button(popup, text='Next', command=lambda: next_animation( index, animate_button, containers, paths, popup))
    next_button.pack()

    popup.mainloop()