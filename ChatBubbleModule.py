import customtkinter as ctk
import datetime


class ChatBubble:
    def __init__(self, tkMaster, color, text, sender, anchorDir, sidePadding):
        self.tkMaster = tkMaster
        self.color = color
        self.text = text
        self.sender = sender
        self.anchorDir = anchorDir
        self.sidePadding = sidePadding
        self.timeStamp = datetime.datetime.now()

    def createChatBubble(self):
        newChatBubble = ctk.CTkLabel(
            master=self.tkMaster,
            text=self.text,
            fg_color=self.color,
            text_color="white",
            wraplength=300,
            padx=self.sidePadding,
            pady=10,
            corner_radius=15,
            justify="left"
        )
        newChatBubble.pack(side="top", anchor=self.anchorDir, padx=10, pady=10)

    def createTimeStamp(self):
        date = self.timeStamp.strftime("%Y-%m-%d")
        time = self.timeStamp.strftime("%H:%M:%S")
        return [date, time]
