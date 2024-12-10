import ollama
import os

class VisionChatService:

    visionModels = ["llama3.2-vision:11b", "llama3.2-vision:latest"]

    def __init__(self, visionModel):
        self.visionModel = visionModel
        self.chatContext = []

    def askOllamaVision(self, promptMessage, imageContext):
        if not self.verifyImageSorce(imageContext[0]):
            return f"Could not locate image: {imageContext[0]}"
        try:
            if imageContext[0] == "":
                response = ollama.chat(
                    model=self.visionModel,
                    messages=self.chatContext
                    + [
                        {
                            "role": "user",
                            "content": promptMessage,
                        }
                    ],
                )
                self.add_history_log(res=response, promptMessage=promptMessage)

            else:
                response = ollama.chat(
                    model=self.visionModel,
                    messages=[
                        {
                            "role": "user",
                            "content": promptMessage,
                            "images": imageContext,
                        }
                    ],
                )
                self.add_history_log(
                    res=response, promptMessage=promptMessage, imageContext=imageContext
                )

            return response["message"]["content"]

        except Exception as e:
            print(f"An error occurred: {e}")
            return "Pleae make sure to have vision capeable ollama model installed and up to date running in the background (https://ollama.com/)"

    def chatInteraction(self):
        while True:
            img = input("Please provide image path:")
            ##validate ??? here???? maybe not here!!
            userPrompt = input("Ask Away:")

            if userPrompt.lower() != "/bye":
                print("Humm..")
                ollamaResponse = self.askOllamaVision(
                    promptMessage=userPrompt, imageContext=[img]
                )
                print(ollamaResponse)
            else:
                break

    def verifyImageSorce(self, imgSource):
        if os.path.exists(imgSource) or imgSource == "":
            return True
        return False

    def add_history_log(self, res, promptMessage, imageContext=None):
        self.chatContext.append(
            {"role": "user", "content": promptMessage, "images": imageContext}
        )
        ##adding the AI reponse as context
        self.chatContext.append(res["message"])

    def clear_chat_context(self):
        self.chatContext = []


if __name__ == "__main__":
    visionChat = VisionChatService(visionModel="llama3.2-vision:11b ")
    visionChat.chatInteraction()
