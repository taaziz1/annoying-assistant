from tkinter import Tk, Canvas, Text, Entry
from PIL import Image, ImageTk
from time import sleep
import pyttsx3


def main():
    """controls the text-to-speech engine"""

    # initialize pyttsx3 engine
    engine = pyttsx3.init()

    # pyttsx3 relies on text-to-speech packages that are already installed on the user's
    # computer (windows has some by default), so we verify that the user has some tts package
    voices = engine.getProperty('voices')
    if len(voices) <= 0:
        exit("error: system has no text-to-speech packages installed")

    # speed up speech so it sounds more natural
    engine.setProperty('rate', 180)

    # registers a callback such that, when the tts engine begins speaking,
    # the on_start_speaking function is called
    engine.connect("started-utterance", on_start_speaking)

    # registers a callback such that, when the tts engine is done speaking,
    # the on_finish_speaking function is called
    engine.connect("finished-utterance", on_finish_speaking)

    # registers a callback such that, every time a word is spoken,
    # the on_word function is called for whatever word was read
    engine.connect("started-word", on_word)

    paragraph = ("This is a test paragraph meant to verify that text is "
                 "being spoken and rendered by the application.")

    pyttsx3.speak(paragraph)

    engine.stop()


def on_start_speaking(name: str):
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


def process_command(event=None):
    """prints out whatever the user entered"""

    print("user entered: " + user_entry.get())


# create the main Tkinter window
root = Tk()
root.title("assistant")

try:
    ratio = 4  # controls how much of the screen the avatar takes up

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # create the avatar
    image = Image.open("smile.png")
    avatar_width = int(screen_width / ratio)
    avatar_height = int(image.height * (avatar_width / image.width))
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

except FileNotFoundError:
    exit("avatar image couldn't be opened")

root.after(20, main)

root.mainloop()