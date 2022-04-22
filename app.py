from tkinter import *
from chat1 import get_response, bot_name
import speech_recognition as sr
# import pyttsx3         # text to speech conversion library
# import nltk


BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"


def input_query():     # function to accept a command from the user
    recognizer = sr.Recognizer()    # recognize the speech from audio source
    mic = sr.Microphone()   # device_index=1   # sr.Microphone.list_microphone_names()
    with mic as source:   # invoke microphone on the SR package with an alias named as source
        print('start speaking....')
        recognizer.pause_threshold = 0.5    #
        recognizer.adjust_for_ambient_noise(source)
        voice = recognizer.listen(source)
        # listen method on the recognizer instant will record as transcribes from source as long as user speaks
        try:
            query = recognizer.recognize_google(voice).lower()
            # passing the voice through Google search,or,bing,etc
            # also convert the transcribed text into lower case
            print('you said....', query)
            return query
        except Exception as ex:
            print('No clue what you said: An exception', ex)


class ChatApplication:

    def __init__(self):
        self.window = Tk()
        self._setup_main_window()

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("MPI")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=870, height=550, bg=BG_COLOR)

        # head label
        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR,
                           text="Welcome", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)

        # tiny divider
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)

        # text widget
        self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)

        # scroll bar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)

        # bottom label
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)

        # message entry box
        self.msg_entry = Entry(bottom_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        # send button
        send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_GRAY,
                             command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

    def _on_enter_pressed(self, event):
        # msg = self.msg_entry.get()
        msg = input_query()
        self._insert_message(msg, "You")

    def _insert_message(self, msg, sender):
        if not msg:
            return

        self.msg_entry.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)

        msg2 = f"{bot_name}: {get_response(msg)}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)

        msg3 = f"press enter to speak\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg3)
        self.text_widget.configure(state=DISABLED)

        self.text_widget.see(END)

    def speak_start(self):
        mg3 = "press enter to speak\n\n"
        self._insert_message00(mg3)

    def _insert_message00(self, msg):
        if not msg:
            return

        self.msg_entry.delete(0, END)
        # msg3 = f"start speaking"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg)
        self.text_widget.configure(state=DISABLED)

        self.text_widget.see(END)


if __name__ == "__main__":
    app = ChatApplication()
    app.speak_start()
    app.run()
