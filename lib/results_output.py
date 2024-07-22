#!/usr/bin/env python3

import os
from .alerts import *
from urllib.parse import urlparse
from .config import magic_bytes


def results(url, file_name, content_type, upload_location, magic_byte, output_folder, allowed_extension, current_time, module):
    domain = get_domain_name(url)
    domain = domain.split(":")[0] # Windows cannot create a directory with a filename containing the colon sign (:) which notes the port number (i.e 127.0.0.1:8008)

    if not output_folder:
        folder_path = os.path.join(os.getcwd(), domain)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True)

        # Save the results to results.txt
        file_path = os.path.join(folder_path, "results.txt")
        f = open(f"{file_path}", "a")
        success(f"Results saved in {os.getcwd()}/{domain}/results.txt")

    else:
        f = open(output_folder, "a")

    if not magic_byte:
        f.write("-------------------------------------------------------------------------------------------\n")
        f.write(
            f"File uploaded successfully with the extension: {file_name}\nContent-Type: {content_type}\nUpload Location: {upload_location}\nDate & Time: {current_time}\nModule: {module}\n\n")
        f.close()
    else:
        f.write("-------------------------------------------------------------------------------------------\n")
        f.write(
            f"File uploaded successfully with the extension: {file_name}\nContent-Type: {content_type}\nUpload Location: {upload_location}\nMagic Bytes: {magic_bytes[allowed_extension]}\nDate & Time: {current_time}Module: {module}\n\n")
        f.close()


def get_domain_name(url):
    parsed_url = urlparse(url)
    domain_name = parsed_url.netloc
    return domain_name
