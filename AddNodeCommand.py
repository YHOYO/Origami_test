import Draw as draw
import sys

class AddNodeCommand:
    def __init__(self, model, source, x, y, length, strain):
        self.source = source
        self.x = x
        self.y = y
        self.length = length
        self.strain = strain
        self.add_node_to(model, self.source, self.x, self.y, self.length, self.strain)

    def add_node_to(self, model, source_node=None, x=0.0, y=0.0, length=1.0, strain=0.0):
        # Ensure model.width and model.height are floats
        model.width = float(model.width)
        model.height = float(model.height)

        if x > model.width or y > model.height:
            print("Error: coordinates not in scope", file=sys.stderr)
        elif x < 0 or y < 0:
            print("Error: coordinates must be positive", file=sys.stderr)
        elif length < 0 or strain < 0:
            print("Error: length and strain must be positive", file=sys.stderr)
        # if this is the first node
        elif len(model.G) == 0 and source_node is None:
            model.G.add_node(model.node_counter, x=x, y=y)
            draw.DrawCommand(model.app)
            model.node_counter += 1
        # adding additional nodes
        elif source_node in model.G.nodes():
            new_node = model.node_counter
            model.G.add_node(new_node, x=x, y=y)
            model.G.add_edge(new_node, source_node, length=length, strain=strain)
            draw.DrawCommand(model.app)
            model.node_counter += 1
        else:
            print("Error: source not found", file=sys.stderr)

    def undo(self, model):
        model.node_counter -= 1
        model.G.remove_node(model.node_counter)
        draw.DrawCommand(model.app)
