import DinoBrain
import random
import component

class Agent:
    def __init__(self, x, y):
        self.brain = DinoBrain.DinoBrain()
        self.x = x
        self.y = y
        self.rect = component.pygame.Rect(self.x, self.y, 30, 30)
        self.velocity_y = 0
        self.on_ground = True
        self.alive = True
        self.fitness = 0
        self.distance_traveled = 0
        self.successful_jumps = 0
        self.last_block_x = 550  # Track when block passes
        
    def draw(self, window):
        if self.alive:
            component.pygame.draw.rect(window, (255, 255, 255), self.rect)
    
    def jump(self):
        if self.on_ground and self.alive:
            self.velocity_y = -18  # Increased jump velocity for better clearance
            self.on_ground = False
    
    def update(self):
        if not self.alive:
            return
            
        # Apply gravity
        self.velocity_y += 0.7  # Slightly reduced gravity for better jump arc
        self.y += self.velocity_y
        
        # Check if dino hits ground
        if self.y >= 370:  # Ground level
            self.y = 370
            self.velocity_y = 0
            self.on_ground = True
        
        # Update rectangle position
        self.rect.y = self.y
        
        # Track distance traveled (fitness)
        self.distance_traveled += 2  # Block moves 2 pixels per frame

class Species:
    def __init__(self):
        self.agents = []
        self.average_fitness = 0
        self.generations_without_improvement = 0
        
    def calculate_average_fitness(self):
        if self.agents:
            self.average_fitness = sum(agent.fitness for agent in self.agents) / len(self.agents)
        else:
            self.average_fitness = 0

class Population:
    def __init__(self, size=10):
        self.size = size
        self.generation = 1
        self.species = []
        
        # Create initial species with agents
        initial_species = Species()
        for i in range(size):
            agent = Agent(50, 370)  # All start at same position
            initial_species.agents.append(agent)
        self.species.append(initial_species)
        
    def get_all_agents(self):
        """Get all agents from all species"""
        all_agents = []
        for species in self.species:
            all_agents.extend(species.agents)
        return all_agents
    
    def update_fitness(self, block_x):
        """Update fitness based on survival time and successful jumps"""
        for species in self.species:
            for agent in species.agents:
                if agent.alive:
                    # Check if agent successfully jumped over a block
                    if block_x < agent.last_block_x - 30:  # Block passed the agent
                        agent.successful_jumps += 1
                        agent.last_block_x = block_x
                    
                    # Reward for staying alive + bonus for successful jumps
                    frames_alive = agent.distance_traveled / 2
                    agent.fitness = frames_alive + (agent.successful_jumps * 100)  # 100 points per successful jump
                else:
                    # Dead agents keep their final fitness
                    frames_alive = agent.distance_traveled / 2
                    agent.fitness = frames_alive + (agent.successful_jumps * 100)
    
    def evolve(self):
        """Evolve the population to next generation"""
        self.generation += 1
        
        # Get all agents and sort by fitness
        all_agents = self.get_all_agents()
        all_agents.sort(key=lambda a: a.fitness, reverse=True)
        
        # Create new population
        new_species = Species()
        
        # Keep top 20% of agents unchanged (elitism)
        elite_count = max(1, self.size // 5)
        for i in range(elite_count):
            elite_agent = Agent(50, 370)
            elite_agent.brain = all_agents[i].brain.clone()  # Clone without mutation
            new_species.agents.append(elite_agent)
        
        # Fill remaining slots with mutated versions of best agents
        remaining_slots = self.size - elite_count
        for i in range(remaining_slots):
            # Select parent from top 50% of agents (tournament selection)
            parent_pool = all_agents[:max(1, len(all_agents)//2)]
            parent = random.choice(parent_pool)
            
            # Create child with mutation
            child = Agent(50, 370)
            child.brain = parent.brain.clone()
            child.brain.mutate()
            new_species.agents.append(child)
        
        # Replace old species with new one
        self.species = [new_species]
        
        # Reset all agents for new generation
        for agent in new_species.agents:
            agent.x = 50
            agent.y = 370
            agent.rect.x = 50
            agent.rect.y = 370
            agent.velocity_y = 0
            agent.on_ground = True
            agent.alive = True
            agent.fitness = 0
            agent.distance_traveled = 0
            agent.successful_jumps = 0
            agent.last_block_x = 550
    
    def get_best_agent(self):
        """Get the agent with highest fitness"""
        all_agents = self.get_all_agents()
        if all_agents:
            return max(all_agents, key=lambda a: a.fitness)
        return None
    
    def all_dead(self):
        """Check if all agents are dead"""
        return all(not agent.alive for agent in self.get_all_agents())