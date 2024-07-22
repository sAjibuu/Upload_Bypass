#!/usr/bin/env python3

# Importing necessary modules and libraries
import os
from . import interactive_shell
from . import file_parser
from urllib.parse import urlparse
from .ansi_colors import *
import json
from . import config
from . import eicar_checker
from . import random_string
import datetime
from requests.exceptions import SSLError
import time


# Function to send GET request
def send_get_request(headers, options, url):
    keys_to_delete = []
    for key, value in headers.items():
        # Delete unnecessary headers except cookies and authorization header
        if key != "Cookie" and key != "Authorization" and key != "Host":
            keys_to_delete.append(key)

    # Delete unnecessary headers
    for key in keys_to_delete:
        del headers[key]

    try:
        # Send the command request to the target machine and get the response
        response = options.session.get(url, allow_redirects=False,
                                       proxies=options.proxies, headers=headers, verify=options.verify_tls)
    except SSLError:
        url = url.replace('https://', 'http://')  # Change protocol to http

        # Send the command request to the target machine and get the response
        response = options.session.get(url, allow_redirects=False, headers=headers,
                                       proxies=options.proxies, verify=False)

    return response, url


# Function to send request
def send_request(current_extension, request_file, file_name, extension_to_test, options, module, allowed_extension,
                 overall_progress, current_extension_tested=None, filename_without_nullbyte=None):
    # Check for anti-malware option and file extension
    if options.anti_malware and options.file_extension == 'com':
        # Send request with given parameters
        magic_bytes = False
        mimetype = config.mimetypes["com"]

        file_upload(request_file, file_name, extension_to_test, options,
                                                            magic_bytes, allowed_extension, mimetype, module,
                                                            overall_progress, None, None, current_extension_tested, filename_without_nullbyte)

        # Send request with allowed extension mimetype
        mimetype = config.mimetypes[allowed_extension]
        magic_bytes = False
        file_upload(request_file, file_name, extension_to_test, options,
                                                            magic_bytes, allowed_extension, mimetype, module,
                                                            overall_progress, None, None, current_extension_tested, filename_without_nullbyte)
        
    else:
        current_extension = current_extension.replace(".", "").lower()
        # Send request with given parameters
        magic_bytes = False
        mimetype = config.mimetypes[current_extension]
        
        file_upload(request_file, file_name, extension_to_test, options,
                                                            magic_bytes, allowed_extension, mimetype, module,
                                                            overall_progress, None, None, current_extension_tested, filename_without_nullbyte)

        # Send request with magic bytes of the allowed extension
        magic_bytes = config.magic_bytes[allowed_extension]
        mimetype = config.mimetypes[current_extension]
        file_upload(request_file, file_name, extension_to_test, options,
                                                            magic_bytes, allowed_extension, mimetype, module,
                                                            overall_progress, None, None, current_extension_tested, filename_without_nullbyte)

        # Send request with the allowed extension mimetype
        mimetype = config.mimetypes[allowed_extension]
        magic_bytes = False
        file_upload(request_file, file_name, extension_to_test, options,
                                                            magic_bytes, allowed_extension, mimetype, module,
                                                            overall_progress, None, None, current_extension_tested, filename_without_nullbyte)


        # Send request with the allowed extension mimetype and magic_bytes
        mimetype = config.mimetypes[allowed_extension]
        magic_bytes = config.magic_bytes[allowed_extension]
        file_upload(request_file, file_name, extension_to_test, options,
                                                            magic_bytes, allowed_extension, mimetype, module,
                                                            overall_progress, None, None, current_extension_tested, filename_without_nullbyte)


# Function for version comparison
def version_comparison(latest_version, current_version):
    update = ""

    if latest_version != current_version:
        update = "A new version of Upload_Bypass is available to download 🎉"

    elif latest_version == current_version:
        update = current_version + " (Latest)"

    return update


# Function to get terminal size
def get_terminal_size():
    try:
        columns, _ = os.get_terminal_size(0)  # 0 means the standard output (stdout)
    except OSError:
        columns = 80  # Default value if unable to get terminal size
    return columns


# Function to print progress bar
def print_progress_bar(iteration, total):
    terminal_width = get_terminal_size()
    length = terminal_width - 20  # Adjust as needed for padding and other elements

    percent = int((iteration / total) * 100)
    filled_length = int(length * iteration // total)
    bar = '{}={}'.format(turquoise, reset) * filled_length + ' ' * (length - filled_length)
    print("")
    print("\rProgress: [{}]  {}% ".format(bar, percent), end='', flush=True)
    print("")


# Function to print status code with color coding
def print_status_code(status_code):
    if str(status_code).startswith("2"):
        status_code = f"{green}{status_code}{reset}"
    elif str(status_code).startswith("3"):
        status_code = f"{yellow}{status_code}{reset}"
    elif str(status_code).startswith("4"):
        status_code = f"{red}{status_code}{reset}"
    else:
        status_code = f"{red}{status_code}{reset}"

    return status_code


def print_response(response, options):
    terminal_width = get_terminal_size()

    if options.response:
        print("")
        print(f"📡 {cyan}HTTP Response: {reset}")
        print("-" * terminal_width)
        print(response.text)  # Print the response text to the console
        print("-" * terminal_width)


def display_options(attributes):
    concat_options = ""
    for display in attributes:
        concat_options += display + " | "
    concat_options = concat_options[:-2]
    return concat_options


# Function to print response details
def print_response_options(response, file_name, current_time, module, magic_bytes, mimetype):
    response_attributes = ["Module", "Mimetype", "Magic-Byte?", "Filename", "Status-Code", "Current-Time",
                           "Response-Time"]
    response_attributes = display_options(response_attributes)
    term_size = os.get_terminal_size()

    print("")
    print(response_attributes)
    print('─' * term_size.columns)
    response_time = response.elapsed.total_seconds()
    status_code = response.status_code
    status_code = print_status_code(status_code)
    if isinstance(file_name, bytes):
        file_name = file_name.decode('latin-1')

    print(
        f"{module}     {mimetype}     {magic_bytes}     {file_name}     {status_code}     {current_time}     {response_time}")
    print('─' * term_size.columns)


# Function to print straight line
def print_straight_line(length, character='-'):
    print(character * length)


# Function to print various details
def printing(options, user_options, response, file_name, overall_progress, current_time, module, magic_bytes, mimetype):
    print("\033c", end="")
    print("")
    print("\033[1mUser Options:\033[0m")
    print(user_options)

    print_response_options(response, file_name, current_time, module, magic_bytes, mimetype)

    print_progress_bar(overall_progress, 100)

    print_response(response, options)


# Function for file upload
def file_upload(request_file, file_name, original_extension, options, magic_bytes, allowed_extension, mimetype, module,
                overall_progress, file_data=None, skip_module=None, current_extension_tested=None, filename_without_nullbyte=None):
    # Declaring these variables for ease an ease access later
    options.current_mimetype = mimetype
    options.current_module = module
    options.current_extension_tested = current_extension_tested

    # Parse request file
    response, headers, url, content_type = file_parser.parse_request_file(request_file, options, file_name,
                                                                          original_extension, mimetype,
                                                                          magic_bytes, file_data, module)
    user_options = ""

    rate_limit_seconds = options.rateLimit / 1000
    time.sleep(rate_limit_seconds)

    # Remove trailing forward slash from the URL
    if url.endswith('/'):
        url = url[:-1]

    user_options += f"🌐 Target URL: {url}\n"
    user_options += f"🔗 Backend Extension: {options.file_extension}\n"
    user_options += f"🔗 Allowed Extension: {allowed_extension}\n"

    # Determine mode based on options
    if options.exploitation:
        mode = "Exploit"
    elif options.detect:
        mode = "Detect"
    else:
        mode = "Anti-Malware"

    user_options += f"🎮 Mode: {mode}\n"

    if options.upload_dir != 'optional':
        parsed_url = urlparse(url)
        base_url = parsed_url.scheme + "://" + parsed_url.netloc

        # Removing trailing extension
        if module in config.original_filenames:
            split_file_name = file_name.split(".", 1)
            tmp_file_name = split_file_name[0]
            new_file_name = tmp_file_name + "." + options.current_extension_tested

            location_url = base_url + options.upload_dir + new_file_name
        else:
            location_url = base_url + options.upload_dir + file_name

    else:
        location_url = "Not specified"

    if options.upload_dir != 'optional':
        user_options += f"📍 Upload Location: {options.upload_dir}\n"

    if not str(options.text_or_code).isdigit():
        user_options += f"💬 Upload Message: {options.upload_message}\n"
    else:
        user_options += f"🚦 Status Code: {options.status_code}\n"

    if not options.output_dir:
        user_options += f"📁 Output File: {os.getcwd()}/{options.host}/results.txt\n"
    else:
        user_options += f"📁 Output File: {options.output_dir}\n"

    if options.include_modules:
        user_options += f"➕ Include Only Modules: {options.include_modules}\n"
    elif options.exclude_modules:
        user_options += f"➖ Exclude Modules: {options.exclude_modules}\n"

    if options.rateLimit != 0:
        rate_limit = options.rateLimit
        user_options += f"⏳ Rate Limiting: {rate_limit}\n"

    if options.proxy != 'optional':
        proxy = options.proxy
        user_options += f"🕵️ Proxy: {proxy}\n"
    elif options.burp_http or options.burp_https:
        proxy = "http(s)://127.0.0.1:8080"
        user_options += f"🕵️ Proxy: {proxy}\n"

    if options.debug:
        user_options += f"🐞 Debug Mode: {options.debug}\n"

    user_options += f"🕒 Request Timeout: {options.request_timeout}\n"

    if options.base64:
        user_options += f"🔢 Base64 Encode: {options.base64}\n"

    if options.brute_force:
        user_options += f"💪 Brute Force: {options.brute_force}\n"

    if options.allow_redirects:
        user_options += f"🚀 Allow Redirects {options.verify_tls}\n"

    if options.response:
        user_options += f"📨 Print Response {options.upload_message}\n"

    user_options += f"🚨 Verify SSL: {options.verify_tls}\n"

    now = datetime.datetime.now()
    current_time = now.strftime("%d.%m.%Y_%H:%M:%S")

    # Read the current configuration
    with open("config/version.json", "r") as file:
        version = json.load(file)

    update = version_comparison(version["latest_version"], version["current_version"])

    user_options += f"🔄 Version: {update}"

    # Print various details
    printing(options, user_options, response, file_name, overall_progress, current_time, module, magic_bytes, mimetype)

    if filename_without_nullbyte:
        filename_nullbyte = file_name
        
    if options.anti_malware:

        # Send response to Eicar function and checks if brute_force is active or not
        response_status = eicar_checker.eicar(response, file_name, url, content_type, options, allowed_extension,
                                              current_time, user_options, skip_module, headers)
    else:
        # Send response to Success function and checks if brute_force is active or not
        response_status, exploit_machine = interactive_shell.response_check(options, headers, file_name, content_type,
                                                                            location_url, magic_bytes,
                                                                            allowed_extension, current_time, response,
                                                                            user_options, skip_module, module, filename_without_nullbyte)
        if exploit_machine:

            options.exploitation = True
            options.detect = False

            if filename_without_nullbyte:
                split_file_name = filename_nullbyte.split(".")
                new_name = random_string.generate_random_string(10)
                del split_file_name[0]
                filename_without_nullbyte = new_name + "." + original_extension
                extension_nullbyte = ".".join(split_file_name)
                file_name = new_name + "." + extension_nullbyte
                

            else:
                split_filename = file_name.split(".", 1)
                split_extensions = split_filename[1]
                new_name = random_string.generate_random_string(10)
                file_name = new_name + "." + split_extensions

            response, headers, url, content_type = file_parser.parse_request_file(request_file, options, file_name,
                                                                    original_extension, mimetype,
                                                                    magic_bytes, file_data, module)

            _, _ = interactive_shell.response_check(options, headers, file_name, content_type, location_url,
                                                    magic_bytes, allowed_extension, current_time, response,
                                                    user_options, skip_module, module, filename_without_nullbyte)

            return


    return headers, response_status, response, url, content_type, current_time, user_options
