# Enroll Clicker

A simple Python autoclicker script for automating clicks on the Animosys enrollment page.

---

## Features

- Automatically clicks a sequence of coordinates on your screen.
- Configurable click interval and coordinates.
- Helper script to easily get mouse coordinates.

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/pring-nt/Enroll_Clicker.git
cd Enroll_Clicker
```

### 2. Edit the configuration

Open `enroll_clicker.py` and set:

- `FIRST_COORD` → coordinates of the enrollment button to click.
- `CLICK_INTERVAL` (optional) → seconds between clicks.
- `other_coords` → any additional coordinates you want the script to click.

### 3. Install dependencies
In the terminal go to the repo directory and run this command:
```bash
pip install pynput
```

### 4. Run the clicker

1. Open the animo.sys enrollment page in your browser and navigate to add enrollment.  
2. Run the clicker script:
```bash
python enroll_clicker.py
```
3. Switch to the enrollment page.
4. Press **F7** to start clicking.  
5. Press **ESC** to terminate the program.

---

## Helper Script: Get Mouse Coordinates

Use `get_coords.py` to find screen coordinates:

1. Ensure `pynput` is installed.  
2. Run the helper script:
```bash
python get_coords.py
```
3. Press **A** to print the current cursor coordinates to the terminal.  
4. Press **ESC** to exit the script.

---

## Notes

- Make sure your browser window is positioned consistently; the script clicks absolute screen coordinates.  
- Adjust `CLICK_INTERVAL` if the clicks are too fast or too slow for your system.  
- Always test with a small number of clicks first to avoid unintended actions.
