from tkinter import *
from random import choice
import pandas as pd

# ---------------------------- CONSTANTS ------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Ariel"
RANDON_WORD_DICT = {}

# ---------------------------- Data Extraction using Pandas ------------------------------- #
try:
    word_dataframe = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    word_dataframe = pd.read_csv("data/german_words (1-121).csv")
lang_list_dict = word_dataframe.to_dict(orient="records")


# ---------------------------- New Card ------------------------------- #
def new_card(state):
    global lang_list_dict, RANDON_WORD_DICT, word_dataframe
    wrong_button["state"] = "disabled"
    right_button["state"] = "disabled"

    if state == 1:
        lang_list_dict.remove(RANDON_WORD_DICT)
        word_dataframe = pd.DataFrame(lang_list_dict)
        word_dataframe.to_csv("data/words_to_learn.csv", index=False)

    if len(lang_list_dict) == 0:
        lang_list_dict.append({"German": "You have learned all words...", "English": "Well Done!"})
        canvas.itemconfig(word_label, font=(FONT_NAME, 25, "italic"))

    RANDON_WORD_DICT = choice(lang_list_dict)
    lang_word = RANDON_WORD_DICT["German"]

    canvas.itemconfig(canvas_image, image=card_front)
    canvas.itemconfig(language_label, text="German", fill="black")
    canvas.itemconfig(word_label, text=lang_word, fill="black")
    canvas.itemconfig(deck_size_label, text=f"Cards left: {len(lang_list_dict) + 1}", fill="black")
    window.after(3000, show_english_card, RANDON_WORD_DICT["English"])


# ---------------------------- Show English Translation ------------------------------- #

def show_english_card(eng_word):
    wrong_button["state"] = "normal"
    right_button["state"] = "normal"

    canvas.itemconfig(canvas_image, image=card_back)
    canvas.itemconfig(language_label, text="English", fill="white")
    canvas.itemconfig(word_label, text=eng_word, fill="white")
    canvas.itemconfig(deck_size_label, text=f"Cards left: {len(lang_list_dict) + 1}", fill="white")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Gateway to German Mastery")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")
canvas_image = canvas.create_image(400, 264, image=card_front)

language_label = canvas.create_text(400, 100, text="", fill="black", font=(FONT_NAME, 45, "italic"))
word_label = canvas.create_text(400, 280, text="", fill="black", font=(FONT_NAME, 60, "bold"))
deck_size_label = canvas.create_text(400, 420, text="", fill="black", font=(FONT_NAME, 20, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# Button Setup
right_img = PhotoImage(file="./images/right.png")
right_button = Button(image=right_img, highlightthickness=0, command=lambda m=1: new_card(m))
right_button.grid(column=1, row=1)

wrong_img = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, command=lambda m=0: new_card(m))
wrong_button.grid(column=0, row=1)


# ---------------------------- Main Program------------------------------- #
new_card(0)

window.mainloop()
