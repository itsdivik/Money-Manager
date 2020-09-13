class MoneyManager():

       
    def __init__(self):
        '''Constructor to set username to '', pin_number to an empty string,
           balance to 0.0, and transaction_list to an empty list.'''
        self.u_num = ''
        self.pin_number = ''
        self.balance = ''
        self.i_rate = ''
        self.transaction_list = []
        self.amt = 0.0
        self.type = ''


    def user_details(self, unum, pinnum, bal, irate, transaction):
        '''Function to get the details about the user such as account_number, pin_number, balance, transaction_list'''
        self.u_num = unum
        self.pin_number = pinnum
        self.balance = bal
        self.i_rate = irate
        self.transaction_list = transaction



    def add_entry(self, amount, entry_type):
        '''Function to add and entry an amount to the tool. Raises an
           exception if it receives a value for amount that cannot be cast to float. Raises an exception
           if the entry_type is not valid - i.e. not food, rent, bills, entertainment or other'''
        try:
            float(amount)
            self.type = entry_type
            # if the value is successfully casted to float then passing it to the respective functions
            if self.type == "Deposit":
                self.deposit_funds(amount)
            elif self.type == "Withdraw":
                self.withdraw_funds(amount)

        except ValueError as e:
            raise e


    def deposit_funds(self, amount):
        '''Function to deposit an amount to the user balance. Raises an
           exception if it receives a value that cannot be cast to float. '''
        # casting self.balance type <class 'str'> to <class 'float'> to add the amount retrieved into the balance
        bal = float(self.balance)
        try:
            self.amt = float(amount)
            bal += self.amt
            # casting bal type <class 'float'> to <class 'str'> to save it to the account file
            self.balance = str(bal)
        except ValueError as e:
            raise e


    def withdraw_funds(self, amount):
        '''Function to withdraw an amount to the user balance. Raises an
                   exception if it receives a value that cannot be cast to float. '''
        # casting self.balance type <class 'str'> to <class 'float'> to add the amount retrieved into the balance
        bal = float(self.balance)
        try:
            self.amt = float(amount)
            if amount <= bal:
                bal -= self.amt
            else:
                raise ValueError("Overdraft!!!")
            # casting bal type <class 'float'> to <class 'str'> to save it to the account file
            self.balance = str(bal)
        except ValueError as e:
            raise e

        
    def get_transaction_string(self):
        '''Function to create and return a string of the transaction list. Each transaction
           consists of two lines - either the word "Deposit" or the entry type - food etc - on
           the first line, and then the amount deposited or entry amount on the next line.'''
        # casting self.amt type <class 'float'> to <class 'str'> for appending in the transaction_list
        self.amt = str(self.amt)

        # Appending the tuple to the transaction_list
        self.transaction_list.append((self.type, self.amt))
        return self.transaction_list


    def save_to_file(self):
        '''Function to overwrite the user text file with the current user
           details. user number, pin number, and balance (in that
           precise order) are the first four lines - there are then two lines
           per transaction as outlined in the above 'get_transaction_string'
           function.'''
        # Creating the file name with .txt extension with the current users account_id
        file = self.u_num + ".txt"

        # Trying to open the file and raising an exception if it's not found
        try:
            with open(file, "w") as user_file:
            # Writing the Object's data to the File in the exact Order
                # Writing the account_id
                user_file.write(self.u_num + "\n")
                # Writing the pin_number
                user_file.write(self.pin_number + "\n")
                # Writing the current balance
                user_file.write(self.balance + "\n")
                # Writing the interest_rate
                user_file.write(self.i_rate + "\n")

                # Writing the Updated transaction history into the File
                for t_type, amt in self.transaction_list:
                    user_file.write(t_type + "\n" + amt + "\n")
        except IOError as e:
            raise e



        
