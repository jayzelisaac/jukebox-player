
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\User\Documents\Dev\Tkinter-Designer-master\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("900x900")
window.configure(bg="#E5B402")


canvas = Canvas(
    window,
    bg = "#E5B402",
    height = 900,
    width = 1480,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_text(
    20.0,
    31.0,
    anchor="nw",
    text="J-Box player",
    fill="#1E1E1E",
    font=("Inter SemiBold", 40 * -1)
)

canvas.create_rectangle(
    409.0,
    275.0,
    1167.0,
    640.0,
    fill="#1E1E1E",
    outline="")

canvas.create_rectangle(
    531.7898559570312,
    575.022216796875,
    1065.64306640625,
    632.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    374.0,
    15.0,
    1196.0,
    290.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    374.0,
    622.0,
    1196.0,
    884.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    585.0,
    426.0,
    1012.0,
    488.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    521.0,
    307.0,
    1055.0,
    414.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    413.0,
    312.0,
    532.0,
    414.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    1045.0,
    312.0,
    1164.0,
    414.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    644.0,
    497.0,
    966.0,
    563.0,
    fill="#000000",
    outline="")
window.resizable(False, False)
window.mainloop()