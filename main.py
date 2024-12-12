import customtkinter as ctk
from ChatBubbleModule import ChatBubble
from OllamaChat import ChatService
from VisionOllamaChat import VisionChatService
import threading
import requests
from tkinter import filedialog
from PIL import Image, ImageOps, ImageFilter


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
        self.OllamaVisionLocal = VisionChatService(self.current_model)
        self.contextImg = ""
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

    def update_current_model(self, value, messageFrame, buttonList, conversationFrame):
        self.current_model = value

        if self.current_model in VisionChatService.visionModels:
            for button in buttonList:
                button.configure(state="normal")
                self.contextImg = ""
        else:
            for button in buttonList:
                button.configure(state="disabled")

        self.clear_conv_context(frame=messageFrame, conversationFrame=conversationFrame)

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
            command=lambda value: self.update_current_model(
                value,
                messageFrame=innerConversationFrame,
                buttonList=[
                    screenContextButton,
                    ImgContextButton,
                    attachmentContextButton,
                ],
                conversationFrame=conversationFrame,
            ),
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
        ##Attached Imgs
        imgsFrame = ctk.CTkFrame(
            master=UserInputSectionFrame,
            height=35,
            bg_color="white",
            fg_color="white",
        )
        imgsFrame.place(x=10, y=140)
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
                    attachmentFrame=imgsFrame,
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
                attachmentFrame=imgsFrame,
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
            master=userAttachmentButtonsFrame,
            text="IM",
            width=40,
            height=40,
            command=lambda: self.selectImageFile(attachmentFrame=imgsFrame),
        )

        ImgContextButton.place(x=0, y=45)
        attachmentContextButton = ctk.CTkButton(
            master=userAttachmentButtonsFrame,
            text="AT",
            width=40,
            height=40,
        )
        attachmentContextButton.place(x=0, y=90)
        clearContextButton = ctk.CTkButton(
            master=userAttachmentButtonsFrame,
            text="CC",
            width=40,
            height=40,
            command=lambda: self.clear_conv_context(
                frame=innerConversationFrame, conversationFrame=conversationFrame
            ),
        )
        clearContextButton.place(x=0, y=135)

        self.update_current_model(
            self.current_model,
            messageFrame=innerConversationFrame,
            buttonList=[
                screenContextButton,
                ImgContextButton,
                attachmentContextButton,
            ],
            conversationFrame=conversationFrame,
        )

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
        self.scrollToRecentMessages(conversationFrame, placement=1.0)

    def localAskOllama(self, tkMaster, prompt, conversationFrame):
        ##fetch here
        if self.current_model in VisionChatService.visionModels:
            ChatRes = self.OllamaVisionLocal.askOllamaVision(
                promptMessage=prompt,
                imageContext=[self.contextImg],  ##insert img here
            )
        else:
            ChatRes = self.OllamaChatLocal.askOllama(promptMessage=prompt)

        self.contextImg = ""
        newChatBubble = ChatBubble(
            tkMaster=tkMaster,
            color="transparent",
            text=ChatRes,
            sender="AI",
            anchorDir="w",
            sidePadding=0,
        )
        newChatBubble.createChatBubble()
        self.scrollToRecentMessages(messageFrame=conversationFrame, placement=1.0)

    def scrollToRecentMessages(self, messageFrame, placement):
        try:
            messageFrame.update_idletasks()
            messageFrame._parent_canvas.yview_moveto(placement)
        except Exception as e:
            print("Error : ", e)

    def handleUserSend(
        self, tkMaster, textProvider, conversationFrame, attachmentFrame
    ):
        ##check for image attachment
        if self.contextImg != "":
            self.includeImage(tkMaster=tkMaster, conversationFrame=conversationFrame)

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
        # reset textbox & attachments
        self.deleteAttachment(tkMaster=attachmentFrame)
        textProvider.delete("1.0", "end")
        return "break"  # Prevent the default action (moving to the next line)

    def clear_conv_context(self, frame, conversationFrame):
        self.contextImg = ""
        self.OllamaChatLocal.clear_chat_context()
        self.OllamaVisionLocal.clear_chat_context()
        self.scrollToRecentMessages(messageFrame=conversationFrame, placement=0)

        for widget in frame.winfo_children():
            widget.destroy()

    def selectImageFile(self, attachmentFrame):
        filepath = filedialog.askopenfilename(
            title="Select an image for context",
            filetypes=[
                ("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"),
                ("PNG Files", "*.png"),
                ("JPEG Files", "*.jpg;*.jpeg"),
                ("BMP Files", "*.bmp"),
                ("GIF Files", "*.gif"),
            ],
        ).replace("/", "\\\\")
        self.contextImg = filepath
        self.createAttachment(tkMaster=attachmentFrame, imgSource=filepath)

    def includeImage(self, tkMaster, conversationFrame):
        image = Image.open(self.contextImg)
        imgTk = ctk.CTkImage(image, size=(200, 200))
        imgLabel = ctk.CTkLabel(
            text="",
            master=tkMaster,
            image=imgTk,
            padx=0,
            pady=10,
            width=200,
            height=200,
            corner_radius=15,
            justify="left",
        )
        imgLabel.pack(side="top", anchor="e", padx=10, pady=10)
        self.scrollToRecentMessages(messageFrame=conversationFrame, placement=1.0)

    def createAttachment(self, tkMaster, imgSource):
        image = Image.open(imgSource)
        imgTk = ctk.CTkImage(image)
        imgLabel = ctk.CTkLabel(
            master=tkMaster,
            image=imgTk,
            height=35,
            text="",
        )
        imgLabel.place(x=0, y=0)
        deleteButton = ctk.CTkButton(
            master=tkMaster,
            text="D",
            width=15,
            height=15,
            command=lambda: self.deleteAttachmentAndClear(tkMaster=tkMaster),
        )
        deleteButton.place(x=24, y=7)

    def deleteAttachmentAndClear(self, tkMaster):
        self.deleteAttachment(tkMaster)
        self.contextImg = ""

    def deleteAttachment(self, tkMaster):
        for widget in tkMaster.winfo_children():
            widget.destroy()

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
            current_model=model_names[0],
        )
        appInstance.startMainLoop()

    except Exception as e:
        print(
            f"Error Initializing App, Please try again and make sure to run pre-boot-script.py to launch\nError:{e}"
        )


##future improvements
##clear chat and attachements of models switch
##if model in non-vision clear attachment

##diable buttons while chat is thinking
##enablethem when done
##visual!
