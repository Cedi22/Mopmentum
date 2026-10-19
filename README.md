# MOPMENTUM

> *Clean the house. Fight your own movement. Keep your total damage under $2,000.*

A Bennett Foddy and Dani-inspired 3D cleaning game where your movement is deliberately slippery, wobbly, and drunk. Cleaning is your job — but your body refuses to cooperate.

---

## 📖 DOCUMENTATION
* **Gameplay & Strategy Guide**: See [instructions.md](instructions.md) for full player instructions, controls, tool guides, and damage budget tips.
* **Credits & Attributions**: See [CREDITS.md](CREDITS.md) for asset credits, author attributions, and Sketchfab plugin licensing.

---

## 🚀 LATEST UPDATES (VERSION 1.2.0)

### 🧹 Fixed Dirt Spawning & No Floating Decals
* **Surface-Snapping Raycasts**: All dirt spots now automatically cast downward in `_ready()` to detect the exact top of tables, chairs, counters, or floors. Dirt quads snap flush (+0.003m) to the physical surface, completely eliminating floating stains.
* **Table & Chair Sponge Stains**: Added proper sticky grime and coffee mug rings directly on the **Coffee Table**, **Kitchen Bar Counter**, **Dining Chair Seat**, and **Bookshelf Shelves**.
* **Bold, High-Contrast Textures**: Overhauled `dirt_table_grime.png`, `dirt_coffee_spill.png`, and `dirt_mud_splat.png` with deep, rich coffee capillary rings, dark syrup splatters, and high-opacity stains that stand out clearly on all wood, marble, and painted surfaces.

### ⏱️ Paced & Gradual Cleaning (No Instant 100% Jump!)
* **Fixed Cleanliness Initialization**: Fixed a critical bug where `GameManager.start_game()` reset `total_dirt_spots = 0` on level load, causing the first cleaned spot to jump immediately to 100% and finish the game!
* **Deliberate Cleaning Duration**: Tuned cleaning times to a satisfying pace (~3.8s for table grime with sponge, ~3.2s for mud puddles with mop, ~2.8s for 3D trash piles with broom).
* **Live Visual & Audio Feedback**: Dirt textures smoothly fade out as you scrub, accompanied by 3D percentage indicators (`25% Cleaned`, `50% Cleaned`, `100% Cleaned`) and tactile audio feedback.

### 💥 Fixed Physics Explosions & Window Shatter Flinging
* **Debris Layer Isolation**: Broken fragments and glass shards are now spawned on `collision_layer = 0` and `collision_mask = 1`. Shards bounce realistically off floors and walls, but **never push, teleport, or fling the player character**!
* **Safe Collision Deferral**: Breaking objects and windows safely disables collisions with `set_deferred()` and physics sleep, preventing sudden velocity spikes.
* **Perimeter Boundary Barriers**: Placed tall invisible boundary walls surrounding the patio and yard so players can never be launched or fall into the endless void.
* **Fall Recovery Safety Net**: If the player ever escapes map bounds (`y < -3.5`), the system automatically resets them safely into the living room without crashing or penalizing the run.

### 💰 Damage Tracker: $?? / $2,000 (Avoid Bankruptcy!)
* **Live HUD Counter**: The HUD now prominently displays `Damage: $?? / $2,000`.
* **Dynamic Warning States**:
  * 🟢 **$0 - $599**: Green (Safe)
  * 🟠 **$600 - $1,499**: Orange (Warning)
  * 🔴 **$1,500 - $1,999**: Pulsing Red (Danger - Bankruptcy Imminent!)
  * 💀 **$2,000+**: Fired & Bankrupt (Game Over)

### 🛋️ Replaced Placeholder Assets with Stylized 3D Models
* **Custom Bookshelf** (`assets/models/bookshelf.obj`): A full multi-tier wooden bookcase with side uprights, crown cornice, 4 distinct shelves, and colorful rows of low-poly books (no more plain brown block!).
* **Custom Coffee Table** (`assets/models/coffee_table.obj`): Beveled wood tabletop, apron frame, brass-capped tapered legs, and lower magazine shelf.
* **Dining Chairs** (`assets/models/chair.obj`): Tapered legs, cross stretchers, cushioned seats, and slatted backrests.
* **Integrated 3D Props**: Replaced inline primitive cylinders with dedicated scenes for **Antique Porcelain Vases**, **Retro CRT TV**, **Table & Floor Lamps**, **Framed Paintings**, and **Drinking Glasses**.

---

## 🎮 CONTROLS QUICK REFERENCE

| Key | Action |
|:----|:-------|
| **WASD** | Move (slippery & momentum-based) |
| **Mouse** | Camera look |
| **LMB (Hold)** | Use tool (scrub, sweep, wipe) |
| **Q / 1-4** | Switch tool (`1`=Mop, `2`=Sponge, `3`=Broom, `4`=Spray) |
| **E** | Interact (slide glass doors, drink milk, right buckets, open chests) |
| **Left Shift** | Sprint (high velocity & knock-over risk!) |
| **Escape** | Pause menu |

---

## 🔌 SKETCHFAB PLUGIN USAGE

The official Godot 4 Sketchfab plugin is active in `addons/sketchfab/`.
1. In the Godot Editor, click the **Sketchfab** tab in the top workspace dock.
2. Enter your Sketchfab API token to browse and download CC-licensed 3D models.
3. Credit all imported model authors in [CREDITS.md](CREDITS.md).

---

*Mopmentum v1.2.0 — Semantic Versioning Release*
