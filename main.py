import pygame
from sys import exit
import config
import Population

pygame.init()
clock=pygame.time.Clock()

def quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

def main():
    # Initialize population of dinos
    population = Population.Population(size=10)
    game_over = False
    generation_start_time = pygame.time.get_ticks()
    
    while True:
        quit_game()
        config.window.fill((0,0,0))
        
        # Update game objects
        config.block.updates()
        
        # Update all agents
        for agent in population.get_all_agents():
            if agent.alive:
                agent.update()
        
        # Draw everything
        config.ground.draw(config.window)
        config.block.draw(config.window)
        
        # Draw all alive agents
        for agent in population.get_all_agents():
            if agent.alive:
                agent.draw(config.window)

        # AI decision making for each alive agent
        for agent in population.get_all_agents():
            if agent.alive:
                # Dino vision (AI inputs)
                distance = config.block.x - agent.x
                block_height = config.block.rect.height
                dino_y = agent.y

                inputs = [distance / 550, block_height / 100, dino_y / 400]  # normalize
                output = agent.brain.feed_forward(inputs)

                # Make dino jump if output > 0.3 and dino is on ground
                if output > 0.3 and agent.on_ground:
                    agent.jump()

                # Check collision
                if agent.rect.colliderect(config.block.rect):
                    agent.alive = False

        # Update fitness based on current block position
        population.update_fitness(config.block.x)
        
        # Debug info
        if pygame.time.get_ticks() % 2000 < 16:  # Every 2 seconds
            alive_count = sum(1 for agent in population.get_all_agents() if agent.alive)
            best_fitness = max(agent.fitness for agent in population.get_all_agents())
            print(f"Gen {population.generation}: {alive_count} alive, Best fitness: {best_fitness:.1f}")

        # Check if all agents are dead or generation time limit reached
        if population.all_dead() or pygame.time.get_ticks() - generation_start_time > 30000:  # 30 second limit
            print(f"Generation {population.generation} complete!")
            print(f"Best fitness: {population.get_best_agent().fitness:.1f}")
            
            # Evolve to next generation
            population.evolve()
            generation_start_time = pygame.time.get_ticks()
            game_over = False

        pygame.display.flip()
        clock.tick(60)

main()