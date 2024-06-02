#!/usr/bin/env python3

# Made by Sagiv

# Upload Bypass is a simple tool designed to assist penetration testers and bug hunters in testing file upload mechanisms.

# Copyright (C) 2024 Sagiv Michael

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# importing necessary modules
import argparse
import importlib
import traceback
import time
from lib import config
from lib.banner import banner, program_usage
from lib.update import *
from lib.state import resume_state
from lib import format_detector
from lib import alerts
from lib.debug import save_stack_trace
from lib.list_modules import list_all_modules


class Upload_Bypass:
    def __init__(self, user_options) -> None:

        # Initialize variables
        self.options = user_options
        self.resume_file = user_options.state
        self.debug = user_options.debug
        self.success_message = user_options.success_message
        self.failureMessage = user_options.failure_message
        self.status_code = user_options.status_code
        self.verify_tls = user_options.insecure
        self.proxy = user_options.proxy
        self.upload_dir = user_options.upload_dir
        self.request_file = user_options.request_file
        self.file_extension = user_options.file_extension
        self.upload_dir = user_options.upload_dir
        self.burp_http = user_options.burp_http
        self.burp_https = user_options.burp_https
        self.allowed_extension = options.allowed_extension
        self.session = requests.Session()
        self.upload_message = ""
        self.message = ""

    # User arguments
    @staticmethod
    def args():

        parser = argparse.ArgumentParser(add_help=False)

        # Check if the user explicitly requests help
        if "-h" in sys.argv or "--help" in sys.argv or len(sys.argv) == 1:
            banner()
            sys.exit()

        # User Options
        parser.add_argument("-r", "--request_file", default="not_set", dest="request_file")
        parser.add_argument("-s", "--success", type=str, required=False, dest="success_message", default="not_selected")
        parser.add_argument("-f", "--failure", type=str, required=False, dest="failure_message", default="not_selected")
        parser.add_argument("-d", "--detect", action="store_true", required=False, dest="detect")
        parser.add_argument("-e", "--exploit", action="store_true", required=False, dest="exploitation")
        parser.add_argument("-a", "--anti_malware", action="store_true", required=False, dest="anti_malware")
        parser.add_argument("-E", "--extension", type=str, default="not_set", dest="file_extension")
        parser.add_argument("-A", "--allowed", type=str, default="not_set", dest="allowed_extension")
        parser.add_argument("-D", "--upload_dir", type=str, dest="upload_dir", required=False, default="optional")
        parser.add_argument("-o", "--output", type=str, dest="output_dir", required=False, default=False)
        parser.add_argument("-rl", "--rate_limit", type=int, dest="rateLimit", required=False, default=0)
        parser.add_argument("-l", "--list", dest="list_modules", required=False, action="store_true")
        parser.add_argument("-i", "--include_only", type=str, dest="include_modules", required=False, default=False)
        parser.add_argument("-x", "--exclude", type=str, dest="exclude_modules", required=False, default=False)
        parser.add_argument("-p", "--proxy", type=str, dest="proxy", required=False, default="optional")
        parser.add_argument("-k", "--insecure", action="store_false", dest="insecure", required=False)
        parser.add_argument("-c", "--continue", action="store_true", required=False, dest="brute_force")
        parser.add_argument("-R", "--response", action="store_true", required=False, dest="response")
        parser.add_argument("-t", "--time_out", type=int, default=8, required=False, dest="request_timeout")
        parser.add_argument("-P", "--put", action="store_true", required=False, dest="put_method")
        parser.add_argument("-Pa", "--patch", action="store_true", required=False, dest="patch_method")
        parser.add_argument("--resume", default=False, required=False, dest="state")
        parser.add_argument("--debug", type=int, default=False, required=False, dest="debug")
        parser.add_argument("--base64", action="store_true", required=False, dest="base64")
        parser.add_argument("--burp_http", action="store_true", required=False, dest="burp_http")
        parser.add_argument("--burp_https", action="store_true", required=False, dest="burp_https")
        parser.add_argument("-S", "--status_code", type=int, required=False, dest="status_code", default=200)
        parser.add_argument("--allow_redirects", action="store_true", required=False, dest="allow_redirects")
        parser.add_argument("--version", action="store_true", dest="version")
        parser.add_argument("-U", "--usage", action="store_true", dest="usage")
        parser.add_argument("-u", "--update", action="store_true", dest="update")

        return parser.parse_args()

    def main(self):
        try:

            if not self.resume_file:

                if options.list_modules:
                    list_all_modules()

                if not options.exploitation and not options.detect and not options.anti_malware:
                    alerts.error("You must specify a mode.")

                if self.request_file == 'not_set':
                    alerts.error(f"-r, --request_file is a required argument!")

                if self.file_extension == 'not_set' and options.anti_malware:
                    options.file_extension = 'com'

                elif self.file_extension == 'not_set':
                    alerts.error(f"-E, --extension is a required argument, unless --anti_malware flag is active.")

                if sum([bool(options.anti_malware), bool(options.detect), bool(options.exploitation)]) > 1:
                    alerts.error(f"You must choose only one mode at a time (Detection, Exploitation, Anti-Malware)!")

                if "." in self.file_extension:
                    options.file_extension = self.file_extension.replace(".", "")
                    options.file_extension = self.file_extension.lower()

                if self.success_message == 'not_selected' and self.failureMessage == 'not_selected':
                    alerts.warning(
                        f"Success / Failure message isn't set, a successful upload will be based on {options.status_code} status code.")
                    options.upload_message = 'not_selected'
                    options.text_or_code = options.status_code
                    time.sleep(3)

                elif self.success_message != 'not_selected' and self.failureMessage == 'not_selected':
                    options.text_or_code = 'success_message'
                    options.upload_message = self.success_message

                elif self.success_message == 'not_selected' and self.failureMessage != 'not_selected':
                    options.text_or_code = 'failure_message'
                    options.upload_message = self.failureMessage

                if not self.verify_tls:
                    # Disable SSL verification 
                    options.verify_tls = False

                else:
                    # Enable SSL verification 
                    options.verify_tls = True

                if self.upload_dir != 'optional':
                    if not self.upload_dir.startswith("/"):
                        options.upload_dir = "/" + self.upload_dir

                    if not self.upload_dir.endswith("/"):
                        options.upload_dir = self.upload_dir + "/"

                # Check if proxy is provided and valid
                if self.proxy != 'optional':
                    if self.proxy.startswith("http://"):
                        self.proxy = self.proxy.replace("http://", "")
                    elif self.proxy.startswith("https://"):
                        self.proxy = self.proxy.replace("https://", "")

                    alerts.info(f"Proxy is running on {self.proxy}")

                    if self.proxy.startswith("socks"):
                        proxy_url = self.proxy.replace("socks://", "")
                        options.proxies = {
                            'http': f'socks5://{proxy_url}',
                            'https': f'socks5://{proxy_url}'
                        }
                    else:
                        options.proxies = {
                            'http': self.proxy,
                            'https': self.proxy
                        }

                else:
                    options.proxies = options.proxies = {
                        'http': None,
                        'https': None,
                    }

                if self.burp_http or self.burp_https:
                    alerts.info(f"Proxy is running on 127.0.0.1:8080")
                    options.proxies = {
                        'http': "127.0.0.1:8080",
                        'https': "127.0.0.1:8080",
                    }

                    if self.burp_http:
                        options.verify_tls = True
                    elif self.burp_https:
                        options.verify_tls = False

                # Check if arguments supplied by the user is less than 2
                if len(sys.argv) < 2:
                    print("Try '-h or --help' for more information.")
                    sys.exit(1)

                # Define session withing the argsparse namespace, for an ease use later
                options.session = self.session

                allowed_extension = self.allowed_extension
                if allowed_extension != 'not_set':
                    allowed_extension = self.allowed_extension
                    if allowed_extension.startswith("."):
                        allowed_extension = allowed_extension.replace(".", "")
                else:
                    # Determine which extension is permitted to be uploaded to the system
                    alerts.info("Detecting a permitted extension automatically...")
                    time.sleep(2)
                    allowed_extension = format_detector.parse_request_file(self.request_file, self.session,
                                                                           self.options)
                    allowed_extension = "".join(allowed_extension)
                    if allowed_extension == "":
                        alerts.error(
                            "Couldn't determine allowed extension to be uploaded, use the --insecure flag if you are targeting HTTPs requests or check if the allowed extension exists in config.py.")

                # Include or Exclude modules
                all_modules = config.active_modules
                modules_to_test = []

                if options.exclude_modules:
                    if "," in options.exclude_modules:
                        exclude_modules = options.exclude_modules.replace(" ", "").split(",")
                    else:
                        exclude_modules = options.exclude_modules
                        exclude_modules = exclude_modules.split()
                    for exclude_module in exclude_modules:
                        all_modules.remove(exclude_module)

                elif options.include_modules:
                    if "," in options.include_modules:
                        include_modules = options.include_modules.replace(" ", "").split(",")
                    else:
                        include_modules = options.include_modules
                        include_modules = include_modules.split()
                    for include_module in include_modules:
                        modules_to_test.append(include_module)

                    all_modules = modules_to_test[:]

                # Exclude irrelevant modules for a by the book eicar(Anti-Malware) check (According to eicar.org documentation)
                if options.anti_malware or options.detect:
                    for forbidden_module in config.dont_scan_module:
                        if forbidden_module in all_modules:
                            all_modules.remove(forbidden_module)

                current_progress = 0  # Setting number of modules to 0 for the progress bar

                # Import all modules (based on number of functions)
                final_modules = importlib.import_module("lib.modules")
                total_functions = len(all_modules)

                if len(all_modules) == 0:
                    alerts.error("The module/s you chose does not support detection/anti-malware mode.")
                for module in all_modules:
                    current_progress += 1
                    # Execute each module with its necessary arguments
                    getattr(final_modules, module)(self.request_file, self.options, allowed_extension, current_progress,
                                                   total_functions)

        except KeyboardInterrupt:
            alerts.error("Caught CTRL + C. Exiting...")

        except Exception as error:
            # Check if debug mode is activated
            if self.debug:
                # Print the stack trace to the screen
                traceback.print_exc()

                # Save the stack trace to the 'debug' directory
                save_stack_trace(self.debug, sys.argv, options.request_file)
            else:
                alerts.error(f'{error}\n{red}[-]{reset} For a full stack trace error use the --debug flag')


# Main function with all its arguments parsing
if __name__ == "__main__":

    try:
        options = Upload_Bypass.args()

        version = options.version
        update = options.update
        usage = options.usage
        session = requests.Session()

        if update:
            check_for_updates()
            sys.exit(0)

        if version:
            version = get_current_version()
            print("")
            print(version)
            sys.exit(0)

        if usage:
            print(program_usage())
            sys.exit(0)

        try:

            # Get the current and latest version of the program
            current_version, latest_version = get_current_and_latest_version()

            # Read the current configuration
            with open("config/version.json", "r") as file:
                version = json.load(file)

            # Modify the current version
            version["current_version"] = current_version
            version["latest_version"] = latest_version

            # Write the updated configuration back to the file
            with open("config/version.json", "w") as file:
                json.dump(version, file, indent=4)
        except requests.ConnectionError:
            alerts.info("The program couldn't establish a connection to the internet, check your internet connection.")

        resume_file = options.state

        if resume_file:
            resume_state(resume_file)

        # Create an instance of Upload_Bypass Class
        Upload_Bypass = Upload_Bypass(options)
        # Call main function
        Upload_Bypass.main()

    except Exception as e:

        if options.debug:

            # Check if debug mode is activated
            debug_mode = options.debug
            # Print the stack trace to the screen
            traceback.print_exc()

            # Save the stack trace to the 'debug' directory
            save_stack_trace(debug_mode, sys.argv, options.request_file)
        else:
            alerts.error(f'{e}\n{red}[-]{reset} For a full stack trace error use the --debug flag')

    except KeyboardInterrupt:
        alerts.error("Caught CTRL + C. Exiting...")
