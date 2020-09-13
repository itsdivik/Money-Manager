import tkinter as tk
from tkinter import *
from tkinter import messagebox, scrolledtext

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from moneymanager import MoneyManager

win = tk.Tk()

#Set window size here to '540 x 640'
win.geometry('540x640')
win.minsize(540, 640)
win.maxsize(540, 640)

#Set the window title to 'Money Manager'
win.title("Money Manager")

#The user number and associated variable
user_number_var = tk.StringVar()

# Global variable for holding the user pin
store = ""

#This is set as a default for ease of testing
user_number_var.set('123456')
user_number_entry = tk.Entry(win, textvariable=user_number_var)
user_number_entry.focus_set()

#The pin number entry and associated variables
pin_number_var = tk.StringVar()
#This is set as a default for ease of testing
pin_number_var.set('7890')

#Modify the following to display a series of * rather than the pin ie **** not 1234
user_pin_entry = tk.Entry(win, text='PIN Number', textvariable=pin_number_var)
user_pin_entry.config(show="*")

#set the user file by default to an empty string
user_file = ''

# The balance label and associated variable
balance_var = tk.StringVar()
balance_var.set('Balance: $0.00')
balance_label = tk.Label(win, textvariable=balance_var)

# The Entry widget to accept a numerical value to deposit or withdraw
#amount_var = tk.StringVar()
tkVar = tk.StringVar()
amount_entry = tk.Entry(win, text="Enter Amount", textvariable=tkVar)
entry_type=tk.Entry(win)

# The transaction text widget holds text of the transactions
text_widget = tk.scrolledtext.ScrolledText(win, width=18, height=10)

# The money manager object we will work with
user = MoneyManager()

# ---------- Button Handlers for Login Screen ----------

def clear_pin_entry(event):
    '''Function to clear the PIN number entry when the Clear / Cancel button is clicked.'''    
    # Clear the pin number entry here
    global store
    store = ""
    pin_number_var.set('')

def handle_pin_button(num):
    '''Function to add the number of the button clicked to the PIN number entry.'''    
    # Limit to 4 chars in length
    global store
    store += str(num)
    # Set the new pin number on the pin_number_var
    if len(store) <= 4:
        pin_number_var.set(store)

def log_in(event):
    '''Function to log in to the banking system using a known user number and PIN.'''
    global user
    global user_acc
    global pin_number_var
    global user_file
    global user_num_entry
    global position
    global balance
    global i_rate
    global store
    global transaction_list

    # Variable to keep track if win still exists
    check = True

    # Temporary list to store the contents of the file
    data = []
    transaction_list = []
    acc = ''
    pin = ''

    # Retrieving the Input Given By the User
    user_acc = user_number_entry.get()
    user_num_entry = user_pin_entry.get()

    # Create the filename from the entered account number with '.txt' on the end
    file = user_acc + ".txt"
    # Try to open the account file for reading
    try:
        # Open the account file for reading
        with open(file, "r") as user_file:

            # Variable to track the position of the cursor in the file
            position = user_file.tell()
            for _ in range(4):
                data.append(read_line_from_user_file())

            print("File Read and Stored Data.....")

            # First line is account number
            acc = data[0]
            # Second line is PIN number, raise exception if the PIN entered doesn't match account PIN read
            pin = data[1]
            if user_num_entry == pin:
                # Read third and fourth lines (balance and interest rate)
                balance = data[2]
                i_rate = data[3]
                # Section to read account transactions from file
                while (True):
                    # Attempt to read a line from the account file, break if we've hit the end of the file. If we
                    # read a line then it's the transaction type, so read the next line which will be the transaction amount.
                    # and then create a tuple from both lines and add it to the account's transaction_list

                    # Checking for EOF .
                    newpos = user_file.tell()
                    if newpos == position:  # stream position hasn't changed -> EOF
                        break
                    else:
                        position = newpos

                    # if not ,then appending the type and amount tuple to the transaction_list
                    t_type = read_line_from_user_file()
                    amt = read_line_from_user_file()
                    transaction_list.append((t_type, amt))
            else:
                # Raising an Error in form via MessageBox
                messagebox.showerror('Login Error', 'Sorry! The Pin you Entered was Incorrect!!')
                print("Sorry! The Pin you Entered was Incorrect!!")
                store = []
                win.destroy()
                check = False


        # Close the file now we're finished with it
        # Removing Extra Empty tuple from the list
        if transaction_list:
            transaction_list.pop()
    # Catch exception if we couldn't open the file or PIN entered did not match account PIN
    except IOError as e:
        print("File Not Found!! ",e)
        # Show error messagebox and & reset BankAccount object to default...
        messagebox.showerror('Error', 'Account Doesn\'t Exist')
        #  ...also clear PIN entry and change focus to account number entry
        pin_number_var.set('')
        user_number_entry.focus_set()
        win.destroy()
        check = False
    # Got here without raising an exception? Then we can log in - so remove the widgets and display the account screen
    # Checking if the win still exists
    if check:
        # Using the MoneyManager object to store current users information
            # Passing the i_rate as <class> 'float'
        user.user_details(acc, pin, balance, i_rate, transaction_list)
        remove_all_widgets()
        create_user_screen()

# ---------- Button Handlers for User Screen ----------

def save_and_log_out():
    '''Function  to overwrite the user file with the current state of
       the user object (i.e. including any new transactions), remove
       all widgets and display the login screen.'''
    global user

    # Save the account with any new transactions
    user.save_to_file()
    
    # Reset the bank acount object
    user = MoneyManager()

    # Reset the account number and pin to blank
    user_number_var.set(user_acc)
    pin_number_var.set('')
    user_number_entry.focus_set()
    # Remove all widgets and display the login screen again
    remove_all_widgets()
    create_login_screen()

def perform_deposit():
    '''Function to add a deposit for the amount in the amount entry to the
       user's transaction list.'''
    global user    
    global amount_entry
    global balance_label
    global balance_var
    global text_widget
    global balance
    global tkVar

    # casting <class 'str'> to <class 'float'> for Increasing the Current Balance
    bal = float(balance)
    dep = 0.0
    # Try to increase the account balance and append the deposit to the account file
    try:
        # Get the cash amount to deposit. Note: We check legality inside account's deposit method
        deposit = amount_entry.get()

        # casting <class 'str'> to <class 'float'> to add it to the current balance
        dep = float(deposit)
        print(dep)

        # specifying the type of transaction
        entrytype = "Deposit"
        # Deposit funds
        user.add_entry(deposit, entrytype)
        # Update the transaction widget with the new transaction by calling account.get_transaction_string()
        transaction_string = user.get_transaction_string()
        # Note: Configure the text widget to be state='normal' first, then delete contents, then insert new
        #       contents, and finally configure back to state='disabled' so it cannot be user edited.
        text_widget.config(state='normal')

        text_widget.delete('1.0', END)

        for t_type, amt in transaction_string:
            text_widget.insert('insert', t_type + '\n' + amt + '\n')

        text_widget.config(state="disabled")

        bal += dep
        # casting <class 'float'> to <class 'str'> to be able  to display it in balance label
        balance = str(bal)
        # Change the balance label to reflect the new balance
        lbl = "Balance: $" + balance
        balance_var.set(lbl)
        # Clear the amount entry
        tkVar.set('')
        # Update the interest graph with our new balance
        plot_spending_graph()
    # Catch and display exception as a 'showerror' messagebox with a title of 'Transaction Error' and the text of the exception
    except:
        messagebox.showerror('Transaction Error', 'Deposit Failed')


def perform_transaction():
    '''Function to add the entry the amount in the amount entry from the user balance and add an entry to the transaction list.'''
    global user    
    global amount_entry
    global balance_label
    global balance_var
    global entry_type
    global text_widget
    global balance

    # casting <class 'str'> to <class 'float'> for Increasing the Current Balance
    bal = float(balance)
    wd = 0.0

    # Try to decrease the account balance and append the deposit to the account file
    try:
        # Get the cash amount to use. Note: We check legality inside account's withdraw_funds method
        withdraw = amount_entry.get()

        # casting <class 'str'> to <class 'float'> for Decreasing the Current Balance
        wd = float(withdraw)

        # Get the type of entry that will be added ie rent etc
        # specifying the type of transaction
        entrytype = "Withdraw"

        # Withdraw funds from the balance
        user.add_entry(wd, entrytype)
        # Update the transaction widget with the new transaction by calling user.get_transaction_string()
        transaction_string = user.get_transaction_string()
        # Note: Configure the text widget to be state='normal' first, then delete contents, then insert new
        #       contents, and finally configure back to state='disabled' so it cannot be user edited.
        text_widget.config(state='normal')

        text_widget.delete('1.0', END)

        for t_type, amt in transaction_string:
            text_widget.insert('insert', t_type + '\n' + amt + '\n')

        text_widget.config(state="disabled")

        bal -= wd
        # casting <class 'float'> to <class 'str'> to be able to display it in balance label
        balance = str(bal)
        # Change the balance label to reflect the new balance
        lbl = "Balance: $" + balance
        balance_var.set(lbl)
        # Clear the amount entry
        tkVar.set('')
        # Update the interest graph with our new balance
        plot_spending_graph()

    # Catch and display any returned exception as a messagebox 'showerror'
    except:
        messagebox.showerror('Transaction Error', 'Transaction Failed')


def remove_all_widgets():
    '''Function to remove all the widgets from the window.'''
    global win
    for widget in win.winfo_children():
        widget.grid_remove()

def read_line_from_user_file():
    '''Function to read a line from the users file but not the last newline character.
       Note: The user_file must be open to read from for this function to succeed.'''
    global user_file
    return user_file.readline()[0:-1]

def plot_spending_graph():
    '''Function to plot the user spending here.'''
    # YOUR CODE to generate the x and y lists here which will be plotted
    global balance
    global i_rate

    # casting variables from <class 'str'> to <class 'float'> to be able to perform calculations
    bal = float(balance)
    i_rate = float(i_rate)

    # Empty list to temporarily hold the first four lines of the file
    x = []

    # Appending the current balance to the list
    x.append(bal)

    # for loop to calculate the interest compounded monthly
    for _ in range(11):
        # Rate is in months, When rate is in year then effective rate = (rate/12)
            # using round to limit the decimal positions upto 2 places
        temp = round((bal * ( 1 + i_rate/1200 )), 2)
        x.append(temp)
        bal = temp

    # using list comprehension to create a list of numbers from 0 - 12
    y = [x for x in range(12)]

    #Your code to display the graph on the screen here - do this last
    f = plt.Figure(figsize = (6, 3), dpi=90)
    a = f.add_subplot(111)
    a.set_title("Cumulative Interest 12 Months", fontsize=12)
    a.grid(True, which='major', axis='both')
    a.plot(y, x,  marker='o', markerfacecolor='blue')
    a.set_xlim([0, 12])

    canvas = FigureCanvasTkAgg(f, master=win)
    canvas.get_tk_widget().grid(row=4, columnspan=3,  sticky='nsew')
    canvas.draw()




    
# ---------- UI Drawing Functions ----------

def create_login_screen():
    '''Function to create the login screen.'''    
    

    # ----- Row 0 -----

    # 'Money Manager' label here. Font size is 28.
    lb1 = tk.Label(win, text="Money Manager")
    lb1.config(font=("Arial", 28))
    lb1.grid(row=0, columnspan=3, ipadx=60, ipady=40)

    # ----- Row 1 -----

    # Acount Number / Pin label here
    lb2 = tk.Label(win, text="Account Number / PIN")
    lb2.config(font=('Arial', 10))
    lb2.grid(row=1, column=0,ipadx=14, ipady=20, padx=10, pady=10)

    # Account number entry here
    user_number_entry.grid(row=1, column=1, ipadx=30, ipady=20, sticky="news")

    # Account pin entry here
    user_pin_entry.grid(row=1, column=2, ipadx=30, ipady=20, sticky="news")
 

    # ----- Row 2 -----

    # Buttons 1, 2 and 3 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    btn1 = tk.Button(win, text="1")
    btn1.bind("<Button-1>", lambda x:handle_pin_button(1))
    btn1.grid(row=2, column=0, ipadx=42, ipady=42, sticky="news")

    btn2 = tk.Button(win, text="2")
    btn2.bind("<Button-1>", lambda x:handle_pin_button(2))
    btn2.grid(row=2, column=1, sticky="news")

    btn3 = tk.Button(win, text="3")
    btn3.bind("<Button-1>", lambda x:handle_pin_button(3))
    btn3.grid(row=2, column=2, ipadx=40, sticky="news")

    # ----- Row 3 -----

    # Buttons 4, 5 and 6 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    btn4 = tk.Button(win, text="4")
    btn4.bind("<Button-1>",lambda x:handle_pin_button(4))
    btn4.grid(row=3, column=0, ipadx=42, ipady=41, sticky="news")

    btn5 = tk.Button(win, text="5")
    btn5.bind("<Button-1>", lambda x:handle_pin_button(5))
    btn5.grid(row=3, column=1, sticky="news")

    btn6 = tk.Button(win, text="6")
    btn6.bind("<Button-1>", lambda x:handle_pin_button(6))
    btn6.grid(row=3, column=2, sticky="news")

    # ----- Row 4 -----

    # Buttons 7, 8 and 9 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    btn7 = tk.Button(win, text="7")
    btn7.bind("<Button-1>", lambda x:handle_pin_button(7))
    btn7.grid(row=4, column=0, ipadx=42, ipady=40, sticky="news")

    btn8 = tk.Button(win, text="8")
    btn8.bind("<Button-1>", lambda x:handle_pin_button(8))
    btn8.grid(row=4, column=1, sticky="news")

    btn9 = tk.Button(win, text="9")
    btn9.bind("<Button-1>", lambda x:handle_pin_button(9))
    btn9.grid(row=4, column=2, sticky="news")

    # ----- Row 5 -----

    # Cancel/Clear button here. 'bg' and 'activebackground' should be 'red'. But calls 'clear_pin_entry' function.
    btn10 = tk.Button(win, text="Cancel/Clear", bg="red", activebackground="red")
    btn10.bind("<Button-1>", clear_pin_entry)
    btn10.grid(row=5, column=0, ipadx=42, ipady=40, sticky="news")

    # Button 0 here
    btn11 = tk.Button(win, text="0")
    btn11.bind("<Button-1>", lambda x: handle_pin_button(0))
    btn11.grid(row=5, column=1, sticky="news")

    # Login button here. 'bg' and 'activebackground' should be 'green'). Button calls 'log_in' function.
    btn12 = tk.Button(win, text="Sign In", bg="green", activebackground="green")
    btn12.bind("<Button-1>", log_in)
    btn12.grid(row=5, column=2, sticky="news")

    # ----- Set column & row weights -----

    # Set column and row weights. There are 5 columns and 6 rows (0..4 and 0..5 respectively)


def create_user_screen():
    '''Function to create the user screen.'''
    global user_acc
    global amount_text
    global amount_entry
    global text_widget
    global balance_var
    global balance
    global transaction_list
    
    # ----- Row 0 -----

    # Banking label here. Font size should be 24.
    lb1 = tk.Label(win, text=" Accounting")
    lb1.config(font=("Arial", 24))
    lb1.grid(row=0, columnspan=3, ipadx=150, ipady=30, sticky="news")
    # ----- Row 1 -----

    # Account number label here
    label = "Account Number: " + user_acc
    lb2 = tk.Label(win, text=label)
    lb2.config(font=("Arial", 10), anchor='w')
    lb2.grid(row=1, column=0, padx=24, ipady=10, sticky="news")

    # Balance label here
    label2 = "Balance: $" + balance
    balance_var.set(label2)
    balance_label.config(font=("Arial", 10), anchor='w')
    balance_label.grid(row=1, column=1, padx=24, ipady=10, sticky="news")

    # Log out button here
    btn_1 = tk.Button(win, text="LogOut", command=save_and_log_out)
    btn_1.config(font=("Arial", 10))
    btn_1.grid(row=1, column=2, ipadx=50, ipady=10, sticky="news")

    # ----- Row 2 -----

    # Amount label here
    lb4 = tk.Label(win, text="Amount($)")
    lb4.config(font=('Arial', 10))
    lb4.grid(row=2, column=0, ipadx=30, ipady=10, sticky="news")

    # Amount entry here
    amount_text = tk.StringVar()
    amount_entry.grid(row=2, column=1, ipadx=30, ipady=10, sticky="news")

    # Deposit button here
    frame = tk.Frame(win)
    frame.grid(row=2, column=2)

    btn_2 = tk.Button(frame, text="Deposit", command=perform_deposit)
    btn_2.grid(row=0, column=1, ipadx=11, ipady=10, sticky="news")

    btn_3 = tk.Button(frame, text="Withdraw", command=perform_transaction)
    btn_3.grid(row=0, column=2, ipadx=10, ipady=10, sticky="news")

    # NOTE: Bind Deposit and Withdraw buttons via the command attribute to the relevant deposit and withdraw
    #       functions in this file. If we "BIND" these buttons then the button being pressed keeps looking as
    #       if it is still pressed if an exception is raised during the deposit or withdraw operation, which is
    #       offputting.
    
    
    # ----- Row 3 -----
    # Entry type label here

    # Entry drop list here

    # Add entry button here

    
    # ----- Row 4 -----

    # Declare scrollbar (text_scrollbar) here (BEFORE transaction text widget)

    # Note: Set the yscrollcommand to be 'text_scrollbar.set' here so that it actually scrolls the Text widget
    # Note: When updating the transaction text widget it must be set back to 'normal mode' (i.e. state='normal') for it to be edited


    # Now add the scrollbar and set it to change with the yview of the text widget
    for i,j in transaction_list:
        text_widget.insert('insert', i + '\n' + j + '\n')
    text_widget.grid(row=3, columnspan=3, sticky='news')
    # Add transaction Text widget and configure to be in 'disabled' mode so it cannot be edited.
    text_widget.config(state="disabled")

    # ----- Row 5 - Graph -----

    # Call plot_interest_graph() here to display the graph
    plot_spending_graph()
    

    # ----- Set column & row weights -----

    # Set column and row weights here - there are 6 rows and 5 columns (numbered 0 through 4 not 1 through 5!)




# ---------- Display Login Screen & Start Main loop ----------

create_login_screen()
win.mainloop()
