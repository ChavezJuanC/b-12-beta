

In Progress

Please note that this project is still under development. Some features may not be fully implemented, and certain functionalities may change as the project evolves. We appreciate your patience and feedback as we continue to improve the application.




# Pre-Boot Script for B-12 Application

This repository contains a script that prepares the environment and automatically runs the main application. The pre-boot script will ensure that all necessary components are in place before launching the main application.

### Prerequisites

Before running the script, ensure that you have the following installed:

1. **Python 3.x** (for running the Python scripts):
   - You can download Python from [python.org](https://www.python.org/downloads/).

2. **Ollama** (for AI model integration):
   - This application uses [Ollama](https://ollama.com/) for AI models. Make sure you have it installed to run the application.
   - Download Ollama from the official website: [Ollama Download](https://ollama.com/download).

### How to Run

1. **Run the Pre-Boot Script (`pre-boot-script.py`)**:
   - The pre-boot script will start by verifying that `Ollama` is installed and will then automatically launch the `main.py` script.
   
   To run the pre-boot script, follow these steps:
   
   - Open a terminal or command prompt.
   - Navigate to the folder containing the `pre-boot-script.py` file.
   - Run the following command:
   
     ```bash
     python pre-boot-script.py
     ```

2. **What Happens Next**:
   - The `pre-boot-script.py` will:
     - Verify if `Ollama` is installed.
     - Start any necessary components for the application.
     - Automatically launch the `main.py` Python script once the environment is ready.

3. **Running the Python Script (`main.py`)**:
   - Once the pre-boot script completes, `main.py` will be launched automatically.
   - No further action is required for running `main.py` as it is handled by the pre-boot script.

### Troubleshooting

- If you encounter an error while running `pre-boot-script.py`, make sure that:
  - **Python 3.x** is installed and properly configured.
  - **Ollama** is installed and accessible in your system’s path.
  
- If the `main.py` script does not run after executing `pre-boot-script.py`, check the console output for any error messages, particularly related to `Ollama` or Python setup.

