import customtkinter as ctk
import datetime


class ChatBubble:
    def __init__(self, tkMaster, color, text, sender, anchorDir):
        self.tkMaster = tkMaster
        self.color = color
        self.text = text
        self.sender = sender
        self.anchorDir = anchorDir
        self.timeStamp = datetime.datetime.now()

    def createChatBubble(self):
        newChatBubble = ctk.CTkLabel(
            master=self.tkMaster,
            text=self.text,
            fg_color=self.color,
            text_color="black",
            wraplength=400,
        )
        newChatBubble.pack(side="top", anchor=self.anchorDir, padx=10, pady=5)

    def createTimeStamp(self):
        date = self.timeStamp.strftime("%Y-%m-%d")
        time = self.timeStamp.strftime("%H:%M:%S")
        return [date, time]
