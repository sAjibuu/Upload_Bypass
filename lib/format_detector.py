#!/usr/bin/env python3

import re
import xml.etree.ElementTree as ET
import base64
import time
from . import config
from .ansi_colors import *
from .alerts import error, success
from .random_string import generate_random_string
from lib.debug import save_stack_trace
from lib.file_upload import print_response
import traceback
from requests.exceptions import SSLError
import requests
import sys
import json
from lib.alerts import info


# Determine if an extension is permitted on the system and return it
def response_message(options, status_code, allowed_extension, extension, response):
    if options.upload_message == 'not_selected':
        if status_code == options.status_code:
            allowed_extension.append(extension)

    else:
        message = options.text_or_code
        if message == 'success_message':
            if options.upload_message in response.text:
                allowed_extension.append(extension)

        elif message == 'failure_message':

            if options.upload_message not in response.text:
                allowed_extension.append(extension)

    return allowed_extension


def make_request(data, session, headers, options, url, data_type):
    response = None

    try:

        if options.put_method:
            try:
                if data_type == "raw":  # Check if data is anything but json
                    response = session.put(url, data=data, headers=headers, proxies=options.proxies,
                                           allow_redirects=options.allow_redirects,
                                           verify=options.verify_tls, timeout=options.request_timeout)
                else:  # Send a JSON request
                    response = session.put(url, json=data, headers=headers, proxies=options.proxies,
                                           allow_redirects=options.allow_redirects,
                                           verify=options.verify_tls, timeout=options.request_timeout)
            # Fall back to HTTP
            except SSLError:
                url_http = url.replace('https://', 'http://')  # Change protocol to http
                if data_type == "raw":  # Check if data is anything but json
                    response = session.put(url_http, data=data, headers=headers, proxies=options.proxies,
                                           allow_redirects=options.allow_redirects, verify=False, timeout=options.request_timeout)
                else:  # Send a JSON request
                    response = session.put(url_http, json=data, headers=headers, proxies=options.proxies,
                                           allow_redirects=options.allow_redirects,
                                           verify=options.verify_tls, timeout=options.request_timeout)
            except requests.exceptions.ProxyError:
                error(
                    f"You are having issue with your proxy, check if your proxy program is well configured. If you are trying "
                    f"to access an HTTP website, configure Upload Bypass to use the HTTP protocol inside the config.py.")

        elif options.patch_method:
            try:
                if data_type == "raw":  # Check if data is anything but json
                    response = session.patch(url, data=data, headers=headers, proxies=options.proxies,
                                            allow_redirects=options.allow_redirects,
                                            verify=options.verify_tls, timeout=options.request_timeout)
                else:  # Send a JSON request
                    response = session.patch(url, json=data, headers=headers, proxies=options.proxies,
                                            allow_redirects=options.allow_redirects,
                                            verify=options.verify_tls, timeout=options.request_timeout)
                    # Fall back to HTTP
            except SSLError:
                url_http = url.replace('https://', 'http://')  # Change protocol to http
                if data_type == "raw":  # Check if data is anything but json
                    response = session.patch(url_http, data=data, headers=headers, proxies=options.proxies,
                                            allow_redirects=options.allow_redirects, verify=False, timeout=options.request_timeout)
                else:  # Send a JSON request
                    response = session.patch(url_http, json=data, headers=headers, proxies=options.proxies,
                                            allow_redirects=options.allow_redirects,
                                            verify=options.verify_tls, timeout=options.request_timeout)

            except requests.exceptions.ProxyError:
                error(
                    f"You are having issue with your proxy, check if your proxy program is well configured. If you are trying "
                    f"to access an HTTP website, configure Upload Bypass to use the HTTP protocol inside the config.py.")
                                   
        else:
            try:
                if data_type == "raw":  # Check if data is anything but json
                    response = session.post(url, data=data, headers=headers, proxies=options.proxies,
                                            allow_redirects=options.allow_redirects,
                                            verify=options.verify_tls, timeout=options.request_timeout)
                else:  # Send a JSON request
                    response = session.post(url, json=data, headers=headers, proxies=options.proxies,
                                            allow_redirects=options.allow_redirects,
                                            verify=options.verify_tls, timeout=options.request_timeout)
                    # Fall back to HTTP
            except SSLError:
                url_http = url.replace('https://', 'http://')  # Change protocol to http
                if data_type == "raw":  # Check if data is anything but json
                    response = session.post(url_http, data=data, headers=headers, proxies=options.proxies,
                                            allow_redirects=options.allow_redirects, verify=False, timeout=options.request_timeout)
                else:  # Send a JSON request
                    response = session.post(url_http, json=data, headers=headers, proxies=options.proxies,
                                            allow_redirects=options.allow_redirects,
                                            verify=options.verify_tls, timeout=options.request_timeout)

            except requests.exceptions.ProxyError:
                error(
                    f"You are having issue with your proxy, check if your proxy program is well configured. If you are trying "
                    f"to access an HTTP website, configure Upload Bypass to use the HTTP protocol inside the config.py.")

    except Exception as e:

        if options.debug:

            # Check if debug mode is activated
            debug_mode = options.debug
            # Print the stack trace to the screen
            traceback.print_exc()

            # Save the stack trace to the 'debug' directory
            save_stack_trace(debug_mode, sys.argv, options.request_file)
        else:
            error(f'{e}\n{red}[-]{reset} For a full stack trace error use the --debug flag')

    if options.response:
        print_response(response, options)

    return response.status_code, response


# Parse headers from the request file
def parse_headers(options, request, extension):
    try:
        # Set file name with a random string
        file_name = generate_random_string(10) + f".{extension}"

        # Split the request into headers and body
        headers_end_index = request.find('\n\n')

        # If no double newline is found, try finding '\n\r\n'
        if headers_end_index == -1:
            headers_end_index = request.find('\n\r\n')

        # Extract the header content
        headers_content = request[:headers_end_index]

        # Extract headers using regular expression
        headers_list = re.findall(r'^(?P<name>[^:\r\n]+):\s*(?P<value>[^\r\n]*)', headers_content, flags=re.MULTILINE)

        # Convert the list of tuples to a list of dictionaries for easier manipulation
        headers_list = [{'key': key.strip(), 'value': value.strip()} for key, value in headers_list]

        # Convert the list of dictionaries to a dictionary
        headers = {item['key']: item['value'] for item in headers_list}

        # Split the request string by lines
        lines = request.split('\n')

        # Extract the host value from the 'Host' header
        host = [line.split(': ')[1] for line in lines if line.startswith('Host')][0].split()[0]

        # Extract the path from the first line of the request
        path = lines[0].split(' ')[1]
        # Extract protocol from a predefined configuration
        protocol = config.protocol

        # Construct the URL from the extracted components
        url = f'{protocol}://{host}{path}'

        keys_to_delete = []
        for key, value in headers.items():
            # Delete the accept header
            if "Accept" in key:
                keys_to_delete.append(key)

        # Deleting unnecessary headers
        for key in keys_to_delete:
            del headers[key]

        return headers, url, file_name, host

    except IndexError:
        error("A malformed request file was supplied, please check your request file.")

    except Exception as e:

        if options.debug:

            # Check if debug mode is activated
            debug_mode = options.debug
            # Print the stack trace to the screen
            traceback.print_exc()

            # Save the stack trace to the 'debug' directory
            save_stack_trace(debug_mode, sys.argv, options.request_file)
        else:
            error(f'{e}\n{red}[-]{reset} For a full stack trace error use the --debug flag')


def parse_request_file(request_file, session, options):
    try:
        request = ""  # Initialize an empty string to store the decoded request

        # Declare an XML object and parsing the XML file
        tree = ET.parse(request_file)
        root = tree.getroot()

        for i in root:
            # Search for the 'request' element in the XML and extracting its text content
            request = i.find('request').text

            # Decode the base64 encoded content
            content = base64.b64decode(request)

            # Decode the content from latin-1 encoding
            request = content.decode('latin-1')

    except:
        # Open the request file as text
        with open(request_file, "r") as f:
            request = f.read()

    try:
        # Load all allowed extensions from the config file
        extensions = config.extensions['allow_list']
        allowed_extension = []

        # Iterate each extension loaded from the config file
        for extension in extensions:

            info(f"Checking if {extension} is permitted...")

            headers, url, file_name, host = parse_headers(options, request, extension)

            # Add variables to an argparse namespace, so it can be accessible in modules easily
            options.host = host
            options.url = url

            # Replace with the actual local file path
            with open(f"assets/samples/sample.{extension}", 'rb') as file:
                file_data = file.read()

            file_data = file_data.decode('latin-1')
            mimetype = config.mimetypes[extension]
            xml_mimetypes = config.xml_mimetypes
            request = request.replace("\r\n", "\n").replace("\n", "\r\n")
            # Replace marker with a filename
            content = request.replace(config.filename_marker, file_name)

            xml = False
            # Auto-detect xml and base64 the data binary
            for xml_mime in xml_mimetypes:
                if xml_mime in str(headers):
                    xml = True
                    break

            # Auto-detect JSON and base64 the data binary
            if "application/json" in str(headers):
                if isinstance(file_data, bytes):
                    file_data = base64.b64encode(file_data)
                else:
                    file_data = base64.b64encode(file_data.encode('latin-1'))

            elif options.base64:
                if isinstance(file_data, bytes):
                    file_data = base64.b64encode(file_data)
                else:
                    file_data = base64.b64encode(file_data.encode('latin-1'))

            else:
                if not xml:
                    if isinstance(file_data, bytes):
                        file_data = file_data.decode('latin-1')
                        # Replace marker with binary data
                        content = content.replace(config.data_marker, file_data)
                    else:
                        content = content.replace(config.data_marker, file_data)
                else:
                    if isinstance(file_data, bytes):
                        file_data = base64.b64encode(file_data)
                    else:
                        file_data = base64.b64encode(file_data.encode('latin-1'))

            if isinstance(file_data, bytes):
                content = content.replace(config.data_marker, file_data.decode('latin-1'))
            else:
                content = content.replace(config.data_marker, file_data)

            # Handle various newlines and carriage returns
            try:
                content = content.split('\r\n\r\n', 1)
                body = content[1]
            except IndexError:
                try:
                    content = content.split('\n\n', 1)
                    body = content[1]
                except AttributeError:
                    content = content[0]
                    content = content.split('\n\n', 1)
                    body = content[1]

            # Replace the mimetype marker with the file's mimetype
            data = body.replace(config.mimetype_marker, mimetype)

            try:
                data = data.encode("latin-1")
            except UnicodeDecodeError:
                data = data.encode("utf-8")

            if "application/json" not in str(headers):
                data_type = "raw"

            else:
                data_type = "json"
                data = json.loads(data)

            # Send the request
            status_code, response = make_request(data, session, headers, options, url, data_type)

            allowed_extension = response_message(options, status_code, allowed_extension, extension, response)

            # Check if allowed extensions is not empty
            if len(allowed_extension) > 0:
                success(f"{allowed_extension[0]} found to be permitted, adding it for future requests.")
                time.sleep(2)
                break

        return allowed_extension

    except Exception as e:

        if options.debug:

            # Check if debug mode is activated
            debug_mode = options.debug
            # Print the stack trace to the screen
            traceback.print_exc()

            # Save the stack trace to the 'debug' directory
            save_stack_trace(debug_mode, sys.argv, options.request_file)
        else:
            error(f'{e}\n{red}[-]{reset} For a full stack trace error use the --debug flag')
