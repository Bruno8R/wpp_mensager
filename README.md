 # WhatsApp Message Sender

This Python script automates the process of sending personalized messages to multiple contacts via WhatsApp using the `pywhatkit` library. It is designed to simplify the sending of customized messages by reading contact information from a CSV or TXT file and sending modified messages based on a template.

## Features

- **Contact File Compatibility:** Supports both CSV and TXT formats for storing contact information.
- **Message Customization:** Allows customization of the message content by replacing occurrences of 'name' with the actual names of the contacts.
- **International and National Phone Number Handling:** Converts telephone numbers to a standardized format, handling both international and national phone number formats.
- **Abort Option:** Provides a 1-second time window for the user to press 'q' and abort the message-sending process for each contact.

## Prerequisites

- Python 3.x
- Required Python packages: `pywhatkit`, `keyboard`

## Usage

- **contatos.csv(or .txt):** File containing contact information (name, telephone number).
- **mensagem.txt:** File containing the message template, where occurrences of 'name' will be replaced with contact names.

## Custom Exceptions

- `ContatosFileError`: Raised when the contacts file is not found.
- `MensagemFileError`: Raised when the message file is not found.
- `CommandLineArgumentsError`: Raised when an incorrect number of command-line arguments is provided.
- `ErrorProcessingFile`: Raised during line processing and telephone validation errors.

## Example

```bash
python wpp.py contacts.csv message.txt

