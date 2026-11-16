🍉 Fruit Ninja - Pygame Edition
A polished, object-oriented 2D arcade slice-em-up game built in Python using the Pygame library. Test your reflexes by slicing juicy procedural fruits while dodging dangerous metallic bombs in a classic Dojo setting!
✨ Features
Procedural Fruit Rendering: Dynamically drawn fruits (Watermelon, Orange, Apple, and Banana) complete with textures, stems, leaves, and realistic sliced halves.
Arc Physics Engine: Fruits and bombs are launched from the bottom of the screen with randomized parabolic arcs, gravity acceleration, and rotation speeds.
Fluid Blade Mechanics: Smooth, glowing mouse trail effect that fades over time to simulate a slicing blade.
Juice & Spark Particles: Slicing fruits triggers colorful juice splashes, while active bombs feature glowing, crackling fuses.
Hazard System: Procedurally spawned bombs that trigger an instant Game Over if sliced.
Arcade Life & Score Tracker: Keep track of your score and 3 lives (losing a life when an unsliced fruit falls off-screen).
Multiple Game States: Clean transitions between Start Menu, Active Gameplay, and Game Over screens.
🛠️ Prerequisites & Installation
Make sure you have Python installed on your system (Python 3.7+ recommended).
Install Pygame:
Open your terminal or command prompt and run:
Bash
pip install pygame
Run the Game:
Save the Python script as fruit_ninja.py and run it:
Bash
python fruit_ninja.py
🎮 Controls
Action	Control
Start / Restart Game	Spacebar or Left Mouse Click
Slice Fruits / Bombs	Hold and drag the Left Mouse Button
Return to Menu	ESC key (during gameplay or game over)
Restart from Game Over	R key
🏗️ Code Architecture
The game is structured using clean, object-oriented programming principles:
Particle: Handles juice splashes and explosion sparks with gravity and fading alpha transparency.
Fruit: Handles whole fruit rendering, rotation physics, slice detection, and split-half animation.
Bomb: Manages metallic bomb rendering, fuse spark animations, and collision hitboxes.
Game: Controls the main state machine (START, PLAYING, GAMEOVER), event loops, score/lives tracking, and rendering pipelines.
📝 License
This project is open-source and free to use for educational and personal projects.
