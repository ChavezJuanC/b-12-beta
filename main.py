import customtkinter as ctk

class App:
    def __init__(
        self, app_width, app_height, screen_width, right_side_adjuster, models_list
    ):
        self.app_width = app_width
        self.app_height = app_height
        self.screen_width = screen_width
        self.right_side_adjuster = right_side_adjuster
        self.models_list = models_list
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
        )
        modelDropdown.grid(row=0, column=1)

        ##conversation Frame
        coversationTopSpacer = ctk.CTkLabel(master=self.root, height=15, text="")
        coversationTopSpacer.pack()
        conversationFrame = ctk.CTkFrame(master=self.root, width=420, height=650)
        conversationFrame.pack()
        coversationBottomSpacer = ctk.CTkLabel(master=self.root, height=15, text="")
        coversationBottomSpacer.pack()

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
            master=UserInputSectionFrame, text="Send Promt", width=100, height=35
        )
        userSendButtom.place(x=255, y=140)

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

    def startMainLoop(self):
        self.root.mainloop()


if __name__ == "__main__":

    models = ["Ollama 3.1", "Ollama 3.2", "Ollama 3.1b"]

    appInstance = App(
        app_width=450,
        app_height=1005,
        screen_width=1920,
        right_side_adjuster=8,
        models_list=models,
    )
    appInstance.startMainLoop()
