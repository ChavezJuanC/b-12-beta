import requests


class ChatService:

    def __init__(self, model):
        self.model = model
        self.chatHistory = []

    ##APi Request with History
    ##Maybe implement an option for a memory limit
    def askOllama(self, promptMessage):
        url = "http://localhost:11434/api/chat"
        payload = {
            "model": self.model,
            "messages": self.chatHistory
            + [
                {"role": "user", "content": promptMessage},
            ],
            "stream": False,
        }
        headers = {"Content-Type": "application/json"}

        try:
            APIresponse = requests.post(url, json=payload, headers=headers)

            if APIresponse.status_code == 200:
                res = APIresponse.json()
                self.add_history_log(res, promptMessage)
                print(self.chatHistory)
                return res["message"]["content"]
            else:
                return (
                    f"Error: Received unexpected status code {APIresponse.status_code}"
                )
        except Exception as e:
            print(f"An error occurred: {e}")
            return "Pleae make sure to have ollama up to date and running in the background (https://ollama.com/)"

    def add_history_log(self, res, promptMessage):
        self.chatHistory.append({"role": "user", "content": promptMessage})
        ##adding the AI reponse as context
        self.chatHistory.append(res["message"])

    def clear_chat_context(self):
        self.chatHistory = []

    ##Chat Interaction Via Terminal
    def chatInteraction(self):
        while True:
            userPrompt = input("Ask Away: ")

            if userPrompt.lower() != "/bye":
                print("Humm..")
                ollamaResponse = self.askOllama(promptMessage=userPrompt)
                print(ollamaResponse)
            else:
                break
