BACKGROUND_COLOR = "#B1DDC6"
TIME_TO_FLIP = 1000

import random
from cgitb import text
from curses import flash
from email.mime import image
from multiprocessing.dummy import current_process
from tkinter import *

import pandas as pd

try:
    data = pd.read_csv("data/to_learn_cantonese.csv")
    # print(data)
except FileNotFoundError:
    data = pd.read_csv('data/cantonese.csv')


to_learn_dict = data.to_dict(orient="records")
# print(type(to_learn_dict))
known_list = []
current_card = {}

def next_card():

    # user_input_Pronunciation = user_input.get()
    # print(user_input_Pronunciation)
    # user_input.delete(0, 'end')

    global current_card,flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn_dict)    
    canvas.itemconfig(card_title,text = "Cantonese",fill="black")
    canvas.itemconfig(card_word,text=current_card["Word"],fill="black")
    canvas.itemconfig(card_back_img,image=card_front_img)

    flip_timer = window.after(500,func=flip_card)

    return current_card["Word"]


def flip_card():
    canvas.itemconfig(card_title,text = "Pronunciation",fill = "white")
    canvas.itemconfig(card_word,text=current_card["Pronunciation"],fill = "white")
    canvas.itemconfig(card_background_image,image = card_back_img)

    return current_card["Pronunciation"]


def is_known():
    known_list.append(current_card)
    to_learn_dict.remove(current_card)
    
    to_learn_df = pd.DataFrame(to_learn_dict)
    to_learn_df.to_csv('data/to_learn_cantonese.csv',index=False)

    next_card()


window = Tk()
window.title("Flashy")
window.config(padx=50,pady=50,bg=BACKGROUND_COLOR)

flip_timer = window.after(TIME_TO_FLIP,func=flip_card)

canvas = Canvas(width = 800,height=526)

card_front_img = PhotoImage(file = "images/card_front.png")
card_back_img = PhotoImage(file='images/card_back.png')
card_background_image = canvas.create_image(400,263,image = card_front_img)
canvas.config(bg = BACKGROUND_COLOR , highlightthickness=0)
canvas.grid(row = 0 , column= 0 , columnspan=3)


card_title = canvas.create_text(400,150,text="Title",font=("Ariel",40,"italic"))
card_word = canvas.create_text(400,263,text="Word",font=("Ariel",60,"bold") )

cross_image = PhotoImage(file = "images/wrong.png")
unknown_button = Button(image = cross_image,command=next_card)
unknown_button.grid(row=1,column=0)

# user_input =Entry(width=21) 
# user_input.grid(row=1,column=1)

check_image = PhotoImage(file = "images/right.png")
known_button = Button(image = check_image,command=is_known)
known_button.grid(row=1,column=2)

next_card()

window.mainloop()

known_list_df = pd.DataFrame(data=known_list)
print(known_list_df)
known_list_df.to_csv('data/known_cantonese.csv',index=False)
