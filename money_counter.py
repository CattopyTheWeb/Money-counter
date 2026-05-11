from pathlib import Path
import base64
from cryptography.fernet import Fernet
import time

#Asks for the users name
user = input("Who's this? (Case sensitive)\n").strip()

#Create a password to encrypt the transaction list
password = input("Please make a password or enter your existing password:\n")

#To check if this is the first time running the progam
is_first_time_running = []

#encodes the users password in base64
password_bytes = password.encode()
base64_bytes = base64.b64encode(password_bytes)
base64_string = base64_bytes.decode()


#Puts the users encrypted password in a text file
file_password_path = Path(f"{user}password.txt")
if file_password_path.is_file():
    try:
        with file_password_path.open("r", encoding="utf-8") as file:
            existing_password = file.read()
    except PermissionError:
        print(f"Permission denied: Cannot read '{file_password_path}'.")
    except OSError as e:
        print(f"OS error while reading '{file_password_path}': {e}")
else:
    print(f"The file '{file_password_path}' does not exist. Creating File...")
    is_first_time_running.append(1)
    # Create and write to the file
    with file_password_path.open('wb') as file:
        file.write(base64_string.encode('utf-8'))
    print(f"Password created successfully.")

    with file_password_path.open('r') as file:
        existing_password = file.read()

#Defines variables and actions of encrypting/decrypting the transaction file with Fernet
key_path = Path("thekey.key")
if key_path.is_file():
    try:
        with key_path.open("r", encoding="utf-8") as file:
            key = file.read()
    except PermissionError:
        print(f"Permission denied: Cannot read '{key_path}'.")
    except OSError as e:
        print(f"OS error while reading '{key_path}': {e}")
else:
    print(f"The file '{key_path}' does not exist. Creating File...")
    is_first_time_running.append(1)
    with open("thekey.key", "wb") as thekey:
        key = Fernet.generate_key()
        thekey.write(key)

def encrypt():
        with open(f"{user}TransactionList.txt", "rb") as thefile:
            contents = thefile.read()
        contents_encrypted = Fernet(key).encrypt(contents)
        with open(f"{user}TransactionList.txt", "wb") as thefile:
            thefile.write(contents_encrypted)


def decrypt():
    with open(f"{user}TransactionList.txt", "rb") as thefile:
        contents = thefile.read()
    contents_decrypted = Fernet(key).decrypt(contents)
    with open(f"{user}TransactionList.txt", "wb") as thefile:
        thefile.write(contents_decrypted)

    

# Check if transaction list file exists before opening
file_path = Path(f"{user}TransactionList.txt")
if file_path.is_file():
    try:
        with file_path.open("r", encoding="utf-8") as file:
            pass
    except PermissionError:
        print(f"Permission denied: Cannot read '{file_path}'.")
    except OSError as e:
        print(f"OS error while reading '{file_path}': {e}")
else:
    # Create the transaction file
    print(f"The file '{file_path}' does not exist. Creating File...")
    is_first_time_running.append(1)
    with file_path.open('w') as file:
        pass
    print(f"File '{file_path}' created successfully.")


#Defines the action of counting the total amount of money in the Transaction list 
def total_money(data_list):
    if not isinstance(data_list, list):
        raise TypeError("Input must be a list.")

    total = 0.0
    positive_prefix = "Amount: £"
    negative_prefix = "Amount: -£"

    for item in data_list:
        if isinstance(item, str):
            try:
                if item.startswith(positive_prefix):
                    amount_str = item[len(positive_prefix):].strip()
                    amount = float(amount_str)
                    total += amount
                elif item.startswith(negative_prefix):
                    amount_str = item[len(negative_prefix):].strip()
                    amount = float(amount_str)
                    total -= amount
                # Ignore anything else
            except ValueError:
                print(f"Warning: Could not parse amount from '{item}'")

    return total


#Defines the action of modifying the transaction history
def modify():
    name = input("What is the name of the transaction?\n")
    money = input("How much?\n")
    date = input("What is the date?\n")
    f = open(file_path, "a", encoding="utf-8")
    f.write("\n\nTransaction name: " + name + "\nAmount: " + money + "\nDate: " + date)
    f.close()
    print("Transaction has been added to your transaction history.")
    whatmore()


#Defines what to do next
def whatmore():
    whatnext = input("What do you want to do? (view/modify/exit)\n")
    if whatnext == "view":
        with file_path.open("r", encoding="utf-8") as file:
            content = file.read()
            #Calculates the total amount of money
            #The task is here to always get the latest total number
            matches = []
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    for line in file:
                        if "Amount: £" in line or "Amount: -£" in line:
                            matches.append(line.strip())
            except FileNotFoundError:
                print(f"Error: File '{file_path}' not found.")
            except PermissionError:
                print(f"Error: Permission denied for file '{file_path}'.")
            except Exception as e:
                print(f"Unexpected error: {e}")

            total = total_money(matches)
        print(f"Here is your transaction history:\n{content}")
        print(f"Total amount is: £{total:.2f}")
        whatmore()
    elif whatnext == "modify":
        modify()
    elif whatnext == "exit":
        encrypt()
        exit()
    else:
        print("Invalid Option, try again.")
        whatmore()


#Checks if the password is correct before proceeding
if base64_string == existing_password:
    if len(is_first_time_running) > 1:
        #ask the user what they want to do
        todo = input("What do you want to do? (view/modify)\n")
        if todo == "view":
            with file_path.open("r", encoding="utf-8") as file:
                content = file.read()
                #Calculates the total amount of money
                #The task is here to always get the latest total number
                matches = []
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        for line in file:
                            if "Amount: £" in line or "Amount: -£" in line:
                                matches.append(line.strip())
                except FileNotFoundError:
                    print(f"Error: File '{file_path}' not found.")
                except PermissionError:
                    print(f"Error: Permission denied for file '{file_path}'.")
                except Exception as e:
                    print(f"Unexpected error: {e}")

                total = total_money(matches)
            print(f"Here is your transaction history:\n{content}")
            print(f"Total amount is: £{total:.2f}")
            whatmore()

        elif todo == "modify":
            modify()
            whatmore()
        else:
            print("Invalid Option, try again.")
            whatmore()
    else:
        decrypt()
        #ask the user what they want to do
        todo = input("What do you want to do? (view/modify)\n")
        if todo == "view":
            with file_path.open("r", encoding="utf-8") as file:
                content = file.read()
                #Calculates the total amount of money
                #The task is here to always get the latest total number
                matches = []
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        for line in file:
                            if "Amount: £" in line or "Amount: -£" in line:
                                matches.append(line.strip())
                except FileNotFoundError:
                    print(f"Error: File '{file_path}' not found.")
                except PermissionError:
                    print(f"Error: Permission denied for file '{file_path}'.")
                except Exception as e:
                    print(f"Unexpected error: {e}")

                total = total_money(matches)
            print(f"Here is your transaction history:\n{content}")
            print(f"Total amount is: £{total:.2f}")
            whatmore()

        elif todo == "modify":
            modify()
            whatmore()
        else:
            print("Invalid Option, try again.")
            whatmore()
else:
    print("Incorrect password")
    time.sleep(5)