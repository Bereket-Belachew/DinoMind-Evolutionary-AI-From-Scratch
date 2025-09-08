import Node
import Connection
import random
class DinoBrain:
    def __init__(self):
        self.input_nodes = [Node.Node(i) for i in range(3)]
        self.bias_node = Node.Node(3)
        self.output_node=Node.Node(4)
        self.output_node.layer=1
        self.connections=[]
        #Lets create the connections between the nodes with better initial weights:
        for i, nod in enumerate(self.input_nodes +[self.bias_node]):
            # Give better initial weights - distance should trigger jumps when close
            if i == 0:  # distance input
                weight = random.uniform(2, 5)  # Positive weight for distance
            elif i == 1:  # block height input  
                weight = random.uniform(-2, 2)  # Mixed weight for height
            elif i == 2:  # dino y position
                weight = random.uniform(-1, 1)  # Small weight for position
            else:  # bias node
                weight = random.uniform(-3, -1)  # Negative bias to prevent constant jumping
                
            conn = Connection.Connection(nod,self.output_node,weight)
            nod.connections.append(conn)
            self.connections.append(conn)
    #Now lets Work on NEAT(Neuroevolution)
    def clone(self):
        clone = DinoBrain()
        for i, conn in enumerate(self.connections):
            clone.connections[i].weight = conn.weight
        return clone
    
    def mutate(self):
        for conn in self.connections:
            if random.random() < 0.1:  # 10% chance per connection
                conn.weight += random.gauss(0, 0.5)
                conn.weight = max(min(conn.weight, 5), -5)
    def feed_forward(self,inputs):
        for i, val in enumerate(inputs):
            self.input_nodes[i].output_value=val

        # Set bias node output to 1 (bias should always be 1)
        self.bias_node.output_value = 1

        #lets clear any initial value in the output node
        self.output_node.input_value=0

        # First, activate input nodes and bias node to propagate values
        for nod in self.input_nodes +[self.bias_node]:
            nod.activate()
        
        # Now activate the output node with accumulated input
        self.output_node.activate()
        output = self.output_node.output_value
        
        # Debug: Print neural network internals (reduced frequency)
        if hasattr(self, 'debug_counter'):
            self.debug_counter += 1
        else:
            self.debug_counter = 0
            
        if self.debug_counter % 300 == 0:  # Print every 300 frames (5 seconds)
            print(f"AI Output: {output:.3f} (Jump threshold: 0.3)")

        #lets reset the input value for the next frame
        self.output_node.input_value=0

        return output
