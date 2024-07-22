#!/usr/bin/env python3

import warnings
from .results_output import *
from requests.exceptions import SSLError
from . import file_upload

warnings.filterwarnings("ignore")


def print_eicar_message(eicar_reflected, options, user_options, response, file_name, current_time, is_magic_bytes,
                        skip_module, url, content_type, upload_location, allowed_extension):
    if not options.brute_force:
        # Reach 100% in the progress bar
        file_upload.printing(options, user_options, response, file_name, 100, current_time, options.current_module,
                             is_magic_bytes, options.current_mimetype)
        if eicar_reflected:
            warning("The uploaded Eicar (Anti-Malware test file) was found on the system!")
            warning("There is no sign of Anti-Malware on the system.")
        else:
            warning("Anti-Malware is enabled on the system, EICAR file not found!")

        success(f"Eicar file uploaded successfully with: {file_name}")

        if not skip_module:
            results(url, file_name, content_type, upload_location, is_magic_bytes, options.output_dir,
                    allowed_extension,
                    current_time, options.current_module)

            exit(1)

    else:

        results(url, file_name, content_type, upload_location, is_magic_bytes, options.output_dir, allowed_extension,
                current_time, options.current_module)

        if eicar_reflected:
            warning("The uploaded Eicar (Anti-Malware test file) was found on the system!")
            warning("There is no sign of Anti-Malware on the system.")

        else:
            warning("Anti-Malware is enabled on the system, EICAR file not found!")
            success(f"Eicar file uploaded successfully with: {file_name}")


def check_eicar(response, file_name, current_time, url, content_type, options, allowed_extension, user_options,
                skip_module, headers):
    is_magic_bytes = False

    upload_location = options.upload_dir

    if upload_location != 'optional':
        parsed_url = urlparse(url)
        base_url = parsed_url.scheme + "://" + parsed_url.netloc
        if options.upload_dir.endswith("=/"):
            upload_location = upload_location[:-1]
        final_url = base_url + upload_location + file_name

        try:
            # Send the command request to the target machine and get the response
            response, _ = file_upload.send_get_request(headers, options, final_url)

        except SSLError:
            final_url = final_url.replace('https://', 'http://')  # Change protocol to http
            # Send the command request to the target machine and get the response
            response, _ = file_upload.send_get_request(headers, options, final_url)

        eicar_file = r"X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"
        eicar_encoded = "WDVPIVAlQEFQWzRcUFpYNTQoUF4pN0NDKTd9JEVJQ0FSLVNUQU5EQVJELUFOVElWSVJVUy1URVNULUZJTEUhJEgrSCo="

        if eicar_file in response.text or eicar_encoded in response.text:

            print_eicar_message(True, options, user_options, response, file_name, current_time, is_magic_bytes,
                                skip_module, url, content_type, upload_location, allowed_extension)
        else:
            print_eicar_message(False, options, user_options, response, file_name, current_time, is_magic_bytes,
                                skip_module, url, content_type, upload_location, allowed_extension)

    else:
        upload_location = "Not specified by the user"
        print_eicar_message(False, options, user_options, response, file_name, current_time, is_magic_bytes,
                            skip_module, url, content_type, upload_location, allowed_extension)


def eicar(response, file_name, url, content_type, options, allowed_extension, current_time, user_options, skip_module,
          headers):
    # Initialize variable
    response_status = ""

    if str(options.text_or_code).isdigit():
        # Check if response is match the status code in message
        if options.text_or_code == response.status_code:  # If status code is equals to the status code of the response
            check_eicar(response, file_name, current_time, url, content_type, options, allowed_extension, user_options,
                        skip_module, headers)
            response_status = "success"
        else:
            response_status = "fail"

    elif options.text_or_code == 'success_message':

        if options.upload_message in response.text:  # If success text is present in the response body
            check_eicar(response, file_name, current_time, url, content_type, options, allowed_extension, user_options,
                        skip_module, headers)
            response_status = "success"
        else:
            response_status = "fail"

    elif options.text_or_code == 'failure_message':
        if options.upload_message not in response.text:  # If success text is present in the response body
            check_eicar(response, file_name, current_time, url, content_type, options, allowed_extension, user_options,
                        skip_module, headers)
            response_status = "success"
        else:
            response_status = "fail"

    return response_status
