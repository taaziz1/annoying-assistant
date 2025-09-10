import random
import threading
import pyttsx3
import requests
import re

from tkinter import Tk, Canvas, Text, Entry
from PIL import Image, ImageTk
from time import sleep

from LLM.engine import run_command


class Assistant:

    def __init__(self):

        self.wacky_factor = 1  # determines how often random events occur, a higher value means more frequent events

        self.avatar_active = False  # keeps track of if the avatar is performing an action

        # tkinter elements
        self.root = None
        self.avatar = None
        self.text = None
        self.user_entry = None

        # screen dimensions and avatar position and dimensions
        self.screen_width = 0
        self.screen_height = 0
        self.avatar_width = 0
        self.avatar_height = 0
        self.initial_x = 0
        self.initial_y = 0

        # variables used to properly display response text
        self.i = 0
        self.original_response = []
        self.modified_response = []
        self.previous_label = "null"
        self.alreadyInserted = False

        self.create_avatar()


    def create_avatar(self):
        """creates and starts the avatar"""

        # create the main Tkinter window
        self.root = Tk()
        self.root.title("assistant")

        try:
            ratio = 3  # controls how much of the screen the avatar takes up

            self.screen_width = self.root.winfo_screenwidth()
            self.screen_height = self.root.winfo_screenheight()

            # create the avatar
            image = Image.open("smile.png")
            self.avatar_height = int(self.screen_height / ratio)
            self.avatar_width = int(image.width * (self.avatar_height / image.height))
            image = image.resize((self.avatar_width, self.avatar_height))
            photo_image = ImageTk.PhotoImage(image)

            # render the avatar
            self.avatar = Canvas(self.root, bg="black")
            self.avatar.config(highlightthickness=0)
            self.avatar.create_image(0, 0, image=photo_image, anchor="nw")
            self.avatar.pack(side="bottom", fill="both", expand=True)

            # render the text box above the avatar
            self.text = Text(self.avatar, bg="white", fg="black", width=30, height=1, font=("Arial", 12), wrap="word")
            self.text.config(highlightthickness=0)
            self.text.insert("end", "")

            # render the entry box below the avatar
            self.user_entry = Entry(self.avatar, bg="white", fg="black", width=int(self.avatar_width * 0.08), font=("Arial", 12))
            self.user_entry.bind('<Return>', self.prompt_model)
            self.user_entry.pack(side="bottom", anchor="n")

            # hides the title bar of the avatar window and ensures it is always on top of other applications
            self.root.overrideredirect(True)
            self.root.attributes('-topmost', True)
            self.root.focus_force()

            x = int(self.screen_width - self.avatar_width)
            y = int(self.screen_height - self.avatar_height)

            # moves the avatar to the bottom right of the screen
            self.root.geometry(f"{self.avatar_width}x{self.avatar_height}+{x}+{y}")
            self.root.wm_attributes("-transparent", "black")

            # allow the avatar to be dragged
            self.root.bind("<Button-1>", self.on_drag_start)
            self.root.bind("<B1-Motion>", self.on_drag_motion)

        except FileNotFoundError:
            exit("avatar image couldn't be opened")

        # separate thread to generate random events
        threading.Thread(target=self.random_event_generator).start()

        self.root.mainloop()


    def prompt_model(self, event=None):
        """feeds a prompt to the llm and the response to the text-to-speech engine"""

        if not self.avatar_active:
            # placeholder text while llm is generating a response
            self.text.insert("end", "thinking...")
            self.text.pack(side="top", anchor="n")
            self.text.update()

            # disable entry box
            self.user_entry.config(state='disabled')
            self.user_entry.update()

            # prompt llm with the user-entered text and store the response
            r = run_command(self.user_entry.get())

            # clear the placeholder text once the response has been generated
            self.text.delete(1.0, "end")

            self.narrate(r)


    def narrate(self, response, event=None):
        """controls the text-to-speech engine"""

        self.avatar_active = True

        engine = pyttsx3.init()

        # pyttsx3 relies on text-to-speech packages that are already installed on the user's
        # computer (windows has some by default), so we verify that the user has some tts package
        voices = engine.getProperty('voices')
        if len(voices) <= 0:
            exit("error: system has no text-to-speech packages installed")

        # speed up speech so it sounds more natural
        engine.setProperty('rate', 180)

        # registers a callback such that, every time a word is spoken,
        # the on_word function is called for whatever word was read
        engine.connect("started-word", self.on_word)

        # show the response box and disable the entry box while the engine is speaking
        self.text.pack(side="top", anchor="n")
        self.user_entry.config(state='disabled')

        self.i = 0
        self.original_response = response.split(' ')
        self.modified_response = re.sub(r"[.,!?;`]", "", response).split(' ')

        engine.say(response)
        engine.runAndWait()

        # enable the user entry box
        self.user_entry.config(state='normal')

        # clear the response and entry box once the response has been spoken
        self.user_entry.delete(0, "end")
        self.text.delete(1.0, "end")

        # hide the response box
        self.text.see("1.0")
        self.text.pack_forget()

        self.avatar_active = False


    def on_word(self, name: str, location: int, length: int) -> None:
        """updates the text box to show what is being spoken and
        "bounces" the avatar for every spoken word"""

        if name is not None:
            width, height, x_pos, y_pos = self.root.winfo_width(), self.root.winfo_height(), self.root.winfo_x(), self.root.winfo_y()

            # the initial and "bounced" positions
            bounce_amt = int(self.screen_height / 100)
            default_pos = f"{width}x{height}+{x_pos}+{y_pos}"
            up_pos = f"{width}x{height+bounce_amt}+{x_pos}+{y_pos-bounce_amt}"

            # adds the word that was spoken to the response box
            # utilizes a workaround to display the proper text
            if self.i < len(self.original_response):
                if self.previous_label != name:
                    self.alreadyInserted = False
                    self.text.insert("end", self.original_response[self.i] + " ")
                    self.i += 1
                elif not self.alreadyInserted:
                    self.alreadyInserted = True
                    j = self.i
                    self.i = self.modified_response.index(re.sub(r"[.,!?;`]", "", name).split(' ')[-1], self.i) + 1
                    while j < self.i:
                        self.text.insert("end", self.original_response[j] + " ")
                        j += 1
                self.previous_label = name


            # ensures that the cursor is moved to a new line when the text overflows
            self.text.see("end")
            self.text.update()

            # moves avatar up
            self.root.geometry(up_pos)
            self.root.update()
            sleep(0.05)

            # moves avatar back down
            self.root.geometry(default_pos)
            self.root.update()
            sleep(0.05)


    def on_drag_start(self, event):
        """records the position of the avatar at the start of a drag"""

        self.initial_x = event.x
        self.initial_y = event.y

    def on_drag_motion(self, event):
        """updates the position of the avatar at the end of a drag"""

        updated_x = self.root.winfo_x() + (event.x - self.initial_x)
        updated_y = self.root.winfo_y() + (event.y - self.initial_y)
        self.root.geometry(f"{self.avatar_width}x{self.avatar_height}+{updated_x}+{updated_y}")


    def random_event_generator(self):
        """randomly triggers an event"""

        while True:
            sleep(random.randint(int(15 / self.wacky_factor), int(25 / self.wacky_factor)))

            if not self.avatar_active:
                events = [self.random_fact, self.random_movement, self.disappear]
                random.choice(events)()


    def random_fact(self):
        """gets and speaks a random fact"""

        try:
            url = "https://uselessfacts.jsph.pl/random.json"
            fact = "Fun fact, " + requests.get(url).json()["text"]
            self.narrate(response=fact)
        except requests.exceptions.ConnectionError:
            self.narrate("I don't have any fun facts for you today. 😔")


    def random_movement(self):
        """moves the avatar to a random position on the screen"""

        rand_x = random.randint(0, self.screen_width - self.avatar_width)
        rand_y = random.randint(0,self. screen_height - self.avatar_height)

        self.root.geometry(f"{self.avatar_width}x{self.avatar_height}+{rand_x}+{rand_y}")
        self.root.update()


    def disappear(self):
        """hides the avatar for some amount of time before scaring the user"""

        self.root.wm_attributes("-alpha", 0.0)
        sleep(random.randint(1, 3))
        self.root.wm_attributes("-alpha", 1.0)
        self.narrate(response="BOO")


a = Assistant()