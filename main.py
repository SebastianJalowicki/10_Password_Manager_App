from tkinter import *
from tkinter import messagebox
from random import randint, shuffle, choice
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)

    password_entry.insert(0, password)
    pyperclip.copy(password)


# ------------------------------- FIND PASSWORD --------------------------------- #

def find_password():
    website = website_entry.get()
    try:
        with open('data.json') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title='Error', message='No Data File found.')
    else:
        if website in data:
            email = data[website]['email']
            password = data[website]['password']
            messagebox.showinfo(title=website, message=f'Email: {email}\n'
                                                       f'Password: {password}')
        else:
            messagebox.showinfo(title='Error', message=f'No details for {website} exists.')


# ------------------------------- SAVE PASSWORD --------------------------------- #

def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            'email': email,
            'password': password,
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title='Ooops!', message='Please don\'t leave any fields empty!')
    else:
        try:
            with open('data.json', mode='r') as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open('data.json', mode='w') as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)
            with open('data.json', mode='w') as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# --------------------------------- UI SETUP ------------------------------------ #

window = Tk()
window.title('Password Manager')
window.config(padx=20, pady=20)

# Canvas

canvas = Canvas(width=200, height=200, highlightthickness=0)
image = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=image)
canvas.grid(column=1, row=0)

# Labels

website_label = Label(text='Website:', font=('Calibri', 10, 'bold'))
website_label.grid(column=0, row=1)
website_label.config(padx=3, pady=3)

email_label = Label(text='Email/Username:', font=('Calibri', 10, 'bold'))
email_label.grid(column=0, row=2)
email_label.config(padx=3, pady=3)

password_label = Label(text='Password:', font=('Calibri', 10, 'bold'))
password_label.grid(column=0, row=3)
password_label.config(padx=3, pady=3)

# Buttons

generate_button = Button(text='Generate Password', command=generate_password, font=('Calibri', 10, 'bold'),
                         highlightthickness=0)
generate_button.grid(column=2, row=3)
generate_button.config(padx=3, pady=3)

add_button = Button(text='Add', width=44, command=save, font=('Calibri', 10, 'bold'), highlightthickness=0)
add_button.grid(column=1, row=4, columnspan=2)
add_button.config(padx=3, pady=3)

search_button = Button(text='Search', width=15, command=find_password, font=('Calibri', 10, 'bold'),
                       highlightthickness=0)
search_button.grid(column=2, row=1)
search_button.config(padx=3, pady=3)

# Entries

website_entry = Entry(width=32)
website_entry.grid(column=1, row=1)
website_entry.focus()

email_entry = Entry(width=52)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, 'luq@email.com')

password_entry = Entry(width=32)
password_entry.grid(column=1, row=3)

window.mainloop()
