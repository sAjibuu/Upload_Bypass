#!/usr/bin/env python3

# Importing necessary libraries and modules
import json
import warnings
import signal
import sys
import importlib
import requests
from .config import active_modules
from .alerts import error, warning
import datetime
import argparse
import ast
import time
import os

# Ignore warnings
warnings.filterwarnings("ignore")


# Signal handler for CTRL + C
def handler(signal, frame, data_to_save, host):
    """Signal handler for CTRL + C."""
    now = datetime.datetime.now()
    current_time = now.strftime("%d.%m.%Y_%H:%M:%S")

    if not os.path.exists(f'{os.getcwd()}/{host}'):
        os.system(f'mkdir {os.getcwd()}/{host}')

    # Save state to a JSON file
    with open(f"{host}/{current_time}_{host}_state.json", "w") as f:
        json.dump(data_to_save, f)

    # Print a message
    print(f"\n🚨 Caught Ctrl + C 🚨 saving state to {host}/{current_time}_{host}_state.json")

    sys.exit(0)


# Function to save state to a JSON file before exiting
def save_state(options, technique, allowed_extension, function_number, internal_progress, internal_total_iterations,
               total_functions, state_extensions):
    # Delete proxies from argparse object
    proxies = options.proxies
    del options.__dict__["proxies"]
    del options.__dict__["session"]

    # Create data to save
    data_to_save = {
        "extensions": state_extensions,
        "technique": technique,
        "total_functions": total_functions,
        "function_number": function_number,
        "internal_progress": internal_progress,
        "internal_total_iterations": internal_total_iterations,
        "allowedExtension": allowed_extension,
        "request_file": options.request_file,
        "proxies": proxies,
        "options": str(options)
    }

    host = options.host

    # Call the signal handler
    handler(signal.SIGINT, None, data_to_save, host)


# Function to convert argparse.Namespace object to dictionary
def convert_namespace(namespace_string):
    # Split argparse.NameSpace object to dictionary
    namespace_dict = {}
    for item in namespace_string.strip("Namespace()").split(","):
        key, value = item.strip().split("=")
        try:
            value = ast.literal_eval(value)  # Attempt to evaluate simple values
        except (ValueError, SyntaxError):
            pass  # Leave as string if evaluation fails
        namespace_dict[key] = value

    return namespace_dict


# Function to resume state from a JSON file
def resume_state(resume_file):
    try:
        # Load JSON data from the resume file
        with open(resume_file, "r") as file:
            loaded_json_data = json.load(file)
            technique = loaded_json_data['technique']
            leftover_extensions = loaded_json_data['extensions']
            proxies = loaded_json_data['proxies']
            options = loaded_json_data['options']
            options = convert_namespace(options)
            total_functions = loaded_json_data['total_functions']
            function_number = loaded_json_data["function_number"]
            internal_progress = loaded_json_data['internal_progress']
            internal_total_iterations = loaded_json_data["internal_total_iterations"]

            # Reconstruct the object back
            options = argparse.Namespace(**options)
            options.proxies = proxies
            options.session = requests.Session()
            allowed_extension = loaded_json_data['allowedExtension']
            request_file = loaded_json_data['request_file']

        modules = importlib.import_module("lib.modules")
        index = active_modules.index(technique)
        # Remove extensions that has been checked
        if index == 0:
            leftover_modules = active_modules[index:]
        else:
            leftover_modules = active_modules[index - 1:]

        # Resume state
        warning("Resuming state...")
        time.sleep(3)
        modules_to_test = []

        if options.exclude_modules or options.exclude_modules:
            if options.exclude_modules:
                if "," in options.exclude_modules:
                    exclude_modules = options.exclude_modules.replace(" ", "").split(",")
                else:
                    exclude_modules = options.exclude_modules
                    exclude_modules = exclude_modules.split()
                for exclude_module in exclude_modules:
                    leftover_modules.remove(exclude_module)

            elif options.include_modules:
                if "," in options.include_modules:
                    include_modules = options.include_modules.replace(" ", "").split(",")
                else:
                    include_modules = options.exclude_modules
                    include_modules = include_modules.split()
                for include_module in include_modules:
                    modules_to_test.append(include_module)

                leftover_modules = modules_to_test[:]

            # Exclude irrelevant modules for a by the book eicar(Anti-Malware) check (According to eicar.org documentation)
            elif options.anti_malware:
                leftover_modules.remove("htaccess_overwrite")
                leftover_modules.remove("svg_xss")
                leftover_modules.remove("svg_xxe")

        for module in leftover_modules:
            getattr(modules, module)(request_file, options, allowed_extension, function_number, total_functions,
                                     internal_progress, internal_total_iterations, leftover_extensions)

    except FileNotFoundError as e:
        error(e)
