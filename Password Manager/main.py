from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json

FONT_NAME = "Times New Roman"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator Project
def generate_password():
    if password_input.get() == "":
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                   'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

        password_list_l = [choice(letters) for _ in range(randint(8, 10))]
        password_list_s = [choice(symbols) for _ in range(randint(2, 4))]
        password_list_n = [choice(numbers) for _ in range(randint(2, 4))]

        password_list = password_list_l + password_list_s + password_list_n
        shuffle(password_list)

        password = "".join(password_list)
        # print(password)
        password_input.insert(0, password)
        pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    user_website = website_input.get()
    user_email = email_username_input.get()
    user_password = password_input.get()
    new_data = {
        user_website: {
            "email": user_email,
            "password": user_password
        }
    }

    if user_website == "" or user_password == "":
        messagebox.showerror(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            with open("비밀번호_파일.json", "r") as password_file:
                # Reading old data
                data = json.load(password_file)

        except FileNotFoundError:
            with open("비밀번호_파일.json", "w") as password_file:
                json.dump(new_data, password_file, indent=4)

        else:
            # Updating old data
            data.update(new_data)

            # Saving updated data
            with open("비밀번호_파일.json", "w") as password_file:
                json.dump(data, password_file, indent=4)
        finally:
            website_input.delete(0, 'end')
            website_input.focus()
            password_input.delete(0, 'end')


# ---------------------------- Find_Data SETUP ------------------------------- #
def find_password():
    website = website_input.get()

    if website == "":
        messagebox.showerror(title="Oops", message="Please don't leave 'Website' field empty!")
    else:
        try:
            with open("비밀번호_파일.json", "r") as password_file:
                # Reading old data
                data = json.load(password_file)
                try:
                    email_password_dict = data[website]
                except KeyError:
                    messagebox.showerror(title="Data Not Found!", message="No details for the website exists")
                else:
                    email = email_password_dict["email"]
                    password = email_password_dict["password"]
                    # messagebox.showinfo(title=website, message=f"Email: {email} \nPassword: {password}")
                    yes = messagebox.askyesno(title=website, message=f"Email: {email} \nPassword: {password} "
                                                                     f"\nDo you want to delete entry?")
                    if yes:
                        data.pop(website)
                        with open("비밀번호_파일.json", "w") as f:
                            json.dump(data, f, indent=4)

                    pyperclip.copy(password)
        except FileNotFoundError:
            messagebox.showerror(title="Data File Not Found!", message="No Data File Found...")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200, highlightthickness=0)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

# Website label
website_label = Label(text="Website:", font=(FONT_NAME, 15, "bold"))
website_label.grid(column=0, row=1)

# Email/Username label
email_username_label = Label(text="Email/Username:", font=(FONT_NAME, 15, "bold"))
email_username_label.grid(column=0, row=2)

# Password label
password_label = Label(text="Password:", font=(FONT_NAME, 15, "bold"))
password_label.grid(column=0, row=3)

# Website_Entry
website_input = Entry(width=35)
website_input.focus()
website_input.grid(column=1, row=1)

# Email/Username_Entry
email_username_input = Entry(width=53)
email_username_input.insert(END, "abhignanrakshith@outlook.com")
email_username_input.grid(column=1, row=2, columnspan=2)

# Password_Entry
password_input = Entry(width=35)
password_input.grid(column=1, row=3)

# Search Button
search_button = Button(text="Search", width=10, command=find_password)
search_button.grid(column=2, row=1)

# Generate Password Button
generate_pass_button = Button(text="Generate Password", command=generate_password, width=14)
generate_pass_button.grid(column=2, row=3)

# Add Password Button
Add_pass_button = Button(text="Add", width=45, command=save)
Add_pass_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
