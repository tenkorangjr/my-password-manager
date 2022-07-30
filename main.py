from tkinter import *
from tkinter import messagebox
import pyperclip
import json

# ---------------------------- SEARCH METHOD ------------------------------- #


def search():
    """Search json file for website's details"""
    try:
        with open("data.json", mode="r") as file:
            # Read the json file and access the input in the website entry
            content = json.load(file)
            web_search = website_name_entry.get()

            # Show error messages when KeyError occurs
            try:
                # Access the website's details from the json dictionary
                details = content[web_search]
            # Catch the event where the website being searched does not exist
            except KeyError:
                messagebox.showwarning(title=f"{web_search.title()}", message="This website's password details does not exist!")
            else:
                messagebox.showinfo(title=f"{web_search.title()}", message=f"Email/Username: {details['email']}\nPassword: {details['password']}")

    # Display warning when file is not found
    except FileNotFoundError:
        messagebox.showwarning(message="No data file found!\nTry saving a password before searching")

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    """Generate password for My Password Manager"""
    import random
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # Select a random number of letter, numbers, and symbols
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    # Add a list of random letters, numbers and symbols in a parent list(password_list)
    password_list = []
    letters_list = [random.choice(letters) for i in range(nr_letters)]
    password_list.extend(letters_list)
    numbers_list = [random.choice(numbers) for i in range(nr_numbers)]
    password_list.extend(numbers_list)
    symbols_list = [random.choice(symbols) for i in range(nr_symbols)]
    password_list.extend(symbols_list)

    random.shuffle(password_list)  # randomise the positions of the elements in the password_list

    password = "".join(password_list)  # join the lists into a string

    password_entry.insert(0, password)  # show generated password inside the password entry space
    window.update()

    pyperclip.copy(password)  # copy password to clipboard
    messagebox.showinfo(message="Password has been copied to clipboard")

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    # Store current inputs in entries
    website = website_name_entry.get()
    username = email_entry.get()
    password = password_entry.get()

    # Save entries into a dictionary
    data = {
        website: {
            "email": username,
            "password": password,
        }
    }

    if website == "" or username == "" or password == "":  # if any of the fields are empty
        messagebox.showwarning(title="Oops", message="Please do not leave any of the fields empty!")
    else:
        save_message = messagebox.askokcancel(title=f"{website}", message="Are you sure you want to save these details")

        if save_message:
            try:
                with open("data.json", mode="r") as data_file:
                    contents = json.load(data_file)  # to read the data in json and store to contents
            except FileNotFoundError:
                contents = data
            else:
                # Check if website details already exists
                if website in contents.keys():
                    override = messagebox.askokcancel(message=f"Details for {website.title()} already exist"
                                                              f"\nDo you want to update?")

                    if override:
                        contents[website] = data[website]

                else:
                    # Update contents dictionary with new inputted data
                    contents.update(data)

            # Finally, update data.json with added details
            with open("data.json", mode="w") as data_file:
                json.dump(contents, data_file, indent=4)
                messagebox.showinfo(message="Stored Successfully")
                website_name_entry.delete(0, END)
                password_entry.delete(0, END)

                website_name_entry.focus()


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("My Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=220, height=250)
logo = PhotoImage(file="my_padlock.png")
canvas.create_image(110, 125, image=logo)
canvas.grid(row=0, column=1)

website_name_label = Label(text="Website:")
website_name_label.grid(row=1, column=0)
website_name_entry = Entry(width=22)
website_name_entry.focus()
website_name_entry.grid(row=1, column=1)
search_button = Button(text="Search", width=13, command=search)
search_button.grid(column=2, row=1)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
email_entry = Entry(width=40)
email_entry.insert(0, "tenkorangmichael@icloud.com")
email_entry.grid(row=2, column=1, columnspan=2)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)
password_entry = Entry(width=22)
password_entry.grid(row=3, column=1)
generate_password_button = Button(text="Generate Password", command=generate_password,)
generate_password_button.grid(row=3, column=2)

add_button = Button(text="Add", command=save, width=37)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
