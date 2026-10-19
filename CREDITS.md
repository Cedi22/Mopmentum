# MOPMENTUM — CREDITS & ATTRIBUTIONS

## Engine & Tools
* **Godot Engine 4.x** — Juan Linietsky, Ariel Manzur, and Godot Engine contributors ([godotengine.org](https://godotengine.org)). Licensed under the MIT License.
* **Sketchfab Godot Plugin** — Official Sketchfab Plugin for Godot 4.x ([github.com/sketchfab/godot-plugin](https://github.com/sketchfab/godot-plugin)). Maintained by Sketchfab, James, ajreckof, and the open-source community under the MIT License.

---

## Inspiration & Dedication
* **Bennett Foddy** — Gameplay design inspired by *Getting Over It with Bennett Foddy* (deliberate friction, wobbly physics, and comedic struggle).
* **Dani (DaniDev)** — Visual aesthetic, stylized low-poly world, milk drinking mechanics, muck mushrooms, and comedic chaos inspired by *Muck*, *Karlson*, and *Milkman Karlson*.

---

## 3D Models & Meshes
* **First-Person Rubber Cleaning Gloves** — Custom viewmodel gloves generated via `scripts/build_player_viewmodel.py`.
* **Cleaning Tools** (Mop, Broom, Scrubbing Sponge, Spray Bottle) — Custom low-poly 3D assets generated via `scripts/build_cleaning_tools.py`.
* **Custom Stylized Furniture**:
  * Bookshelf with multi-tier shelving and colorful book rows (`assets/models/bookshelf.obj`) generated via `scripts/build_custom_furniture.py`.
  * Mid-century coffee table with beveled top and magazine rack (`assets/models/coffee_table.obj`) generated via `scripts/build_custom_furniture.py`.
  * Dining / kitchen chairs with slatted backrests and cushioned seats (`assets/models/chair.obj`) generated via `scripts/build_custom_furniture.py`.
* **Environment & Breakables**:
  * Porcelain Vase, Table Lamp, Flat CRT TV, Drinking Glass, Picture Frame, Coffee Mug, Golden Trophy, Milk Carton, Wooden Barrel, Wooden Chest, Patio Fences, Muck Trees & Birch Trees — Custom 3D Wavefront models and procedural scenes.
  * Interactive Sliding Patio Glass Door & Windows — Custom transparent collision and shatter physics system (`scripts/interactive_window.gd`).

## Sketchfab Community Attribution Guidelines
When downloading 3D assets using the in-editor Sketchfab plugin (`addons/sketchfab/`), users and developers must:
1. Ensure the asset is licensed for use (e.g., CC-BY, CC0, or Royalty-Free).
2. Record the asset title, original author name, Sketchfab model URL, and license type in this file under an "External Sketchfab Assets" heading.
3. Preserve all original author notices and copyright declarations.

---

## Textures & UI Badges
* **Original Procedural Furniture Master Textures** (100% Original, Copyright-Free / CC0):
  * `bookshelf_texture.png` — High-resolution 1024x1024 master texture containing warm polished mahogany wood grain, 6 ornate gold-embossed book spines (Crimson Gold, Royal Sapphire, Emerald Forest, Antique Leather, Golden Terracotta, Midnight Violet), and textured parchment paper edges. Generated via `scripts/generate_furniture_textures.py`.
  * `chest_texture.png` — High-resolution 1024x1024 master texture featuring weathered rustic oak planks, wrought-iron metal bands with metallic rivets and drop shadows, corner brackets, and an antique brass keyhole lock plate. Generated via `scripts/generate_furniture_textures.py`.
  * `wood_warm_grain.png` — Warm wood grain texture for furniture trims and picture frames.
  * `tv_screen_retro.png` — Retro CRT phosphor scanline test pattern.
  * `painting_landscape.png` — Scenic sunset mountain lake landscape.
  * `painting_retro_milk.png` — Stylized pop-art milk carton canvas.
* **High-Resolution Transparent Dirt & Grime Decals**:
  * `dirt_mud_splat.png` — Organic mud puddle with wet sheen and satellite droplets.
  * `dirt_coffee_spill.png` — Translucent coffee/soda puddle with surface tension rim and gloss highlights.
  * `dirt_stain_grime.png` — Ingrained sticky kitchen grease and wine crust decal.
  * `dirt_dust_cluster.png` — Fluffy dust bunny cluster with lint fiber streaks.
* **3D Tool Recommendation Badges**:
  * `badge_mop.png` — Mop indicator badge.
  * `badge_broom.png` — Broom indicator badge.
  * `badge_sponge.png` — Sponge indicator badge.
  * `badge_spray.png` — Spray bottle indicator badge.

---

## Audio
* **Procedural Audio Synthesis** — Custom procedural audio generator (`scripts/procedural_audio.gd`) generating dynamic footsteps, sloshes, clatters, glass breaks, and score ticks directly in-engine.

---

## Licenses
All custom assets, scripts, and generator tools created for Mopmentum are licensed under the MIT License.
Third-party plugins and libraries retain their respective original licenses.
