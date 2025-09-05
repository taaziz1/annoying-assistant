from tkinter import Tk, Canvas, Text
from PIL import Image, ImageTk


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
    canvas = Canvas(root, bg="black")
    canvas.config(highlightthickness=0)
    normal = canvas.create_image(0, 0, image=photo_image, anchor="nw")
    canvas.pack(side="bottom", fill="both", expand=True)

    # render the text box above the avatar
    text = Text(canvas, bg="white", fg="black", width=30, height=1, font=("Arial", 12), wrap="word")
    text.config(highlightthickness=0)
    text.insert("end", "")
    text.pack(side="top", anchor="nw")

    # hides the title bar of the avatar window and ensures it is always on top of other applications
    root.overrideredirect(True)
    root.attributes('-topmost', True)
    root.focus_force()

    x = int(screen_width - avatar_width)
    y = int(screen_height - avatar_height)

    root.geometry(f"{avatar_width}x{avatar_height}+{x}+{y}")
    # root.wm_attributes("-transparent", "black")

except FileNotFoundError:
    exit("avatar image couldn't be opened")

root.mainloop()