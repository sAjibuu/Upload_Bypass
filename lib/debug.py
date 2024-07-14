import traceback
import os
from .alerts import error
import datetime


# Function for saving a stack trace
def save_stack_trace(debug_level, arguments, request_file):

    # Get the current directory
    current_directory = os.getcwd()
    now = datetime.datetime.now()
    current_time = now.strftime("%d.%m.%Y_%H_%M_%S")

    # Create a 'debug' directory if it doesn't exist
    debug_directory = os.path.join(current_directory, 'debug')
    if not os.path.exists(debug_directory):
        os.makedirs(debug_directory)

    # Generate a unique file name for the stack trace
    file_name = os.path.join(debug_directory, f'{current_time}_stack_trace.txt')

    if debug_level == 1:
        # Open the file in write mode
        with open(file_name, 'w') as file:
            # Use traceback module to print the stack trace to the file
            traceback.print_exc(file=file)
    else:
        # Open the file in write mode
        with open(file_name, 'w') as file:
            file.write("\nTraceback error:\n")
            # Use traceback module to print the stack trace to the file
            traceback.print_exc(file=file)
            file.write("\nUser's Arguments:\n")
            file.write(" ".join(arguments))
            file.write("\n\nUser's request file:\n")
            request_file = open(request_file, "r")
            file.write(request_file.read())
            
    error(f"Stack trace saved to: {file_name}")
