import random
import threading
from tkinter import Tk, Canvas, Text, Entry
from PIL import Image, ImageTk
from time import sleep
import pyttsx3
import requests

from LLM import *
from LLM.engine import run_command

avatar_active = False
wacky_factor = 2    # determines how often random events occur

def process_command(event=None, response=None):
    """controls the text-to-speech engine"""

    global avatar_active

    avatar_active = True

    # initialize pyttsx3 engine
    engine = pyttsx3.init()

    # pyttsx3 relies on text-to-speech packages that are already installed on the user's
    # computer (windows has some by default), so we verify that the user has some tts package
    voices = engine.getProperty('voices')
    if len(voices) <= 0:
        exit("error: system has no text-to-speech packages installed")

    # speed up speech so it sounds more natural
    engine.setProperty('rate', 180)

    # registers a callback such that, when the tts engine is done speaking,
    # the on_finish_speaking function is called
    engine.connect("finished-utterance", on_finish_speaking)

    # registers a callback such that, every time a word is spoken,
    # the on_word function is called for whatever word was read
    engine.connect("started-word", on_word)

    on_start_speaking()

    if response is None:

        # placeholder text while llm is generating a response
        text.insert("end", "thinking...")
        text.update()

        # prompt llm with the user-entered text
        response = run_command(user_entry.get())

        # clear the placeholder text once the response has been generated
        text.delete(1.0, "end")

    pyttsx3.speak(response)

    # clear the user entry box once the response has been spoken
    user_entry.delete(0, "end")

    engine.stop()

    avatar_active = False


def on_start_speaking():
    """"shows the text box when the engine begins speaking"""

    text.pack(side="top", anchor="nw")


def on_finish_speaking(name: str, completed: bool):
    """hides and clears the text box when the engine finishes speaking"""

    if completed:
        text.delete(1.0, "end")
        text.see("1.0")
        text.pack_forget()
    else:
        print("speech terminated unexpectedly")


def on_word(name: str, location: int, length: int) -> None:
    """updates the text box to show what is being spoken and
    "bounces" the avatar for every spoken word"""

    width, height, x_pos, y_pos = root.winfo_width(), root.winfo_height(), root.winfo_x(), root.winfo_y()

    # the initial and "bounced" positions
    bounce_amt = int(screen_height / 100)
    default_pos = f"{width}x{height}+{x_pos}+{y_pos}"
    up_pos = f"{width}x{height+bounce_amt}+{x_pos}+{y_pos-bounce_amt}"

    # adds the word that was spoken to the tkinter widget to display on screen
    text.insert("end", name + " ")

    # ensures that the cursor is moved to a new line when the text overflows
    text.see("end")

    # moves avatar up
    root.geometry(up_pos)
    root.update()
    sleep(0.05)

    # moves avatar back down
    root.geometry(default_pos)
    root.update()
    sleep(0.05)

initial_x = 0
initial_y = 0

def on_drag_start(event):
    """records the position of the avatar at the start of a drag"""

    global initial_x
    global initial_y
    initial_x = event.x
    initial_y = event.y

def on_drag_motion(event):
    """updates the position of the avatar at the end of a drag"""

    updated_x = root.winfo_x() + (event.x - initial_x)
    updated_y = root.winfo_y() + (event.y - initial_y)
    root.geometry(f"{avatar_width}x{avatar_height}+{updated_x}+{updated_y}")


def random_event_generator():
    """periodically triggers a random event"""

    global avatar_active

    while True:
        sleep(random.randint(int(15 * wacky_factor), int(25 * wacky_factor)))

        if not avatar_active:
            events = [random_fact, random_movement, disappear]
            random.choice(events)()


def random_fact():
    """generates and speaks a random fact"""

    url = "https://uselessfacts.jsph.pl/random.json"
    response = "Fun fact: " + requests.get(url).json()["text"]
    process_command(response=response)


def random_movement():
    """moves the avatar to a random position on the screen"""

    rand_x = random.randint(0, screen_width - avatar_width)
    rand_y = random.randint(0, screen_height - avatar_height)

    root.geometry(f"{avatar_width}x{avatar_height}+{rand_x}+{rand_y}")
    root.update()


def disappear():
    """hides the avatar for some amount of time before scaring the user"""

    root.wm_attributes("-alpha", 0.0)
    sleep(random.randint(1, 3))
    root.wm_attributes("-alpha", 1.0)
    process_command(response="BOO")


# create the main Tkinter window
root = Tk()
root.title("assistant")

try:
    ratio = 3  # controls how much of the screen the avatar takes up

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # create the avatar
    image = Image.open("smile.png")
    avatar_height = int(screen_height / ratio)
    avatar_width = int(image.width * (avatar_height / image.height))
    image.resize((avatar_width, avatar_height))
    photo_image = ImageTk.PhotoImage(image)

    # render the avatar
    avatar = Canvas(root, bg="black")
    avatar.config(highlightthickness=0)
    normal = avatar.create_image(0, 0, image=photo_image, anchor="nw")
    avatar.pack(side="bottom", fill="both", expand=True)

    # render the text box above the avatar
    text = Text(avatar, bg="white", fg="black", width=30, height=1, font=("Arial", 12), wrap="word")
    text.config(highlightthickness=0)
    text.insert("end", "")

    # render the entry box below the avatar
    user_entry = Entry(avatar, bg="white", fg="black", width=30, font=("Arial", 12))
    user_entry.bind('<Return>', process_command)
    user_entry.pack(side="bottom", anchor="nw")

    # hides the title bar of the avatar window and ensures it is always on top of other applications
    root.overrideredirect(True)
    root.attributes('-topmost', True)
    root.focus_force()

    x = int(screen_width - avatar_width)
    y = int(screen_height - avatar_height)

    # moves the avatar to the bottom right of the screen
    root.geometry(f"{avatar_width}x{avatar_height}+{x}+{y}")
    root.wm_attributes("-transparent", "black")

    # allow the avatar to be dragged
    root.bind("<Button-1>", on_drag_start)
    root.bind("<B1-Motion>", on_drag_motion)

except FileNotFoundError:
    exit("avatar image couldn't be opened")

# separate thread to generate random events
threading.Thread(target=random_event_generator).start()

root.mainloop()