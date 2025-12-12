from pynput import mouse, keyboard

m = mouse.Controller()
running = True

def on_press(key):
    global running

    try:
        if key.char == 'a':  # when 'A' is pressed
            print(f"aaaaa{m.position}")
    except AttributeError:
        pass  # special keys don't have .char

    if key == keyboard.Key.esc:
        running = False
        return False
    return None


print("Press A to print mouse coordinates, ESC to quit")

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

print("stopped.")
