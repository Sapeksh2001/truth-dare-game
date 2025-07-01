import tkinter as tk
import random
import pyttsx3
import pygame

# --- Load Prompts from Files ---
def LoadPrompts(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"File '{path}' not found.")
        return [f"(No {path} found)"]

arrTr = LoadPrompts("truth.txt")
arrDr = LoadPrompts("dare.txt")

ShuffledTruths = []
ShuffledDares = []

def GetNext(arr, pool):
    if not pool:
        pool.extend(arr)
        random.shuffle(pool)
    return pool.pop()

def DrawItem(arr, pool):
    vr = GetNext(arr, pool)
    lbl.config(text=vr)
    Announce(vr)

# --- Text-to-Speech Setup (Indian voice) ---
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for v in voices:
    if 'Indian' in v.name or 'hi' in v.id:
        engine.setProperty('voice', v.id)
        break
engine.setProperty('rate', 150)

def Announce(txt):
    engine.say(txt)
    engine.runAndWait()

# --- Background Music Setup ---
pygame.mixer.init()
try:
    pygame.mixer.music.load("erotic_music.mp3")  # Place this MP3 in the same folder
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)  # Loop indefinitely
except:
    print("Background music file not found or failed to load.")

# --- GUI Setup ---
root = tk.Tk()
root.title("Truth or Dare Spinner")
root.geometry("500x300")
root.config(bg="#1f1f1f")

# --- Display Frame ---
lbl = tk.Label(root, text="Click a button to begin!", font=("Arial", 14), fg="white", bg="#1f1f1f", wraplength=450, justify="center")
lbl.pack(pady=30)

# --- Countdown Spinner ---
def CountdownThen(callFn, seconds=2):
    lbl.config(text="Spinning...")
    root.after(seconds * 1000, callFn)

# --- Draw Functions ---
def DrawTruth():
    CountdownThen(lambda: DrawItem(arrTr, ShuffledTruths))

def DrawDare():
    CountdownThen(lambda: DrawItem(arrDr, ShuffledDares))

def DrawRandom():
    if random.choice([True, False]):
        DrawTruth()
    else:
        DrawDare()

# --- Animate Typing Effect (not used by buttons, can be added if needed) ---
def AnimateText(txt):
    lbl.config(text="")
    def Step(i=0):
        if i <= len(txt):
            lbl.config(text=txt[:i])
            root.after(20, lambda: Step(i+1))
    Step()
    Announce(txt)

# --- Buttons ---
btnFrame = tk.Frame(root, bg="#1f1f1f")
btnFrame.pack()

btnTruth = tk.Button(btnFrame, text="TRUTH", font=("Arial", 12), width=12, bg="#ff4081", fg="white", command=DrawTruth)
btnTruth.grid(row=0, column=0, padx=10, pady=10)

btnDare = tk.Button(btnFrame, text="DARE", font=("Arial", 12), width=12, bg="#7c4dff", fg="white", command=DrawDare)
btnDare.grid(row=0, column=1, padx=10, pady=10)

btnRandom = tk.Button(btnFrame, text="RANDOM", font=("Arial", 12), width=12, bg="#00bcd4", fg="white", command=DrawRandom)
btnRandom.grid(row=0, column=2, padx=10, pady=10)

# --- Reset Button (Optional) ---
def ResetPools():
    ShuffledTruths.clear()
    ShuffledDares.clear()
    lbl.config(text="Prompt pools reset!")

#btnReset = tk.Button(root, text="RESET POOLS", font=("Arial", 10), bg="#f44336", fg="white", command=ResetPools)
#btnReset.pack(pady=5)

# --- Key Bindings ---
root.bind("t", lambda e: DrawTruth())
root.bind("d", lambda e: DrawDare())
root.bind("r", lambda e: DrawRandom())

# --- Start ---
root.mainloop()
