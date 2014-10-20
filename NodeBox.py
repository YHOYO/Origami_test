import Tkinter as Tk
import re

class NodeBox(object):

    #the initial nodebox should have a frame and add-node
    
    def __init__(self, parent, application):
        top = self.top = Tk.Toplevel(parent)
        dialog = Tk.Frame(self.top)
        dialog.grid()
        self.add_node_widgets(dialog)
        self.app = application
    
    #provides interface for adding node information
    def add_node_widgets(self,dialog):
        self.l_source_node = Tk.Label(dialog)
        self.l_source_node["text"] = "Source Node:"
        self.l_source_node.grid(row = 0,column = 0)
        
        
        self.e_source_node = Tk.Entry(dialog)
        self.e_source_node.grid(row = 0, column = 1)
        
        self.l_xy = Tk.Label(dialog)
        self.l_xy["text"] = "Coordinates:"
        self.l_xy.grid(row = 1, column = 0)
        
        
        self.e_xy = Tk.Entry(dialog)
        self.e_xy.grid(row = 1, column = 1)
        
        self.l_length = Tk.Label(dialog)
        self.l_length["text"] = "Length:"
        self.l_length.grid(row = 2, column = 0)
        
        self.e_length = Tk.Entry(dialog)
        self.e_length.grid(row = 2, column = 1)
         
        self.l_strain = Tk.Label(dialog)
        self.l_strain["text"] = "Strain:"
        self.l_strain.grid(row = 3, column = 0)
        
        self.e_strain = Tk.Entry(dialog)
        self.e_strain.grid(row = 3, column = 1)
        
        
        self.b_addnode = Tk.Button(dialog)
        self.b_addnode['text'] = "Add Node"
        self.b_addnode['command'] = lambda: self.add_node_info(self.app)
        self.b_addnode.grid(columnspan = 2)
        
        
        
    #def 

    #this creates a block of information on a node
    #the info block contiains
    #name of node
    #coordinates
    #neighbors
    #
    
    #pass the node information to the application where the model is stored
    def add_node_info(self, application):
    
        source_string = self.e_source_node.get() #in string form
        x_coordinate = self.coordinate_parse()[0]
        y_coordinate = self.coordinate_parse()[1]
        length = self.e_length.get()
        strain = self.e_strain.get()
        
        
        #checks to see if this is the first node (should change to check box)
        if source_node is "":
            source_node = None
        
        #converte source_node from string to int
        else:
            source_int = int(source_node)
        #user input errors possible
        application.add_node_to_model(source_int, x_coordinate, y_coordinate, length, strain)
        application.draw_node(source_int, x_coordinate, y_coordinate, length, strain)
        
    #takes input string of the coordinates, returns a touple
    def coordinate_parse(self):
        coord_string = self.e_xy.get()
        int_or_float= re.compile("\d+\.?\d*") #really want \d+\.?\d* OR \d*\.?\d+ first covers (1 and 1.0), second covers (.2, 1.0). \d*\.\d* would cover all of these and individual periods, which seems reasonable, but may also caputre periods by themselves need to test.
        xy = re.findall(int_or_float, coord_string)
        if len(xy)!=2:
            print "ERROR: coordinates must have x and y"
        x = float(xy[0])
        y = float(xy[1])
        return (x,y)