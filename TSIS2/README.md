# TSIS 2 — Paint Application

This standalone Pygame project implements **only the TSIS 2 features**, without the Practice 10–11 shape tools.

## Run

```bash
python -m pip install pygame
python paint.py
```

Run the commands inside the `TSIS2` folder.

## Features

- **Pencil**: hold the left mouse button and move to draw continuously.
- **Line**: click, drag (live preview), release to commit the line.
- **Brush sizes**: click 2 / 5 / 10 on the toolbar or press 1 / 2 / 3.
- **Fill**: click an area to replace its connected pixels of exactly the same color.
- **Text**: click, type, press Enter to commit or Escape to cancel. Backspace removes characters.
- **Colors**: select a color from the toolbar for drawing, filling, and text.
- **Save**: press Ctrl+S to save the canvas to `saves/painting_YYYYMMDD_HHMMSS_microseconds.png`.

The `saves/` folder is created automatically. The PNG contains only the drawing canvas, not the toolbar.

## GitHub

```bash
git init
git add .
git commit -m "Implement TSIS2 Pygame drawing tools"
git branch -M main
git remote add origin YOUR_REPOSITORY_URL
git push -u origin main
```

Replace `YOUR_REPOSITORY_URL` with the URL of a repository you created on GitHub.
