🦖 Jumping Dinosaur Game with NEAT AI : First Let me explain why I love this project🫡

**Please Clicck me  https://www.loom.com/share/6eb361d4b70c4f3b94a0254244e62d41?sid=c1e4abf3-ae72-43ff-ae53-df93c1c91ab3**

Hi, I’m Bereket, and this is my little side project that turned into something… kinda cool.
I wanted to see if I could teach a dinosaur to jump over obstacles — without hardcoding the rules, and without relying on big machine learning libraries like TensorFlow or PyTorch. Just pure Python, math, and stubbornness.
So I built everything from scratch:
A neural network (yes, all the nodes, connections, activations — no Keras here 👀)
A population & evolution system inspired by NEAT (NeuroEvolution of Augmenting Topologies)
A little Pygame world where dinos run, blocks spawn, and chaos happens
The result? A dinosaur that learns to jump over blocks… eventually.

![Dino Game Screenshot](Screenshot%202025-09-29%20at%2016.21.51.png)

🎮 What Makes This Project Special

Most “AI dinos” out there use existing frameworks. Mine doesn’t.
No libraries for the neural net. I coded my own nodes, connections, feed-forward logic, and activation.
Evolution from scratch. Species grouping, mutations, fitness tracking — all hand-rolled.
Game + AI built together. Every crash, jump, and mutation happens live in Pygame.
This wasn’t just about making a game. It was about answering a question:
👉 Can I make an AI play a game without importing someone else’s brain?
Turns out, yes. With a lot of debugging. And coffee. Mostly coffee. ☕

The AI makes jumping decisions based on these inputs, and the population evolves over generations to improve performance.
![Dino Game Screenshot](Screenshot%202025-09-29%20at%2016.21.43.png)
🧠 How the Brain Works
The dino gets 3 inputs:
Distance to the nearest obstacle
Height of that obstacle
Its current vertical position
Those go into a tiny neural network I built myself. The network outputs a single value:
If the output > threshold → the dino jumps
Otherwise → it keeps running like nothing happened
Each dino’s brain evolves through generations. The ones that survive longer get better “genes” (weights). The rest… well, natural selection is cruel.
![Dino Game Screenshot](Screenshot%202025-09-29%20at%2016.21.58.png)
📂 File Structure
main.py → The main game loop + evolution process
Population.py → Handles dinos as a group (fitness, mutation, species, etc.)
DinoBrain.py → My DIY neural network
Node.py → A single neuron (mathy little guy)
Connection.py → Synapse connecting two neurons
component.py → Pygame stuff (Dino, Blocks, Ground)
config.py → Global game setup

⚙️ Requirements
Python 3.7+
Pygame

## Installation

1. Clone the repository
2. Install pygame: `pip install pygame`
3. Run the game: `python3 main.py`

## How to Play

The game runs automatically - watch as the AI learns to jump over obstacles! The console will show generation progress and fitness scores.

## NEAT Features

- **Species Management**: Groups similar neural networks
- **Fitness Tracking**: Measures performance based on distance traveled
- **Mutation**: Randomly modifies neural network weights
- **Evolution**: Best performers breed to create next generation
