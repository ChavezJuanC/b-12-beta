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
            text=self.text + str(self.createTimeStamp()),
            fg_color=self.color,
        )
        newChatBubble.pack(side="bottom", anchor=self.anchorDir)

    def createTimeStamp(self):
        date = self.timeStamp.strftime("%Y-%m-%d")
        time = self.timeStamp.strftime("%H:%M:%S")
        return [date, time]
