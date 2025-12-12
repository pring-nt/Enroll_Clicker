#!/usr/bin/env python3
import csv
import os
import threading
import time
from pynput import keyboard, mouse
from pynput.mouse import Button, Controller as MouseController

# CONFIG
CLICK_INTERVAL = float(input("Click interval (seconds, default 0.2): ") or 0.2)
CSV_FILE = "coords.csv"

# GLOBALS
mouse_ctrl = MouseController()
coords: list[tuple[int, int]] = []
clicking = False
running = True

# UTIL
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


# CSV LOAD / SAVE
def load_coords() -> list[tuple[int, int]]:
    if not os.path.exists(CSV_FILE):
        # create empty file
        open(CSV_FILE, "w").close()
        return []
    rows: list[tuple[int, int]] = []
    with open(CSV_FILE, "r", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) != 2:
                continue
            try:
                x = int(row[0])
                y = int(row[1])
                rows.append((x, y))
            except ValueError:
                continue
    return rows


def save_coords():
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        for x, y in coords:
            writer.writerow([x, y])


# DISPLAY
def show_table():
    clear_screen()
    print("---- CURRENT COORDINATES ----")
    if not coords:
        print("(no coordinates configured)")
    else:
        for idx, (x, y) in enumerate(coords):
            print(f"{idx}: ({x}, {y})")
    print("-----------------------------\n")


# RECORD MODE (overwrites CSV after finish)
def start_recording_mode():
    """
    Press LEFT MOUSE BUTTON to record current cursor position.
    Press RIGHT MOUSE BUTTON to finish and save (overwrites coords.csv).
    Press ESC to cancel (no save).
    """
    global coords

    # confirmation
    ans = input("WARNING: This will OVERWRITE coords.csv. Continue? (Y/N): ").strip().lower()
    if ans != "y":
        print("Recording cancelled.")
        time.sleep(0.6)
        return

    print("\nRecording mode: click LEFT mouse button to record position, RIGHT to finish and save, ESC to cancel.")
    print("Recorded positions will replace the current coords.csv upon finishing.\n")

    recorded: list[tuple[int, int]] = []
    cancelled = False

    # mouse listener
    def on_click(x, y, button, pressed):
        nonlocal recorded
        if pressed:
            if button == mouse.Button.left:
                recorded.append((int(x), int(y)))
                print(f"Recorded: ({x}, {y})")
            elif button == mouse.Button.right:
                # finish recording
                return False  # stop listener
        return None

    # keyboard listener (for ESC cancel)
    esc_pressed = False

    def on_press_key(key):
        nonlocal cancelled, esc_pressed
        if key == keyboard.Key.esc:
            print("Recording cancelled (ESC).")
            cancelled = True
            esc_pressed = True
            return False

    # run both listeners
    with keyboard.Listener(on_press=on_press_key) as kl:
        with mouse.Listener(on_click=on_click) as ml:
            ml.join()  # wait for mouse recording to finish
        kl.stop()  # stop keyboard listener if not already

    if cancelled or not recorded:
        print("No changes saved.")
        time.sleep(0.6)
        return

    # overwrite coords and save
    coords = recorded.copy()
    save_coords()
    print(f"Saved {len(coords)} recorded coordinates to {CSV_FILE}")
    time.sleep(0.6)


# EDIT MENU (C/U/D/R/X)

def edit_menu():
    global coords
    # pause clicking while editing
    global clicking
    clicking = False

    while True:
        show_table()
        print("--- Coordinate Editor ---")
        print("[C] Create new coordinate row")
        print("[R] Record new coordinates with UP and DOWN (overwrites CSV)")
        print("[U] Update existing row")
        print("[D] Delete row")
        print("[X] Exit editor")
        choice = input("Choose an action (C/U/D/R/X): ").strip().upper()

        if choice not in ("C", "U", "D", "R", "X"):
            print("Invalid choice. Try again.")
            time.sleep(0.6)
            continue

        if choice == "X":
            print("Exiting editor.")
            time.sleep(0.3)
            break

        if choice == "R":
            start_recording_mode()
            continue

        if choice == "C":
            try:
                sx = input("Enter X (integer): ").strip()
                sy = input("Enter Y (integer): ").strip()
                x = int(sx)
                y = int(sy)
            except ValueError:
                print("Invalid numbers. Create aborted.")
                time.sleep(0.6)
                continue
            coords.append((x, y))
            save_coords()
            print(f"Added: ({x}, {y})")
            time.sleep(0.6)
            continue

        # U or D require an index
        if not coords:
            print("No rows to update/delete.")
            time.sleep(0.6)
            continue

        try:
            idx_s = input("Enter row index: ").strip()
            idx = int(idx_s)
        except ValueError:
            print("Invalid index.")
            time.sleep(0.6)
            continue

        if idx < 0 or idx >= len(coords):
            print("Index out of range.")
            time.sleep(0.6)
            continue

        if choice == "U":
            try:
                sx = input("Enter new X (integer): ").strip()
                sy = input("Enter new Y (integer): ").strip()
                x = int(sx)
                y = int(sy)
            except ValueError:
                print("Invalid numbers. Update aborted.")
                time.sleep(0.6)
                continue
            coords[idx] = (x, y)
            save_coords()
            print(f"Row {idx} updated → ({x}, {y})")
            time.sleep(0.6)
            continue

        if choice == "D":
            deleted = coords.pop(idx)
            save_coords()
            print(f"Deleted row {idx}: {deleted}")
            time.sleep(0.6)
            continue


# CLICK LOOP
def click_loop():
    i = 0
    while running:
        if clicking and coords:
            # guard index if coords list changed size
            if i >= len(coords):
                i = 0
            mouse_ctrl.position = coords[i]
            time.sleep(0.01)
            mouse_ctrl.click(Button.left)
            i = (i + 1) % len(coords)
            time.sleep(CLICK_INTERVAL)
        else:
            time.sleep(0.05)


# KEY HANDLER (F9 toggle, F10 editor, ESC exit)
def on_press(key):
    global clicking, running
    try:
        # handle hotkeys
        if key == keyboard.Key.f9:
            clicking = not clicking
            state = "started" if clicking else "stopped"
            print(f"clicking {state}")
            return None

        if key == keyboard.Key.f10:
            # open editor (blocking)
            print("\nOpening editor...")
            edit_menu()
            print("\nReturned from editor. (press F9 to toggle clicking, ESC to exit)\n")
            return None

    except Exception:
        pass

    # ESC exits the entire program
    if key == keyboard.Key.esc:
        clicking = False
        running = False
        print("ESC pressed — exiting program.")
        return False  # stop listener
    return None


# MAIN
def main():
    global coords
    coords = load_coords()

    # start click loop thread
    t = threading.Thread(target=click_loop, daemon=True)
    t.start()

    print("Enroll Clicker (F9 toggle, F10 editor, ESC exit)")
    print(f"Loaded {len(coords)} coordinates from {CSV_FILE}")
    print("Press F9 to start/stop clicking.")
    print("Press F10 to open the coordinate editor.")
    print("Press ESC to exit.\n")

    # start keyboard listener (blocks here until ESC)
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    # cleanup
    print("shutting down...")
    # ensure click loop exits
    time.sleep(0.2)


if __name__ == "__main__":
    main()
