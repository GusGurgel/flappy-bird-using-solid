# Flappy Bird - Applying SOLID Principles bird 🐥💻

## Introduction
This repository contains the implementation of a **Flappy Bird** clone, developed using the **pygame** library. The project was carried out as part of a **Software Engineering** course assignment, aiming to apply **SOLID** principles to improve code quality.

## About the Assignment
The assignment was structured into five main stages:

1. **Theoretical Research on SOLID Principles**
   - Studying SOLID principles through books, articles, and videos.
   - Identifying practical examples and analyzing the importance of these principles in software design.
   - Producing a theoretical summary for the final report.

2. **Creation/Reutilization of an Initial Algorithm (Without SOLID)**
   - Developing a first version of the game **without applying SOLID**.
   - Identifying common problems such as monolithic code, excessive coupling, and low flexibility.

3. **Refactoring with SOLID**
   - Analyzing violations of principles in the initial code.
   - Refactoring to apply SOLID and improve code structure.

4. **Documentation and Comparison**
   - Preparing a detailed report describing the initial code flaws.
   - Explaining how each SOLID principle was applied during refactoring.
   - Comparing the versions before and after refactoring, highlighting improvements.

5. **Presentation and Demonstration**
   - Demonstrating the game before and after refactoring.
   - Explaining the corrected problems and the benefits of applying SOLID.

## Technologies Used 🔍
- **Python**
- **Pygame**

## Repository Structure
```
📂 flappy-bird-solid
 ├── 📂 src              # Source code
 ├── 📂 LaTeX            # LaTeX project presentation
 ├── README.md           # Project introduction
```

## How to Run
1. Clone this repository:
   ```bash
   git clone 
   cd flappy-bird-solid
   ```
2. Install dependencies:
   ```bash
    pip install pygame-ce
   ```
3. Run the game:
   ```bash
   python src/main(s|o|l|i).py
   ```

### Progressive Development with SOLID

The project started as a nearly procedural Flappy Bird clone, without applying any SOLID principles. The principles were then introduced one by one in an incremental manner.

Each file represents a step in this transformation:

main_s.py applies the Single Responsibility Principle (S).

main_o.py incorporates Open/Closed Principle (O).

main_l.py introduces the Liskov Substitution Principle (L).

And so forth, gradually integrating each SOLID principle.

The development from one version to the next is constructive, ensuring each new iteration builds upon the previous improvements while maintaining functionality.
Aqui está uma explicação mais clara sobre a evolução do código ao aplicar o **Single Responsibility Principle** (SRP):

### **From `main.py` to `main_s.py` (Applying Single Responsibility Principle)**

```python
#imports...

class Game:
    def __init__(self):
        # initating pygame and all objects properties...

    def move_background(self, dt):
        # logic...
    
    def move_bird(self, dt):
        # logic...

    def animate_bird(self):
        # logic...
    
    # mover canos
    def move_pipes(self, dt):
        # logic...

    def handle_collision(self):
        # logic...
    
    # resetar o jogo
    def reset_game(self):
        # logic...

    def update(self, dt):
        # logic...

    # desenhar objetos
    def draw(self):
        # logic...

    # game loop
    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            self.handle_events()
            self.update(dt)
            self.draw()

        # Quit services
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
```

Initially, the project started with a **monolithic** `Game` class, where all functionalities were tightly coupled within a single class. This version had several responsibilities mixed together, including:
- Handling game logic.
- Managing background movement.
- Updating and animating the bird.
- Handling collisions.
- Drawing objects on the screen.

This violated the **Single Responsibility Principle (SRP)** because a single class was responsible for too many tasks.

#### **Refactoring for SRP**

```python
#imports...

class Object():
    # generic object...

class ObjectContainer():
    # logic...

class Background(Object):
    # logic...

class Bird(Object):
    # logic...

class DoublePipe(Object):
    # logic...

class Death(Object):
    # logic...

class Score(Object):
    # logic

class Game:
    def __init__(self):
        # init pygame...

        # instantiate objects...
        self.bird = Bird()
        self.background = Background()
        self.double_pipe = DoublePipe()
        self.death = Death(self.bird, self.double_pipe, self.reset)
        self.score = Score()
        self.score_observer = ScoreObserver(self.bird, self.double_pipe, self.score)

        self.objects_container = ObjectContainer([
            self.bird,
            self.background,
            self.double_pipe,
            self.death,
            self.score,
            self.score_observer
        ])

    def reset(self):
        # logic...
    
    # resolver os eventos
    def handle_events(self):
        # logic...

    # atualizar jogo
    def update(self, dt):
        # logic..

    # desenhar objetos
    def draw(self):
        # logic...
    
    # game loop
    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            self.handle_events()
            self.update(dt)
            self.draw()

        # Quit services
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
```

To address this issue, the responsibilities were **separated into distinct classes**, each handling a specific aspect of the game. The refactored version (`main_s.py`) introduces:
- **`Background` class**: Handles the background movement.
- **`Bird` class**: Manages the bird's movement and animations.
- **`DoublePipe` class**: Controls the pipe obstacles.
- **`Death` class**: Detects collisions and resets the game.
- **`Score` class**: Tracks the player's score.
- **`ObjectContainer` class**: Maintains a collection of game objects.

Now, the `Game` class focuses only on:
- Initializing objects.
- Managing the game loop.
- Handling high-level game state transitions.

This refactoring **reduces coupling**, **improves maintainability**, and **makes future modifications easier**. The next step (`main_o.py`) builds upon this foundation by applying the **Open/Closed Principle (OCP)**.

### **From `main_s.py` to `main_o.py` (Applying Open/Closed Principle)**


After implementing the **Single Responsibility Principle (SRP)**, the next step was applying the **Open/Closed Principle (OCP)**. In `main_s.py`, all objects had fixed behaviors, meaning any change in movement logic required modifying existing classes, which violates OCP.

#### **Refactoring for OCP**

```python
#imports...

class Object():
    # generic object...

class MovableObject(Object):
    # movable generic object..

class HorizontalMovableObject(MovableObject):
    # generic horizontal movable object...

class ObjectContainer():
    # logic...

class Background(MovableObject):
    # logic...

class Bird(MovableObject): # add HozizontalMovable to move bird
    # logic...

class DoublePipe(Object):
    # logic...

class Death(Object):
    # logic...

class Score(Object):
    # logic

class Game:
    def __init__(self):
        # init pygame...

        # instantiate objects...
        self.bird = Bird()
        self.background = Background()
        self.double_pipe = DoublePipe()
        self.death = Death(self.bird, self.double_pipe, self.reset)
        self.score = Score()
        self.score_observer = ScoreObserver(self.bird, self.double_pipe, self.score)

        self.objects_container = ObjectContainer([
            self.bird,
            self.background,
            self.double_pipe,
            self.death,
            self.score,
            self.score_observer
        ])

    def reset(self):
        # logic...
    
    # resolver os eventos
    def handle_events(self):
        # logic...

    # atualizar jogo
    def update(self, dt):
        # logic..

    # desenhar objetos
    def draw(self):
        # logic...
    
    # game loop
    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            self.handle_events()
            self.update(dt)
            self.draw()

        # Quit services
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
```

To allow **extensibility without modifying existing code**, a new **hierarchy of movement-related classes** was introduced:
- **`MovableObject`**: A generic class for all objects that can move.
- **`HorizontalMovableObject`**: A specialization of `MovableObject` that provides horizontal movement logic.

### **Key Changes**
1. The `Background` and `Bird` classes now extend `MovableObject`, allowing them to be moved without modifying their core logic.
2. The `Bird` class was further improved by inheriting from `HorizontalMovableObject`, ensuring it can move horizontally without rewriting movement logic in multiple places.
3. The rest of the game structure remained unchanged, demonstrating **OCP in action**—new functionality was added **without modifying** the existing `Game` class.

This approach **reduces code duplication**, **improves flexibility**, and **makes future movement-related changes easier**. The next step (`main_l.py`) will focus on implementing the **Liskov Substitution Principle (LSP)**.