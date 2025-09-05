from tkinter import Tk, Canvas, Text, Entry
from PIL import Image, ImageTk


# create the main Tkinter window
root = Tk()
root.title("assistant")

try:
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # create the normal and stretched avatars
    image = Image.open("smile.png")

    ratio = 4
    avatar_width = int(screen_width / ratio)
    avatar_height = int(image.height * (avatar_width / image.width))

    image.resize((avatar_width, avatar_height))
    photo_image = ImageTk.PhotoImage(image)

    # render the avatar
    canvas = Canvas(root, bg="black", width=avatar_width, height=avatar_height)
    canvas.config(highlightthickness=0)
    normal = canvas.create_image(0, 0, image=photo_image, anchor="nw")
    canvas.pack(side="bottom", fill="both", expand=True)

    x = int(screen_width - avatar_width)
    y = int(screen_height - avatar_height)

    # hides the title bar of the avatar window and ensures it is always on top of other applications
    root.overrideredirect(True)
    root.attributes('-topmost', True)
    root.focus_force()

    root.geometry(f"{avatar_width}x{avatar_height}+{x}+{y}")
    # root.wm_attributes("-transparent", "black")

except FileNotFoundError:
    exit("avatar image couldn't be opened")

root.mainloop()