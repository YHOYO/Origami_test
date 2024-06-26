import tkinter as tk
import DimensionsBox as dbox
import NodeBox as nbox
import Model as model
import sys
import AddNodeCommand as addnodec

class Application(tk.Frame):
    
    # initialize frame
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        master.title("untitled")
        self.pack()
        self.model = None
        self.dimensions = None
        self.name = None
        self.create_canvas_frame()
        self.widgets()      
            
    def getDimensions(self):
        return self.dimensions
         
    # makes canvas / frame size
    def create_canvas_frame(self):
        self.frame_pixels = 500
        self.frame = tk.Canvas(self, width=self.frame_pixels, height=self.frame_pixels)
        self.frame.pack()
        
        # image = cool_image_from_file
        # image.place location
    
    # creates the basic widgets for starting a new model, quit    
    def widgets(self):
        # quits the program
        self.b_QUIT = tk.Button(self)
        self.b_QUIT["text"] = "QUIT"
        self.b_QUIT["fg"] = "red"
        self.b_QUIT["command"] = self.quit
  
        self.b_QUIT.pack()
        
        # test: print model
        self.b_print = tk.Button(self)
        self.b_print["text"] = "Print Model"
        self.b_print["command"] = self.print_model
        
        self.b_print.pack()
        
        self.b_newmodel = tk.Button(self)
        self.b_newmodel['text'] = "New Model"
        self.b_newmodel['command'] = self.new_model
        self.b_newmodel.pack()
        
        # does scale optimization when ready
        self.b_optimize = tk.Button(self)
        self.b_optimize["text"] = "scale optimization"
        self.b_optimize["command"] = self.scale_optimization_and_check
        self.b_optimize.pack()
 
    # calls optimization if ready
    def scale_optimization_and_check(self):
        if self.model is None:
            print("Error: model not initialized yet")
            
        elif self.model.scale_optimization_ready():
            
            optimization = self.model.scale_optimization()
            newcoords = optimization.x
            self.model.change_to_optimized_coordinates(newcoords)
            print(optimization)
            # redraw model
            # get all of the new coordinates
            # change the coordinates of the model so that nodes are at the optimized coordinates.
            # draw circles at each x coordinate
            
        else:
            print("Error: model not ready for scale optimization yet", file=sys.stderr)
            
        
    # create a dialog box, wait until the box is closed before accessing its properties
    def new_model(self):
        # destroy old windows currently running
        inputDialog = dbox.DimSubmissionBox(self) # not sure whether this should be self or root that goes to dbox as the parent
        self.wait_window(inputDialog.top)
        dimensions = inputDialog.entered_dimensions
        self.name = inputDialog.name
        self.master.title(self.name)
        self.dimensions = dimensions
        self.initialize_model(dimensions)
        self.draw_new_paper()
        self.new_node_dialog_box()
        
    # create origami model object
    def initialize_model(self, paper_size):
    
        width = paper_size[0]
        height = paper_size[1]
        self.model = model.Model(self, width, height)
        
    # draws a square representing the paper
    def draw_new_paper(self):
        # if a node submission box exists already, destroy it
        # 1) check if box exists
        # 2) destroy
        # another possibility
        # destroy all toplevel objects
        # if self.nodebox:
        #    self.nodebox.destroy()
        
        
        dimensions = self.dimensions
        border_p =  self.border_pixels = self.frame_pixels // 10
        frame_pixels = self.frame_pixels
        paper_height = float(dimensions[1])
        paper_width = float(dimensions[0])
        paper_long_edge_pixels = frame_pixels - 2 * border_p
       
        self.frame.delete("all")
        
        # Title
        if self.name:
            self.frame.create_text(paper_long_edge_pixels / 2 + border_p, border_p / 2 - 10, text=self.name.upper())
        
        # draw a hamburger/hotdog rectangle of the same shape as the paper dimensions
        if paper_height > paper_width:
            paper_height_pixels = paper_long_edge_pixels
            paper_width_pixels = paper_shorter_edge_pixels = paper_width / paper_height * paper_long_edge_pixels
            self.frame.create_rectangle(border_p, border_p, border_p + paper_shorter_edge_pixels, border_p + paper_long_edge_pixels, fill="white")
        else:
            paper_width_pixels = paper_long_edge_pixels
            paper_height_pixels = paper_shorter_edge_pixels = paper_height / paper_width * paper_long_edge_pixels
            self.frame.create_rectangle(border_p, border_p, border_p + paper_long_edge_pixels, border_p + paper_shorter_edge_pixels, fill="white")
            
       # draw hash marks / paper size
        # hash markers every .25 size increments
        # width marks
        x_marker_dist = 0
        while x_marker_dist <= paper_width:
            marker_incr_p = paper_width_pixels * x_marker_dist / paper_width
            self.frame.create_line(border_p + marker_incr_p, border_p - 10, border_p + marker_incr_p, border_p - 3)
            self.frame.create_text(border_p + marker_incr_p, border_p - 17, text=str(x_marker_dist))
            x_marker_dist += 0.25
        
        # height marks
        y_marker_dist = 0
        while y_marker_dist <= paper_height:
            marker_incr_p = paper_height_pixels * y_marker_dist / paper_height
            self.frame.create_line(border_p - 10, border_p + marker_incr_p, border_p - 3,  border_p +  marker_incr_p)
            self.frame.create_text(border_p - 23, border_p + marker_incr_p, text=str(y_marker_dist))
            y_marker_dist += 0.25
            
    
    
    def new_node_dialog_box(self):
        nodebox = nbox.NodeBox(self, self)
        # self.wait_window(inputDialog.top)
        # self.dimensions = inputDialog.dimensions ###not ture anymore
    
    
    # adds the information about the node received from the nodebox to the model
    def move_node_info_from_app_to_model(self, source, x=0.5, y=0.5, length=1.0, strain=1.0):
        self.model.add_node_to(source, x, y, length, strain)
    
    # undo add node
    def add_node_undo(self):
        self.model.add_node_undo()
        
    # I'm pretty sure this needs to be discarded    
    def model_widgets(self):
        self.new_node_l = tk.Label(self.master, self)
        self.new_node_l['text'] = 'new node information'
        
        self.node_entry = tk.Entry(self)
        self.node_entry["command"]
        
        self.node_button = tk.Button(self)
        self.node_button["text"] = 'enter new info'

    def print_model(self):
        print("Model Nodes", file=sys.stderr)
        print(self.model.G.nodes(data=True), file=sys.stderr)
        print("Model Edges", file=sys.stderr)
        print(self.model.G.edges(data=True), file=sys.stderr)
            
    def draw_scaled_model(self, optimize_return_object):
        new_x_vector = optimize_return_object.x
        new_scale = new_x_vector[-1]