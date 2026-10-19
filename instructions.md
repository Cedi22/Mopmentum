# MOPMENTUM — PLAYER INSTRUCTIONS & SURVIVAL GUIDE

> *"Clean the house. Fight your own movement. Keep your total damage under $2,000."*

---

## 🎯 1. Mission Objective

You are a professional cleaner tasked with restoring an upscale summer residence and its patio deck to pristine condition within **5 minutes**. 

However, your body is completely uncoordinated: your footing is slippery, your center of gravity wobbles, and every sudden sprint carries dangerous momentum.

* **Cleanliness Goal**: Locate and clean all dirt spots throughout the house and patio to reach **100% Cleaned**.
* **Survival Constraint**: **DO NOT EXCEED $2,000 IN DAMAGES**. If your repair bill reaches $2,000, you are instantly fired and declared **BANKRUPT**!

---

## 💰 2. Damage Budget: $?? / $2,000 (Avoid Bankruptcy!)

Your HUD displays a live **Damage Tracker**:
```
Damage: $?? / $2,000
```
Every time you sprint into, strike, or knock over an item, its replacement cost is added to your bill. Keep a close eye on the HUD color code:
* 🟢 **$0 – $599 (Safe Zone)**: Minor scuffs, deposit intact.
* 🟠 **$600 – $1,499 (Warning Zone)**: Significant destruction; slow down and avoid fragile zones!
* 🔴 **$1,500 – $1,999 (Danger Zone)**: Bankruptcy imminent! One broken vase or window will end your run!
* 💥 **$2,000+ (TERMINATED)**: Instant Game Over!

### 🏷️ Replacement Cost Table (What to Avoid)

| Object | Cost | Vulnerability | Avoidance Advice |
|:-------|:----:|:--------------|:-----------------|
| **Framed Wall Painting** | **$450** | Fragile canvas | Don't swing long pole mops near walls. |
| **CRT Television** | **$400** | Heavy glass screen | Steer clear of the TV stand console. |
| **Spilled Milk Carton** | **$350** | High-value dairy | Press `[E]` to drink for a speed boost before bumping it! |
| **Golden Trophy** | **$300** | Fragile pedestal | Treat the corner display with extreme caution. |
| **Antique Porcelain Vase** | **$250** | Ultra fragile | Sits on the coffee table and bookshelf; one tap will shatter it. |
| **Patio Window / Glass Door** | **$250** | Shatterable glass | **Press `[E]` to slide the glass door open** rather than sprinting through! |
| **Floor & Table Lamp** | **$180** | Slender brass stem | Press `[E]` to toggle light; do not ram into it. |
| **Dining Chairs** | **$120** | Wooden legs | Clean the coffee stain off the seat carefully. |
| **Caution Wet Floor Sign** | **$120** | Plastic hinge | Steer around them or interact to move them. |
| **Wooden Barrel** | **$100** | Sturdy oak | Heavy, but can smash if struck with excessive speed. |
| **Drinking Glass** | **$35** | Fragile glass | Common hazard on counters and coffee tables. |
| **Coffee Mug** | **$45** | Ceramic mug | Cluttered on coffee tables. |

---

## 🧼 3. Cleaning Tools & Surface Stains

Dirt spots appear as visible 3D messes and surface stains on floors, tables, counters, and chairs. Walk within proximity of a dirt spot to see its **3D Proximity Badge** and required tool.

Cleaning is **snappy and responsive** (~1.5 to 2.0 seconds per spot). Each type of mess **strictly requires its designated tool** — using any other tool makes zero progress and will not advance or share progress.

### 🧽 Sponge (Key `2`) — Tables, Counters & Chairs ONLY
* **Required For**: Dried coffee mug rings, syrup spills, and sticky kitchen grime on furniture surfaces.
* **Locations**:
  * **Coffee Table**: Dried coffee mug rings and syrup drips.
  * **Kitchen Bar Counter**: Multiple sticky drink rings and syrup crusts.
  * **Dining Chair Seat**: Sticky coffee puddle on Chair 1.
  * **Bookshelf Shelf**: Dried stain on lower shelf.
* **Cleaning Duration**: ~2.0 seconds of circular scrubbing (must stand on top of or look directly at the stain).

### 🧹 Mop (Key `1`) — Floors & Patio ONLY
* **Required For**: Muddy footprints, thick mud puddles, and spilled milk.
* **Locations**: Living room floor, entrance hallway, patio wooden deck, outdoor mud near trees.
* **Cleaning Duration**: ~1.8 seconds of sweeping.

### 🪥 Broom (Key `3`) — Trash Piles & Debris ONLY
* **Required For**: 3D clusters of crumpled paper balls, crushed soda cans, snack wrappers, and lint.
* **Locations**: Beneath the TV stand, behind the sofa, and near the bookshelf.
* **Cleaning Duration**: ~1.6 seconds of sweeping flicks.

### 🧴 Spray Bottle (Key `4`) — Pre-treatment
* **Best Used For**: Softening tough stains.

---

## 🎮 4. Controls

| Control | Action | Details |
|:--------|:-------|:--------|
| **W, A, S, D** | Move | Slippery and wobbly; momentum takes time to stop. |
| **Mouse** | Look around | Smooth first-person camera rotation. |
| **LMB (Hold)** | Use Tool | Sweeps mop/broom or scrubs sponge in real time. |
| **Q** or **1, 2, 3, 4** | Switch Tool | `1`=Mop, `2`=Sponge, `3`=Broom, `4`=Spray. |
| **E** | Interact | Slide patio door, drink milk, open chests, turn on lamps. |
| **Left Shift** | Sprint | Drastically increases speed (`7.5 m/s`) and risk of breaking props! |
| **Escape** | Pause | Opens the pause menu and options. |

---

## 🛡️ 5. Physics & Boundary Safety

* **Safe Debris Physics**: Broken fragments and glass shards scatter realistically across the floor without pushing, flinging, or moving your character.
* **Patio Door**: Do not sprint into closed glass! Use `[E]` to slide the patio door open smoothly and step outside.
* **Map Boundaries**: Tall invisible boundary barriers enclose the patio and outdoor yard. You cannot accidentally fling or walk off into the void.
* **Fall Recovery**: In the unlikely event you escape map bounds, the system automatically detects the fall and returns you safely to the living room with zero damage penalty.

---

## 🍄 6. Mystery Mushrooms (Buffs & Debuffs)

Eating or hitting red and blue mushrooms in the yard triggers temporary side effects:
* 🏃 **Caffeine Zoomies**: Turbo speed for 15 seconds.
* ✨ **Super Suds**: 4x instant cleaning speed.
* 🦘 **Super Bounce**: Launches you into the air.
* 💰 **Cash Spores**: +$250 immediate cash tip.
* 😵 **Drunk Wobble**: Exaggerated camera roll.
* 🙃 **Inverted Brain**: Controls inverted for 8 seconds.

---

## 🎨 7. Importing 3D Assets from Sketchfab

If you wish to import additional 3D furniture, props, or decorative models into Mopmentum:
1. Open the project in the **Godot 4 Editor**.
2. Locate the **Sketchfab** tab at the top dock (enabled via `res://addons/sketchfab/`).
3. Log in with your free Sketchfab account token.
4. Browse or search for CC-licensed low-poly models (e.g., "low poly furniture", "cleaning bucket").
5. Click **Import** to download models directly into `res://assets/models/`.
6. Whenever you add new external models, please record the author and license in [CREDITS.md](CREDITS.md) and [README.md](README.md) to maintain proper human-readable attributions!
