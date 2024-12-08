import subprocess
import os
import sys

class PreBoot:
    def __init__(self):
        pass

    def run_pre_boot(self):
        print("Starting pre boot...")

        try:
            self.verify_ollama()
            self.ollama_boot()
            self.pull_model_list()

        except Exception as e:
            print("Error starting app...")
            input("Press Any key to close")
            quit()

        print("Starting B-12...")

        userInput = input("Enter to continue")

        while userInput != "":
            userInput = input("Enter to continue")

        ##boot gui in a new thread
        self.boot_gui()
        ##close the script
        sys.exit()

    def verify_ollama(self):
        print("Verifying Ollama installation...")

    def ollama_boot(self):
        print("Starting Ollama...")

    def pull_model_list(self):
        print("Pulling installed models list...")

    def boot_gui(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        gui_file = os.path.join(current_dir, "main.py")

        # Run the GUI file in the background using subprocess.Popen
        subprocess.Popen(["pythonw", gui_file])


if __name__ == "__main__":
    Booter = PreBoot()
    Booter.run_pre_boot()
