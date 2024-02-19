'''
Desc: This Python script is designed to automate the process of sending customized messages to multiple contacts via WhatsApp using the pywhatkit
'''


from sys import argv
import sys
from datetime import datetime
import csv
import logging
import pywhatkit as pwk
import keyboard
import time
import os

# Set up logging configuration
logging.basicConfig(level=logging.ERROR)

class ContatosFileError(FileNotFoundError):
    pass

class MensagemFileError(FileNotFoundError):
    pass

class CommandLineArgumentsError(ValueError):
    pass

class ErrorProcessingFile(ValueError):
    pass

'''
handle errors during line processing and telephone validation by raising a custom exception.
parameters:
- index (int): The index of the line being processed.
- line (str): The content of the line that caused the error.
- e (Exception): The exception that occurred during processing.
'''
def handle_error(index, line, e): # add change tel to include this
    raise ErrorProcessingFile(f"Error processing line {index + 1}: {line}. {e}")
'''
checks file type (CSV or TXT), reads data from file with two elements: a name and a telephone number.
The function processes each row, converts the telephone using change_tel() and stores the information in a list of dictionaries.
parameters: contatos_filename (str): name of the file 
returns: contato_list (lst): list of dictionaries containing the contatos name and telephone
'''
def read_contatos(contatos_filename):
    contato_list = []
    filename, file_extension = os.path.splitext(contatos_filename)  # Extract file extension from the filename
    try:
        with open(contatos_filename, 'r', encoding="utf-8") as contatos_file:
            if file_extension.lower() == '.csv':  # Check the file extension
                csv_reader = csv.reader(contatos_file)  # If it's a CSV file, use csv.reader to iterate through rows
                for index, row in enumerate(csv_reader):
                    if len(row) >= 2: # check if each line have 2 elements
                        nome, tel = row  # Extract name and telephone number from each row
                        # Convert the telephone number and create a dictionary
                        tel = change_tel(tel, index, row)
                        contato_dict = {'Nome': nome, 'Tel': tel}
                        contato_list.append(contato_dict)
                    else:
                        handle_error(index, row, ErrorProcessingFile("Each row must have 2 elements in CSV."))
            elif file_extension.lower() == '.txt':  # Check the file extension
                data = contatos_file.readlines()  # If it's a TXT file, read lines and process each line separately
                for index, line in enumerate(data):
                    parts = line.strip().split(',')  # Split the line into parts using a comma as the delimiter
                    if len(parts) >= 2: # check if each line have 2 elements
                        nome, tel = parts[0], parts[1]  # Extract name and telephone number from each part
                        # Convert the telephone number and create a dictionary
                        tel = change_tel(tel, index, row)
                        data_dict = {'Nome': nome, 'Tel': tel}
                        contato_list.append(data_dict)
                    else:
                        handle_error(index, row, ErrorProcessingFile("Each row must have 2 elements in TXT."))
    except FileNotFoundError as e:
        raise ContatosFileError(f"Error: File '{contatos_filename}' arquivo não encontrado{e}")

    return contato_list
'''
takes a phone number and changed to the international format, with international code (+55), regioanl code (ex: 31), 
4 digit prefix and for digint sufix. It only accepts number in the international or national format.
parameters:
- tel (string): phone number 
- index (int): The index of the line being processed.
- row (str): The content of the line that caused the error.
returns: modified_tel (str): modified phone number
'''
def change_tel(tel, index, row):
    try:
        # Remove non-numeric characters from the input string
        modified_tel = ''.join(filter(str.isdigit, tel))
        # Check if the cleaned string has the correct length for an international phone number
        if len(modified_tel) == 13 and modified_tel.startswith('55'):
            # Add '+' and remove the first digit '9' from the cleaned string
            modified_tel = '+' + modified_tel.replace('9', '', 1)
        elif len(modified_tel) == 11:
            # Check if the cleaned string has the correct length for a national phone number
            # Add '+' and remove the first digit '9' from the cleaned string
            modified_tel = '+55' + modified_tel.replace('9', '', 1)
        else:
            # If the cleaned string doesn't match any valid format, raise a custom error
            handle_error(index, row, ErrorProcessingFile(f"Invalid phone number format: '{modified_tel}'"))
    except ValueError:
        raise

    return modified_tel
'''
function to read the mensage in the txt file
parameters: mensagem_filename (str): file name
returns: mensagem (str): file content
'''
def read_mensagem(mensagem_filename):
    try:
        with open(mensagem_filename, 'r', encoding="utf-8") as mensagem_file:
            mensagem = mensagem_file.read()
    except FileNotFoundError as e:
        raise MensagemFileError(f"Error: File '{mensagem_filename}' não encontrada. {e}")

    return mensagem

'''
function to modiyt the message, replacing the ocurrances of 'name' for the contato['Nome'] and appending the modified message 
to the new list of dictionaries
parameters: 
- contatos_list (list): list of dictionaries with the contatacs 'Nome' and 'Tel'
- mensagem (str): mensage 
returns: modified_messages (list): list of dictionaries with the contatacs 'Nome', 'Tel' and the modified mensage 'Mensagem'
'''
def modify_messages(contatos_list, mensagem):
    modified_messages = []
    for contato in contatos_list:
        # Replace 'name' with the value of the 'nome' key in the mensage
        modified_message = mensagem.replace('name', contato['Nome'])
        # appending the elementos fo the contatos_list to the new list and appending the modified message
        modified_messages.append({'Nome': contato['Nome'], 'Tel': contato['Tel'], 'Mensagem': modified_message})

    return modified_messages

'''
function to send the messages to multiple contacts using pywhatkit.sendwhatmsg()
parameters: modified_message (list): list of dictionaries containing the contacts information
'''
def send_messages(modified_message):
    try:
        # Get the current date and time
        current_datetime = datetime.now()
        # Extract the hour and minute from the current time
        current_hour, upcoming_minute = current_datetime.hour, current_datetime.minute
        # 1 second time window to press 'q' to abort
        exit_time_window = 1  

        for contato in modified_message:
            # Check for key press within the time window to exit the loop
            start_time = time.time()
            print("pressione 'Q' para abortar")   
            while time.time() - start_time < exit_time_window:
                if keyboard.is_pressed('q'):
                    print("Exiting loop due to key press.")
                    exit(0)  # or break if you want to continue with the next iteration

            # extract contact information
            nome, telefone, mensagem = contato['Nome'], contato['Tel'], contato['Mensagem']
            
            # set up pwk.sendwhatmsg() to send menssage after 15 seconds and close the tab after 20 seconds
            upcoming_minute += 1 # send 1 menssage per minute
            wait_time, close_tab, close_time = 15, True, 20

            print(f"\nNome: {nome}\nNúmero do contato: {telefone}\nMensagem: {mensagem}")
            print(f"Hora de envio: {current_hour} : {upcoming_minute}\nWait time: {wait_time}\nClose tab: {close_tab}\nClose time: {close_time}")

            # send menssages
            # pwk.sendwhatmsg(telefone, mensagem, current_hour, upcoming_minute, wait_time, close_tab, close_time)

            print("Message Sent!\n")
    except RuntimeError:
        logging.error("Error in sending the message\n")
        raise RuntimeError("Unexpected runtime error")

# Check if the correct number of command-line arguments is provided
if len(argv) != 3:
    logging.error("\nPara usar digite: python wpp.py contatos.csv(or .txt) mensagem.txt\n") 
    raise CommandLineArgumentsError("Número incorreto de command-line arguments. São esperados 3")

script, contatos_filename, mensagem_filename = argv

# driver code
try:
    # call the function to read the CSV file and create the list of dictionaries
    contatos_list = read_contatos(contatos_filename)
    mensagem = read_mensagem(mensagem_filename)
    modified_message = modify_messages(contatos_list, mensagem)

    send_messages(modified_message)

except (ContatosFileError, MensagemFileError, CommandLineArgumentsError, ValueError, RuntimeError, ErrorProcessingFile) as e:
    logging.error(f"{e}")
    sys.exit(1)