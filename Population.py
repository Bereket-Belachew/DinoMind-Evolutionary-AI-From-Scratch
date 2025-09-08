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
        
    def draw(self, window):
        if self.alive:
            component.pygame.draw.rect(window, (255, 255, 255), self.rect)
    
    def jump(self):
        if self.on_ground and self.alive:
            self.velocity_y = -15
            self.on_ground = False
    
    def update(self):
        if not self.alive:
            return
            
        # Apply gravity
        self.velocity_y += 0.8
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
        """Update fitness based on how far agents traveled before dying"""
        for species in self.species:
            for agent in species.agents:
                if agent.alive:
                    # Fitness = distance traveled + bonus for staying alive
                    agent.fitness = agent.distance_traveled + (550 - block_x) * 0.1
                else:
                    # Dead agents get their final fitness
                    agent.fitness = agent.distance_traveled
    
    def evolve(self):
        """Evolve the population to next generation"""
        self.generation += 1
        
        # Calculate fitness for each species
        for species in self.species:
            species.calculate_average_fitness()
        
        # Sort species by average fitness
        self.species.sort(key=lambda s: s.average_fitness, reverse=True)
        
        # Keep best species, mutate others
        new_species = []
        
        # Keep top 20% of species unchanged
        keep_count = max(1, len(self.species) // 5)
        for i in range(keep_count):
            new_species.append(self.species[i])
        
        # Create new agents for remaining slots
        remaining_slots = self.size - sum(len(s.agents) for s in new_species)
        
        if remaining_slots > 0:
            # Create new species with mutated agents
            new_species_group = Species()
            for i in range(remaining_slots):
                # Clone best agent and mutate
                best_agent = self.species[0].agents[0]  # Best agent from best species
                new_agent = Agent(50, 370)
                new_agent.brain = best_agent.brain.clone()
                new_agent.brain.mutate()
                new_species_group.agents.append(new_agent)
            new_species.append(new_species_group)
        
        self.species = new_species
        
        # Reset all agents for new generation
        for species in self.species:
            for agent in species.agents:
                agent.x = 50
                agent.y = 370
                agent.rect.x = 50
                agent.rect.y = 370
                agent.velocity_y = 0
                agent.on_ground = True
                agent.alive = True
                agent.fitness = 0
                agent.distance_traveled = 0
    
    def get_best_agent(self):
        """Get the agent with highest fitness"""
        all_agents = self.get_all_agents()
        if all_agents:
            return max(all_agents, key=lambda a: a.fitness)
        return None
    
    def all_dead(self):
        """Check if all agents are dead"""
        return all(not agent.alive for agent in self.get_all_agents())