import pyautogui
import keyboard
import os
import datetime

class ScreenShoooter:

    def __init__(self):
        pass

    def allocatePngDestination(self, name):
        try:
            file = "b12photos/".format(name)
            directory = os.path.dirname(file)

            if not os.path.exists(directory):
                os.makedirs(file)

        except Exception as e:
            print("Error ollacating space for file.\n{}".format(e))

    ##This function is intended to run inside a loop of some sort ex : While True: listenForScreenShot()
    def listenForScreenShot(self):
        try:
            if keyboard.read_key() == "\\":
                print("SMILEEEE")
                self.allocatePngDestination("screenshot")
                screen_shot_imgae = pyautogui.screenshot(region=(0, 0, 1470, 1030))
                screen_shot_imgae.save(
                    "Screen_Shot_{}.png".format(
                        (datetime.date.today()).strftime("%m-%d-%Y-%X")
                    )
                )
                return True
        except Exception as e:
            print("Error while taking screenshot", e)

if __name__ == "__main__":
    shooter = ScreenShoooter()
    while True:
        shooter.listenForScreenShot()
