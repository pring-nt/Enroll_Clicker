from pynput.mouse import Button, Controller as MouseController
from pynput import keyboard
import threading
import time

mouse = MouseController()
coords = []

first_coord = (810, 703) # PUT HERE WHERE THE PROCEED TO STEP 2 BUTTON IS
coords.append(first_coord)

SECOND_OFFSET = (59, 51) # CALCULATE COORDINATES OF THE SECOND CLICK USING AN OFFSET
second_coord = tuple(map(int, (first_coord[0] - SECOND_OFFSET[0], first_coord[1] - SECOND_OFFSET[1])))
coords.append(second_coord)

other_coords = [(743, 606)] # ADD OTHER COORDINATES IF NECESSARY

for coord in other_coords:
    coords.append(coord)

clicking = False
running = True

def click_loop():
    i = 0
    while running:
        if clicking:
            # move to coordinate
            mouse.position = coords[i]
            time.sleep(0.01)  # tiny delay so OS catches up

            # click
            mouse.click(Button.left)

            # cycle to next coordinate
            i = (i + 1) % len(coords)

            time.sleep(0.2)  # click interval (30ms)
        else:
            time.sleep(0.05)

def on_press(key):
    global clicking, running

    if key == keyboard.Key.f7:
        clicking = True
        print("clicking started")

    elif key == keyboard.Key.esc:
        clicking = False
        running = False
        print("exiting…")
        return False  # stop keyboard listener
    return None


# start click thread
threading.Thread(target=click_loop, daemon=True).start()

print("press F7 to start clicking, ESC to stop & exit")

# keyboard listener
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
