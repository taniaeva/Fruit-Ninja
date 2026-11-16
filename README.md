
# 🍉 Fruit Ninja Clone - Pygame Edition

A fully functional, arcade-style **Fruit Ninja** clone built from scratch using **Python** and the **Pygame** library. Slice flying fruits, trigger juicy particle splashes, dodge explosive bombs, and test your ninja reflexes!


## ✨ Features

- **Procedural Fruit Rendering:** Dynamically drawn fruits (Watermelon, Orange, Apple, and Banana) complete with rotation, texturing, and realistic split-half physics.
- **Arc Physics & Gravity:** Fruits and bombs follow authentic parabolic trajectories with adjustable gravity.
- **Glowing Blade Trail:** Fluid, fading mouse trail that simulates a razor-sharp ninja blade.
- **Juice Splashes & Particles:** Dynamic splash effects matching the color of the sliced fruit.
- **Bomb Hazards:** Dangerous metallic bombs with blinking fuses that trigger an instant Game Over if sliced.
- **Lives & Score System:** Lose a life if an unsliced fruit falls off-screen, with a 3-life limit before game over.
- **Dojo Aesthetic:** Custom wooden-themed dojo UI background and overlays.



## 🛠️ Prerequisites

Make sure you have **Python 3.x** installed on your system. You will also need the **Pygame** library.



## 🚀 Installation & Running

1. **Clone or Download** this repository to your local machine:
   ```bash
   git clone [https://github.com/your-username/fruit-ninja-pygame.git](https://github.com/your-username/fruit-ninja-pygame.git)
   cd fruit-ninja-pygame



2. **Install Pygame** using pip:
```bash
pip install pygame



3. **Run the Game:**
```bash
python main.py





## 🎮 Controls

| Action | Control |
| --- | --- |
| **Slice Fruits / Interact** | Move Mouse (Hover / Swipe across fruits) |
| **Start Game** | `SPACE` key or Click on Start Screen |
| **Restart (on Game Over)** | `R` key |
| **Return to Menu** | `ESC` key |



## 🏗️ Code Architecture

The game is structured using clean, object-oriented principles with Pygame:

* `Particle`: Manages juice splash droplets and spark physics/alpha fading.
* `Fruit`: Handles arc velocity, rotation, whole fruit drawing, and split-half animation upon slicing.
* `Bomb`: Simulates metallic explosive hazards with ticking fuse animation and collision detection.
* `Game`: Manages game states (`START`, `PLAYING`, `GAMEOVER`), score tracking, life penalties, and main event/render loops.



## 💡 Future Improvements (Planned)

* [ ] Add sound effects for slicing, splashes, and bomb detonations.
* [ ] Implement combo slicing bonuses (extra points for slicing 3+ fruits at once).
* [ ] Add high score tracking saved locally.
* [ ] Support click-and-hold swipe detection.



## 📜 License

This project is open-source and available under the [MIT License](https://www.google.com/search?q=LICENSE).


