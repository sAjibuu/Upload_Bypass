#!/usr/bin/env python3

from .ansi_colors import *
from datetime import datetime

# Defining warning messages
def warning(message):
    print("")
    print(f"{yellow}[!]{reset} {message}")

# Defining success messages
def success(message):
    print("")
    print(f"{green}[+]{reset} {message}")

# Defining info messages
def info(message):
    print("")
    print(f"{blue}[i]{reset} {message}")

# Defining error messages
def error(message):
    print("")
    print(f"{red}[-]{reset} {message}")
    exit(1)

# Defining try messages
def upload(message):
    current_time = datetime.now().strftime("%H:%M:%S")
    print(f"{turquoise}[{current_time}]{reset}  {message}")
