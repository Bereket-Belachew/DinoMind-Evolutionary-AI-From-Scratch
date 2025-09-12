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
            # Give better initial weights based on input meaning
            if i == 0:  # time_to_collision input (higher = more time, lower = less time)
                weight = random.uniform(-3, -1)  # Negative weight - less time = more likely to jump
            elif i == 1:  # block height input  
                weight = random.uniform(-0.5, 0.5)  # Small weight for height
            elif i == 2:  # clearance needed input
                weight = random.uniform(1, 3)  # Positive weight - more clearance needed = more likely to jump
            else:  # bias node
                weight = random.uniform(-1, 0)  # Small negative bias to prevent constant jumping
                
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
            if random.random() < 0.3:  # 30% chance per connection for more diversity
                conn.weight += random.gauss(0, 0.8)  # Larger mutations
                conn.weight = max(min(conn.weight, 8), -8)  # Wider weight range
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
