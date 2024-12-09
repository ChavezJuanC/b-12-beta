import subprocess
import os
import sys
import requests


class PreBoot:
    def __init__(self):
        pass

    def run_pre_boot(self):
        input("Please make sure ollama is running and press any key to continue.")
        print("Starting...")

        self.verify_ollama()
        self.list_avail_models()
        ##ping ollama here!!
        print("Starting B-12...")

        userInput = input("Enter to continue")

        while userInput != "":
            userInput = input("Enter to continue")

        ##start GUI
        self.boot_gui()
        ##close the script
        sys.exit()

    def verify_ollama(self):
        print("Verifying Ollama installation...")

        try:
            subprocess.run(
                ["ollama", "--version"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            print("Validation Completed")
            return True

        except subprocess.CalledProcessError:
            print("Ollama is not installed or not recognized")
            print("Please install Ollama from https://ollama.com/ and try again.")
            input("Press any key to Exit")
            quit()

        except FileNotFoundError:
            print("Ollama is not installed or not found in PATH")
            print("Please install Ollama from https://ollama.com/ and try again.")
            input("Press any key to Exit")
            quit()

    ##List avail models and doubles as a ping to check ollama serve status
    def list_avail_models(self):
        try:
            models = requests.get("http://localhost:11434/api/tags")
            models.raise_for_status()
            models_list = models.json()
            model_names = [model["name"] for model in models_list["models"]]
            return model_names

        except Exception as e:
            print(f"Error Initializing App, make sure Ollama is running and try again.")
            userInput = input("press E to exit or any other key to try again")
            if userInput.upper() == "E":
                sys.exit()
            else:
                self.list_avail_models()

    def boot_gui(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        gui_file = os.path.join(current_dir, "main.py")
        # Run the GUI file in the background using subprocess.Popen
        subprocess.Popen(["pythonw", gui_file])

    def ping_ollama(self, defaultModel):
        print(f"Pinging Ollama with model: {defaultModel}")
        pinging = True

        while pinging:
            try:
                res = requests.post(
                    "http://localhost:11434/api/generate",
                    json={"model": defaultModel},
                )
                res.raise_for_status()
                print(res.json())
                pinging = False

            except requests.exceptions.RequestException as e:
                print("Error connecting to Ollama. Please make sure it is running.")
                print(f"Details: {e}")
                choice = input("Press 'r' to retry or any other key to exit: ").lower()
                if choice != "r":
                    pinging = False


if __name__ == "__main__":
    Booter = PreBoot()
    Booter.run_pre_boot()
