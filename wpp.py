from sys import argv
from datetime import datetime
import pywhatkit as pwk

# Check if the correct number of command-line arguments is provided
if len(argv) != 3:
    print("Usage: python files.py <input_filename> <output_filename>") # !! adicionar msg erro
    exit(1)

script, filename1, filename2 = argv

# Open the file for reading
with open(filename1, 'r', encoding="utf-8") as file:
    # Initialize an empty dictionary to store the data
    data_dict = {}
    
    # Read each line from the file
    for line in file:
        # Split the line into key and value using the specified delimiter
        key, value = line.strip().split(':')
        
        # Store the key-value pair in the dictionary
        data_dict[key] = value

# Open the message template file for reading
with open(filename2, 'r', encoding="utf-8") as template_file:
    # Read the message template
    message_template = template_file.read()

try:
    # Get the current date and time
    current_datetime = datetime.now()

    # Extract the hour and minute
    current_hour = current_datetime.hour
    upcoming_minute = current_datetime.minute


# Replace the placeholder "name" with the corresponding value from the dictionary

    for key, value in data_dict.items():
        modified_message = message_template.replace('name', key)

        # Remove single quotes around the value
        modified_message = modified_message.replace("'", "")

        # Append the modified message to the list
        print(modified_message, value)

        upcoming_minute += 1
        contact_no = value
        message = modified_message
        wait_time = 15 # time to wait before sending the message (minute)
        close_tab = True # close the browser tab
        close_time = 10 # time to close the tab (minute)

        print("Número do contato:", contact_no)
        print("Mensagem:", message)
        print(f"Hora de envio:, {current_hour} : {upcoming_minute}")
        print("Wait time:", wait_time)
        print("Close tab:", close_tab)
        print("Close time:", close_time)


        pwk.sendwhatmsg(contact_no, message, current_hour, upcoming_minute, wait_time, close_tab, close_time)

        print("Message Sent!") #Prints success message in console
    # error message
except:
    print("Error in sending the message")