from tkinter import *

animation_running = False
current_path = 0

#intitalizes each grid for the animation
class Container:
    def __init__(self, master, row, column, name):
        self.master = master
        self.row = row
        self.column = column
        self.name = name
        self.selected = False
        self.is_start = False
        self.is_end = False
        self.color = 'black' if self.name == 'NAN' else 'white'
        self.rect = self.master.create_rectangle(self.column*50, self.row*50, (self.column+1)*50, (self.row+1)*50, fill=self.color)
        self.start_text_id = None  # save the ID of the start text
        self.end_text_id = None  # save the ID of the end text
        
        

    def select(self):
        self.selected = True
        self.master.itemconfig(self.rect, fill='red')

    def deselect(self):
        self.selected = False
        self.color = 'black' if self.name == 'NAN' else 'white'
        self.master.itemconfig(self.rect, fill=self.color)

    def select_start(self, column, row):
        self.is_start = True
        if self.start_text_id is not None:
               self.master.delete(self.start_text_id)  # delete the old start text
        self.start_text_id = self.master.create_text((column*50 + 25), (row*50 + 25), text="Start")
    
    def deselect_start(self, column, row):
        if self.is_start:
            self.is_start = False
            self.master.delete(self.start_text_id)  # delete the start text
            self.start_text_id = None  # set the ID to None

    def select_end(self, column, row):
        self.is_end = True
        if self.end_text_id is not None:
            self.master.delete(self.end_text_id)  # delete the old end text
        self.end_text_id = self.master.create_text((column*50 + 25), (row*50 + 25), text="End")

    def deselect_end(self, column, row):
        if self.is_end:
            self.is_end = False
            self.master.delete(self.end_text_id)  # delete the end text
            self.end_text_id = None  # set the ID to None

#Animates the path that the operator should follow
#creates a start and end block
def animate(containers, paths, current_path, index,animate_button,popup):
    tempPath = paths[current_path]

    current_container = containers[tempPath[index][0]][tempPath[index][1]]
    current_container.select()
    
    startColumn = tempPath[0][1]
    startRow = tempPath[0][0]

    endColumn = tempPath[-1][1]
    endRow = tempPath[-1][0]

    startContainer = containers[tempPath[0][0]][tempPath[0][1]]
    endContainer = containers[tempPath[-1][0]][tempPath[-1][1]]
  
    startContainer.select_start(startColumn+1,startRow)
    endContainer.select_end(endColumn+1,endRow)

    popup.after(1000, current_container.deselect)
    index = (index + 1) % len(tempPath)
    if index == 0:
        animate_button_text = animate_button["text"]
        if animate_button_text == "Stop":
            popup.after(1000, animate, containers, paths, current_path, index,animate_button, popup)
    else:
        popup.after(1000, animate, containers, paths, current_path, index,animate_button, popup)

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

#button functionality that moves onto to the next move
#deletes old start and end text
#updates name of container being moved
#updates what move number it is
def next_animation( index, animate_button, containers, paths, popup, current_path_label, container_label):
    global current_path,animation_running
    tempPath = paths[current_path]

    startColumn = tempPath[0][1]
    startRow = tempPath[0][0]

    endColumn = tempPath[-1][1]
    endRow = tempPath[-1][0]

    startContainer = containers[tempPath[0][0]][tempPath[0][1]]
    endContainer = containers[tempPath[-1][0]][tempPath[-1][1]]
 
    if not animation_running:
        current_path = (current_path + 1) 
        current_path_label.config(text='Current Move {}/{}'.format(current_path+1, len(paths)))     
        startContainer.deselect_start(startColumn+1,startRow)
        endContainer.deselect_end(endColumn+1,endRow)
        #TODO add update to container name when next is pressed
        # container_label.config(text='Moving Container: {}'.format(containerArray[currentPath]))
        stop_animation(current_path, index, animate_button, containers, paths, popup)
        start_animation(current_path, index, animate_button, containers, paths, popup)

#popup for the main interface to use
def show_animation(paths,filename):
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
    
    max_row = 7

    paths = [[(max_row - row, col) for row, col in path] for path in paths]

    index = 0

    animate_button = Button(popup, text='Animate')
    animate_button.pack()

    animate_button.config(command=lambda current_path=current_path, index=index, animate_button=animate_button, containers=containers, paths=paths, popup=popup: start_animation(current_path, index, animate_button, containers, paths, popup))



    current_path_label = Label(popup, text=f"Current Move: {current_path+1}/{len(paths)}")
    current_path_label.pack()
    #temp name for containers
    #TODO add in
    tempname = "Container"
    container_label = Label(popup, text=f"Moving Container: {tempname}")
    container_label.pack()
    tempname2 = "Boralius"
    ship_label = Label(popup, text=f"Ship: {tempname2}")
    ship_label.pack()

    next_button = Button(popup, text='Next', command=lambda: next_animation( index, animate_button, containers, paths, popup, current_path_label, container_label))
    next_button.pack()

    popup.mainloop()