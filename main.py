import customtkinter as ctk
from ChatBubbleModule import ChatBubble
from OllamaChat import ChatService
import threading
import requests


class App:
    def __init__(
        self,
        app_width,
        app_height,
        screen_width,
        right_side_adjuster,
        models_list,
        current_model,
    ):
        self.current_model = current_model
        self.app_width = app_width
        self.app_height = app_height
        self.screen_width = screen_width
        self.right_side_adjuster = right_side_adjuster
        self.models_list = models_list
        self.OllamaChatLocal = ChatService(self.current_model)
        self.root = ctk.CTk()
        self.root.geometry("{}x{}".format(str(self.app_width), str(self.app_height)))
        self.root.minsize(self.app_width, self.app_height)
        self.root.wm_attributes("-toolwindow", True)
        self.root.geometry(
            "+{}+{}".format(
                self.screen_width - (app_width + self.right_side_adjuster), 0
            )
        )  # Move it to the right side and top
        self.root.title("B-12 Beta")
        self.buildGUI()

    def update_current_model(self, value):
        self.current_model = value
        print(f"Current model selected: {self.current_model}")

    def buildGUI(self):

        ##App Name
        topSpacer = ctk.CTkLabel(master=self.root, height=15, text="")
        topSpacer.pack()
        appNameLabel = ctk.CTkLabel(
            master=self.root, text="B-12 AI Assistant", font=("Consolas", 25), pady=10
        )
        appNameLabel.pack()

        ##Model Selection
        modelFrame = ctk.CTkFrame(master=self.root, fg_color="transparent")
        modelFrame.pack()
        modelLabel = ctk.CTkLabel(
            master=modelFrame,
            text="Models  -",
            width=50,
            pady=5,
            padx=15,
            fg_color="transparent",
            font=("", 14),
        )
        modelLabel.grid(row=0, column=0)
        modelDropdown = ctk.CTkOptionMenu(
            master=modelFrame,
            values=self.models_list,
            corner_radius=10,
            dropdown_fg_color="white",
            dropdown_text_color="black",
            dropdown_hover_color="powderblue",
            command=lambda value: self.update_current_model(value),
        )
        modelDropdown.grid(row=0, column=1)

        ##conversation Frame

        conversationFrame = ctk.CTkScrollableFrame(
            master=self.root, width=420, height=645
        )
        conversationFrame.pack(fill="both", expand=False, padx=10, pady=10)

        innerConversationFrame = ctk.CTkFrame(
            master=conversationFrame,
            width=450,
            height=645,
            fg_color="transparent",
            bg_color="transparent",
        )
        innerConversationFrame.pack(anchor="se", expand=True, fill="x")

        ##User Input Section##
        UISectionFrame = ctk.CTkFrame(
            master=self.root, width=420, height=210, corner_radius=10, border_width=2
        )
        UISectionFrame.pack()

        UserInputSectionFrame = ctk.CTkFrame(
            master=UISectionFrame, width=360, height=180, fg_color="white"
        )

        UserInputSectionFrame.place(x=7, y=14)
        userTextInput = ctk.CTkTextbox(
            master=UserInputSectionFrame,
            width=350,
            height=135,
            padx=4,
            pady=2,
            fg_color="white",
            text_color="black",
            font=("Consolas", 15),
        )
        userTextInput.place(x=0, y=5)
        userSendButtom = ctk.CTkButton(
            master=UserInputSectionFrame,
            text="Send Promt",
            width=100,
            height=35,
            command=(
                lambda: self.handleUserSend(
                    tkMaster=innerConversationFrame,
                    textProvider=userTextInput,
                    conversationFrame=conversationFrame,
                )
            ),
        )
        userSendButtom.place(x=255, y=140)
        userTextInput.bind(
            "<Return>",
            lambda event: self.handleUserSend(
                tkMaster=innerConversationFrame,
                textProvider=userTextInput,
                conversationFrame=conversationFrame,
            ),
        )

        ##User Attachment Section
        userAttachmentButtonsFrame = ctk.CTkFrame(
            master=UISectionFrame, height=180, width=40
        )
        userAttachmentButtonsFrame.place(x=373, y=15)
        screenContextButton = ctk.CTkButton(
            master=userAttachmentButtonsFrame, text="SC", width=40, height=40
        )
        screenContextButton.place(x=0, y=0)
        ImgContextButton = ctk.CTkButton(
            master=userAttachmentButtonsFrame, text="IM", width=40, height=40
        )
        ImgContextButton.place(x=0, y=45)
        attachmentContextButton = ctk.CTkButton(
            master=userAttachmentButtonsFrame, text="AT", width=40, height=40
        )
        attachmentContextButton.place(x=0, y=90)
        clearContextButton = ctk.CTkButton(
            master=userAttachmentButtonsFrame, text="AT", width=40, height=40
        )
        clearContextButton.place(x=0, y=135)

    def spawnNewChatBubble(self, tkMaster, color, text, conversationFrame):
        newChatBubble = ChatBubble(
            tkMaster=tkMaster,
            color=color,
            text=text,
            sender="User",
            anchorDir="e",
            sidePadding=5,
        )
        newChatBubble.createChatBubble()
        self.scrollToRecentMessages(conversationFrame)

    def localAskOllama(self, tkMaster, prompt, conversationFrame):
        ##fetch here
        ChatRes = self.OllamaChatLocal.askOllama(promptMessage=prompt)
        newChatBubble = ChatBubble(
            tkMaster=tkMaster,
            color="transparent",
            text=ChatRes,
            sender="AI",
            anchorDir="w",
            sidePadding=0,
        )
        newChatBubble.createChatBubble()
        self.scrollToRecentMessages(messageFrame=conversationFrame)

    def scrollToRecentMessages(self, messageFrame):
        messageFrame.update_idletasks()
        messageFrame._parent_canvas.yview_moveto(1.0)

    def handleUserSend(self, tkMaster, textProvider, conversationFrame):
        self.spawnNewChatBubble(
            tkMaster=tkMaster,
            color="gray25",
            text=textProvider.get("1.0", "end-1c"),
            conversationFrame=conversationFrame,
        )
        # Independent Thread to avoid main thread interuption
        threading.Thread(
            target=self.localAskOllama,
            kwargs={
                "tkMaster": tkMaster,
                "prompt": textProvider.get("1.0", ctk.END),
                "conversationFrame": conversationFrame,
            },
            daemon=True,
        ).start()
        # reset textbox
        textProvider.delete("1.0", "end")
        return "break"  # Prevent the default action (moving to the next line)

    def startMainLoop(self):
        self.root.mainloop()


if __name__ == "__main__":

    try:
        models = requests.get("http://localhost:11434/api/tags")
        models.raise_for_status()
        models_list = models.json()

        model_names = [model["name"] for model in models_list["models"]]

        appInstance = App(
            app_width=450,
            app_height=1000,
            screen_width=1920,
            right_side_adjuster=8,
            models_list=model_names,
            current_model="llama3.1",
        )
        appInstance.startMainLoop()

    except Exception as e:
        print(
            f"Error Initializing App, Please try again and make sure to run pre-boot-script.py to launch\nError:{e}"
        )
