# Prompts to test o3-mini preview

> Credits to AI Search YouTube ["OpenAI o3-mini is a BEAST"](https://www.youtube.com/watch?v=zRPBovmV8F8) for all these examples.

## Autonomous Snake Game

1. Open the empty [auto-snake.py](../python/auto-snake.py) file.
2. Launch Copilot Edits and add `auto-snake.py` to the working set.
3. Submit the following prompt in the chat:

    ```
    Create an autonomous snake game using Python. The two snakes compete with each other. Add a scoring system to keep track of the scores. The game should end when one of the snakes eats 10 food. The snakes should avoid hitting each other. Do not close the game window after the game ends.
    ```

4. Create a Python environment if you don't have one.
5. Install the required packages.
6. Run the code: `python auto-snake.py`.

### Additional Snake Challenges

```
Every 5 seconds, add a barrier that the snakes must avoid. This should be colored red. Barriers should appear at random locations on the screen. The game should end if a snake hits a barrier.
```

### Observations

- o3-mini generates a working code, but some bugs are present. Using Claude 3.5 Sonnet to fix the bugs work well.
- Claude 3.5 Sonnet can also generate the code in one-shot prompt.

## Ball in Hexagon

```
Write a Python program that shows a ball bouncing inside a spinning hexagon. The ball should be affected by gravity and friction, and it must bounce off the rotating walls realistically.
```

### Observations

- o3-mini generates a working code, but some bugs are present. Using Claude 3.5 Sonnet to fix the bugs work well.
- Claude 3.5 Sonnet can also generate the code in one-shot prompt.

## How water Molecules from Hydrogen bonds

```
Generate an interactive simulation showing how how water molecules form hydrogen bonds. The visualizer should depict dynamic interactions between molecules, highlighting the formation and breaking of hyrdogen bonds based on temperature changes. Use CSS, JS and HTML in a single HTML file.
```

### Observations

- o3-mini generates a working code, but some bugs are present such as molecules not changing speed the higher the temperature.
- Claude 3.5 Sonnet can also generate the code in one-shot prompt, and better visuals.

## Big Bang Simulation

```
Create a highly advanced, visually stunning demo using three.js that simulates the Big Bang expansion. The demo should capture the transition from the initial point of singularity into a vibrant, expanding cosmos. Ensure that the code is self-contained and can be easily run in a modern web browser. Include a start and reset button.
```

### Observations

- Claude 3.5 Sonnet generates a working code but didn't follow the prompt exactly. The visuals are stunning.
- o3-mini didn't get the requirements right, but the code is self-contained and can be run in a modern web browser.
- Revised the prompt and asked o3-mini to generate the code again. The code is now working as expected and visually stunning.

## Spiral Galaxy evolution

```
Create a simulation of a spiral galaxy spinning realistically using Einstien's General Theory of Relativity calculation. The simulation should depict the movement of stars within the galaxy. Add a Super massive black hole at the center of the galaxy. Use a combination of CSS, Three.js, and HTML in a single HTML file. Make the simulation interactive by allowing users to control the speed of time. Include a start and reset button.  Continue Use colors to differentiate between stars, cosmic dusts, and black hole in the center of the galaxy.
```

#### Issue with the simulation
```
The simulation does not generate the spiral arm as the galaxy evolves. 
```

#### Add a SMBH

```
Let's add a super massive black hole at the center of the galaxy and recalculate the evolution algorithm.
```

## The Solar System

```
Create a visually stunning simulation of the solar system using Three.js. The simulation should depict the movement of all 8 planets around the sun, including the rotation of the planets on their axis. Add the moon to the Earth and make it rotate around the Earth. Include play and pause button that controls the movement of the objects in the solar system. Add mouse controls to rotate camera angle and zoom functionality. Use colors to differentiate between planets, moon and the sun.
```

- o3-mini blocks this prompt saying it was filtered by the Responsible AI Service. (What?)
