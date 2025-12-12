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

### 2. Install dependencies
In the terminal go to the repo directory and run this command:
```bash
pip install pynput
```

### 3. Edit the clicker configuration

```bash
python enroll_clicker.py
```
1. Run the clicker script
2. Input the clicker interval (or none to default to 0.2) in the terminal.
3. Press F10 to edit the coordinates you want your clicker to use.
4. Either manually encode the coordinates using the option C, U, and D or you record the clicks using R.
5. When choosing the record option do note that the previously saved coordinates will be overwritten.
6. Press the UP arrow to record a cursor coordinate, press the DOWN arrow to save, and press ESC to quit without saving.


### 4. Run the clicker
```bash
python enroll_clicker.py
```
1. Open the animo.sys enrollment page in your browser and navigate to add enrollment.  
2. Run the clicker script
3. Switch to the enrollment page.
4. Press **F9** to toggle clicking.  
5. Press **F10** to edit the clicker coordinates.
6. Press **ESC** to terminate the program.

---

## Helper Script: Get Mouse Coordinates

Use `get_coords.py` to find screen coordinates:

```bash
python get_coords.py
```
1. Ensure `pynput` is installed.  
2. Run the helper script:
3. Press **A** to print the current cursor coordinates to the terminal.  
4. Press **ESC** to exit the script.

---

## Notes

- Make sure your browser window is positioned consistently; the script clicks absolute screen coordinates.  
- Adjust `CLICK_INTERVAL` if the clicks are too fast or too slow for your system.  
- Always test with a small number of clicks first to avoid unintended actions.
