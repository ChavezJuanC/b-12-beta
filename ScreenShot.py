import pyautogui
import os
import datetime

class ScreenShoooter:

    def __init__(self):
        pass

    def allocatePngDestination(self, name):
        try:
            file = "b12ScreenShots/".format(name)
            directory = os.path.dirname(file)

            if not os.path.exists(directory):
                os.makedirs(file)

        except Exception as e:
            print("Error ollacating space for file.\n{}".format(e))

    ##This function is intended to run inside a loop of some sort ex : While True: listenForScreenShot()
    def takeScreenShot(self):
        try:
            print("SMILEEEE")
            self.allocatePngDestination("screenshot")
            screen_shot_imgae = pyautogui.screenshot(region=(0, 0, 1470, 1030))
            file_name = "b12photos\\Screen_Shot_{}.png".format(
                (datetime.datetime.now()).strftime("%m-%d-%Y-%I-%M-%S")
            )
            screen_shot_imgae.save(file_name)
            return file_name
        except Exception as e:
            print("Error while taking screenshot", e)
            return e
