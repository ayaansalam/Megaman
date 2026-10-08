# megaman

Small 2D platformer game like Mega Man, made with Python and pygame.

Features:
- **Physics:** gravity, friction and jumping
- **Tile collision:** check for tile collision to avoid going through walls and floors
- **Scrolling camera:** world moves, player stays centred
- **Tile map:** the map is loaded from a 2D array
- **Animations:** different player animations for standing, running, jumping and shooting
- **Shooting:** player and enemies shoot bullets
- **Enemies:**
  - *Metall*: faces you, hides when far, shoots a 3-way spread
  - *Blader*: flying patrol, 3 HP, own health bar
- **Items:** random health recovery item drops
- **Health system:** health bar and invincibility after hits
- **Game over and restart page**

To run:
```
pip install pygame-ce
python game.py
```


