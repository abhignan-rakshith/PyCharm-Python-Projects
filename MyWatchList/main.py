from tkinter import *
from datetime import date
from tkinter import messagebox
import json
import webbrowser

FONT_NAME = "Times New Roman"


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    watch_name = Name_input.get()
    watch_link = Link_input.get()
    watch_rating = Rating_input.get()
    watch_date = Date_input.get()
    watch_condition = Condition_input.get()
    new_watch = {
        watch_name: {
            "Watch_Name": watch_name,
            "Watch_Link": watch_link,
            "Watch_Rating": watch_rating,
            "Watch_Date": watch_date,
            "Watch_Condition": watch_condition
        }
    }

    if watch_name == "" or watch_rating == "" or watch_condition == "" or watch_link == "":
        messagebox.showerror(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            with open("MyWatchList.json", "r") as watch_file:
                # Reading old data
                data = json.load(watch_file)

        except FileNotFoundError:
            with open("MyWatchList.json", "w") as watch_file:
                json.dump(new_watch, watch_file, indent=4)

        else:
            # Updating old data
            data.update(new_watch)

            # Saving updated data
            with open("MyWatchList.json", "w") as watch_file:
                json.dump(data, watch_file, indent=4)
        finally:
            Name_input.delete(0, 'end')
            Name_input.focus()
            Link_input.delete(0, 'end')
            Rating_input.delete(0, 'end')
            Condition_input.delete(0, 'end')


# ---------------------------- FIND WATCH ------------------------------- #
def find_watch():
    watch_name = Name_input.get()

    if watch_name == "":
        messagebox.showerror(title="Oops", message="Please don't leave 'Watch_Name' field empty!")
    else:
        try:
            with open("MyWatchList.json", "r") as watch_file:
                # Reading old data
                data = json.load(watch_file)
                try:
                    watch_dict = data[watch_name]
                except KeyError:
                    messagebox.showerror(title="Data Not Found!", message="No details for the WATCH exists!")
                else:
                    w_name = watch_dict["Watch_Name"]
                    w_link = watch_dict["Watch_Link"]
                    w_rating = watch_dict["Watch_Rating"]
                    w_date = watch_dict["Watch_Date"]
                    w_condition = watch_dict["Watch_Condition"]
                    # messagebox.showinfo(title=website, message=f"Email: {email} \nPassword: {password}")
                    yes = messagebox.askyesno(title=watch_name,
                                              message=f"Show Name: {w_name} \nShow Rating: {w_rating} "
                                                      f"\nShow Date: {w_date} \nShow Condition: {w_condition}"
                                                      f"\nDo you want to DELETE entry?")
                    if yes:
                        data.pop(watch_name)
                        with open("MyWatchList.json", "w") as f:
                            json.dump(data, f, indent=4)

                    url = w_link
                    webbrowser.open_new_tab(url)
        except FileNotFoundError:
            messagebox.showerror(title="Data File Not Found!", message="No Data File Found...")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("MyWatchList")
window.config(padx=30, pady=30)

canvas = Canvas(height=214, width=214, highlightthickness=0)
watchlist_img = PhotoImage(file="MyWatchList_Logo.png")
canvas.create_image(107, 107, image=watchlist_img)
canvas.grid(column=1, row=0)

# Watch_Name label
watch_name_label = Label(text="Watch_Name:", font=(FONT_NAME, 15, "bold"))
watch_name_label.grid(column=0, row=1)
watch_name_label.config(pady=10)

# Watch_Link label
watch_link_label = Label(text="Watch_Link:", font=(FONT_NAME, 15, "bold"))
watch_link_label.grid(column=0, row=2)
watch_link_label.config(pady=10)

# Watch_Rating label
watch_rating_label = Label(text="Watch_Rating:", font=(FONT_NAME, 15, "bold"))
watch_rating_label.grid(column=0, row=3)
watch_rating_label.config(pady=10)

# Watch_Date label
watch_date_label = Label(text="Watch_Date:", font=(FONT_NAME, 15, "bold"))
watch_date_label.grid(column=0, row=4)

# Watch_Condition label
watch_cond_label = Label(text="Watch_Condition:", font=(FONT_NAME, 15, "bold"))
watch_cond_label.grid(column=0, row=5)

# Name_Entry
Name_input = Entry(width=35)
Name_input.focus()
Name_input.grid(column=1, row=1)

# Link_Entry
Link_input = Entry(width=35)
Link_input.grid(column=1, row=2)

# Rating_Entry
Rating_input = Entry(width=5)
Rating_input.grid(column=1, row=3)

today = date.today()
# dd/mm/YY
d1 = today.strftime("%d/%m/%Y")

# Date_Entry
Date_input = Entry(width=25)
Date_input.insert(END, d1)
Date_input.grid(column=1, row=4)

# Condition_Entry
Condition_input = Entry(width=15)
Condition_input.grid(column=1, row=5)

# Search Button
search_button = Button(text="Search", width=7, command=find_watch)
search_button.grid(column=2, row=1)

# Add/Update Button
Add_button = Button(text="Add | Update", command=save)
Add_button.grid(column=2, row=5)
Add_button.config(padx=10, pady=10)

window.mainloop()
