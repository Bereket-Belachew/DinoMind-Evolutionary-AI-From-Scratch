import math
class Node:
    def __init__(self,id):
        self.id = id
        self.input_value=0
        self.output_value=0
        self.connections =[]
        self.layer=0
    def activate(self):
        def sigmoid(x):
            return 1 / (1 + math.exp(-x))
        if self.layer==1:
            self.output_value= sigmoid(self.input_value)

        for conn in self.connections:
            conn.to_node.input_value += conn.weight * self.output_value
