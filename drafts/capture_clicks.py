# -------------- COLLECT CLICKS FROM MOUSE --------------
# from pynput import mouse


# # Define a callback function to handle mouse clicks
# def on_click(x, y, button, pressed):
#     if pressed:
#         print(f"Mouse clicked at ({x}, {y}) with {button}")


# # Set up the listener
# with mouse.Listener(on_click=on_click) as listener:
#     print("Listening for mouse clicks. Press Ctrl+C to stop.")    
#     listener.join()

# --------------- EXECUTE CLICKS ---------------
from pynput import mouse
from pynput.mouse import Button, Controller
import time

mouse_controller = Controller()
DELAY = 0.2
LAND_CLICKS = [
    (4686, 623),
    (4763, 630),
    (4840, 630),
    (4912, 626),
    (4912, 719),
    (4834, 710),
    (4765, 710),
    (4684, 711),
    (4689, 779),
    (4754, 782),
    (4844, 774),
    (4906, 778),
    (4918, 866),
    (4831, 852),
    (4759, 853),
    (4686, 849),
    (4680, 929),
    (4747, 920),
    (4840, 928),
    (4909, 934),
    (4910, 993),
    (4832, 1016),
    (4762, 1006),
    (4701, 1005),
    (4681, 1096),
    (4761, 1081),
    (4835, 1083),
    (4912, 1083),
    (4682, 1159),
]

TREES_CLICKS = [
    (5024, 613),
    (5024, 613),
    (5024, 613),
    (5180, 621),
    (5180, 621),
    (5180, 621),
    (5325, 627),
    (5325, 627),
    (5325, 627),
    (5330, 767),
    (5330, 767),
    (5330, 767),
    (5181, 768),
    (5181, 768),
    (5181, 768),
    (5025, 765),
    (5025, 765),
    (5025, 765),
    (5024, 921),
    (5024, 921),
    (5024, 921),
    (5175, 925),
    (5175, 925),
    (5175, 925),
    (5329, 924),
    (5329, 924),
    (5329, 924),
]

current_clicks = LAND_CLICKS
# current_clicks = TREES_CLICKS


def replay_clicks():
    print("Replaying captured clicks...")
    for x, y in current_clicks:
        mouse_controller.position = (x, y)
        mouse_controller.click(Button.left, 1)
        time.sleep(DELAY)
    print("Done!")


replay_clicks()
