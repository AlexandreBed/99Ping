import gpiod
import uinput
import time
import threading
import logging

# --- Config ---
DEBOUNCE_TIME = 0.1
LOGFILE = "/home/pi/pcfkeyboard.log"
REPEAT_DELAY = 0.5
REPEAT_RATE = 0.1

# --- Runtime state ---
pressed_keys = {}  # key -> press timestamp

# --- Button-to-key mapping ---
inputs = [
    {'chip': 'gpiochip14', 'line': 0, 'key': uinput.KEY_X},
    {'chip': 'gpiochip14', 'line': 1, 'key': uinput.KEY_C},
    {'chip': 'gpiochip14', 'line': 2, 'key': uinput.KEY_V},
    {'chip': 'gpiochip14', 'line': 3, 'key': uinput.KEY_ENTER},#not work
    {'chip': 'gpiochip14', 'line': 4, 'key': uinput.KEY_Z},
    {'chip': 'gpiochip14', 'line': 5, 'key': uinput.KEY_D},#not work
    {'chip': 'gpiochip14', 'line': 6, 'key': uinput.KEY_ENTER},
    {'chip': 'gpiochip14', 'line': 7, 'key': uinput.KEY_ENTER},# not work
    
    {'chip': 'gpiochip15', 'line': 0, 'key': uinput.KEY_RIGHT},
    {'chip': 'gpiochip15', 'line': 1, 'key': uinput.KEY_LEFT},
    {'chip': 'gpiochip15', 'line': 2, 'key': uinput.KEY_UP},
    {'chip': 'gpiochip15', 'line': 3, 'key': uinput.KEY_LEFTSHIFT},#not work
    {'chip': 'gpiochip15', 'line': 4, 'key': uinput.KEY_DOWN},
    {'chip': 'gpiochip15', 'line': 5, 'key': uinput.KEY_LEFTSHIFT},
    {'chip': 'gpiochip15', 'line': 6, 'key': uinput.KEY_A},# not work
    {'chip': 'gpiochip15', 'line': 7, 'key': uinput.KEY_L},
]

# Interrupt GPIOs (BCM numbering)
interrupt_lines = {
    'gpiochip14': 5,
    'gpiochip15': 6,
}

# --- Logging setup ---
logging.basicConfig(filename=LOGFILE, level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s')
logging.info("PCF8574 keyboard handler started.")

# Setup virtual keyboard device
device = uinput.Device([entry['key'] for entry in inputs])
logging.info("Keyboard device created")

# Setup PCF input lines
for entry in inputs:
    chip = gpiod.Chip(entry['chip'])
    line = chip.get_line(entry['line'])
    line.request(consumer="pcf-btn", type=gpiod.LINE_REQ_DIR_IN)
    entry['line_obj'] = line
    entry['last_state'] = line.get_value()
    entry['last_change'] = time.time()
    logging.info(f"Setup {entry['chip']} line {entry['line']}")

# Interrupt handler per PCF chip
def monitor_chip(chipname):
    logging.info(f"Monitoring {chipname}")
    chip = gpiod.Chip("gpiochip0")
    int_line = chip.get_line(interrupt_lines[chipname])
    int_line.request(consumer="pcf-int", type=gpiod.LINE_REQ_EV_BOTH_EDGES)

    while True:
        event = int_line.event_wait(sec=1)
        if not event:
            logging.info("..")
            continue
        int_line.event_read()

        now = time.time()
        for entry in inputs:
            if entry['chip'] != chipname:
                continue

            state = entry['line_obj'].get_value()
            if state != entry['last_state']:
                if now - entry['last_change'] >= DEBOUNCE_TIME:
                    key = entry['key']
                    if state == 0:
                        device.emit(key, 1)  # Key held down
                    else:
                        device.emit(key, 0)  # Key released

#                     if state == 0:
#                         device.emit(key, 1)
#                         time.sleep(0.01)
#                         device.emit(key, 0)

                    action = 'press' if state == 0 else 'release'
                    logging.info(f"{entry['chip']} line {entry['line']} => {action}")
                    entry['last_state'] = state
                    entry['last_change'] = now

# Auto-repeat key handler
# def repeat_worker():
#     while True:
#         now = time.time()
#         for entry in inputs:
#             key = entry['key']
#             if key in pressed_keys:
#                 press_time = pressed_keys[key]
#                 if now - press_time >= REPEAT_DELAY:
#                     device.emit(key, 1)
#                     time.sleep(0.01)  # brief press
#                     device.emit(key, 0)
#                     logging.info(f"{entry['chip']} line {entry['line']} => repeat")
#         time.sleep(REPEAT_RATE)

# Start one thread per interrupt line
for chipname in interrupt_lines:
    threading.Thread(target=monitor_chip, args=(chipname,), daemon=True).start()

# Start one repeat worker
# threading.Thread(target=repeat_worker, daemon=True).start()

# Keep the program alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    logging.info("Exiting...")
