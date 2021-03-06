import threading

import keyboard
import kthread
from PIL import Image
from pystray import Icon, MenuItem, Menu

from dev_autopilot import autopilot, resource_path, get_bindings, clear_input, set_scanner

STATE = 0
icon = None
thread = None

def setup(icon):
    icon.visible = True


def exit_action():
    stop_action()
    icon.visible = False
    icon.stop()


def start_action():
    stop_action()
    kthread.KThread(target=autopilot, name="EDAutopilot").start()


def stop_action():
    for thread in threading.enumerate():
        if thread.getName() == 'EDAutopilot':
            thread.kill()
    clear_input(get_bindings())


def set_state(v):
    def inner(icon, item):
        global STATE
        STATE = v
        set_scanner(STATE)

    return inner


def get_state(v):
    def inner(item):
        return STATE == v

    return inner


def tray():
    global icon, thread
    icon = None
    thread = None

    name = 'ED - Autopilot'
    icon = Icon(name=name, title=name)
    logo = Image.open(resource_path('src/logo.png'))
    icon.icon = logo

    icon.menu = Menu(
        MenuItem(
            'Scan Off',
            set_state(0),
            checked=get_state(0),
            radio=True
        ),
        MenuItem(
            'Scan on Primary Fire',
            set_state(1),
            checked=get_state(1),
            radio=True
        ),
        MenuItem(
            'Scan on Secondary Fire',
            set_state(2),
            checked=get_state(2),
            radio=True
        ),
        MenuItem('Exit', lambda: exit_action())
    )

    keyboard.add_hotkey('page up', start_action)
    keyboard.add_hotkey('page down', stop_action)

    icon.run(setup)


if __name__ == '__main__':
    tray()
