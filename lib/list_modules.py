#!/usr/bin/env python3

from .ansi_colors import *
from lib.file_upload import get_terminal_size


# Print all modules
def list_all_modules():
    
    print("\033c", end="")

    # \033[1m is for a bold text
    # \033[0m for a reset
    # \033[1m\033[4m is for a bold and underline text

    terminal_width = get_terminal_size()
    print("_" * terminal_width)
    print(f"\033[1m\nextension_shuffle\033[0m:\n\nDifferent extensions allowed by the back-end engine (ex: php3,php3,phar).")
    print("_" * terminal_width)
    print(f"\033[1m\ndouble_extension\033[0m:\n\nDoubling the back-end extensions (ex: filename.php.php).")
    print("_" * terminal_width)
    print(f"\033[1m\npolyglot\033[0m:\n\nUploading a JPEG file that contains a PHP code, it useful when a server might try to verify certain intrinsic properties of an image, such as its dimensions.")
    print("_" * terminal_width)
    print(f"\033[1m\ndiscrepancy\033[0m:\n\nURL encoding (or double URL encoding) for dots. If the value isn't decoded when validating the file extension, but is later decoded server-side, this can allow to upload malicious files that would otherwise be blocked. Ex: exploit%2Ephp (Front-end) = exploit.php (Back-end)")
    print("_" * terminal_width)
    print(f"\033[1m\nforward_double_extension\033[0m:\n\nAllowed extension concatenated with the back-end extension (ex: filename.jpeg.php).")
    print("_" * terminal_width)
    print(f"\033[1m\nreverse_double_extension\033[0m:\n\nBack-end extension concatenated with the allowed extension (ex: filename.php.jpeg).\n{red}\033[1mWarning\033[0m{reset} - It will probably generate false-positive results! (Suitable for CTFs) - You can turn off the module by commenting it in the config.py file located in the lib directory.")
    print("_" * terminal_width)
    print(f"\033[1m\nstripping_extension\033[0m:\n\nSevers might strip forbidden extensions, for example .php will be stripped from the filename. Therefore, the program will try to upload filename.p.phphp which results in filename.php")
    print("_" * terminal_width)
    print(f"\033[1m\nnull_byte_cutoff\033[0m:\n\nAdding null bytes which ultimately should cut the rest of the extension (ex: filename.php%00.jpeg the result will be filename.php).\n{red}\033[1mWarning\033[0m{reset} - It will generate false-positive results if the system ignores null bytes! - You can turn off the module by commenting it in the config.py file located in the lib directory.")
    print("_" * terminal_width)
    print(f"\033[1m\nname_overflow_cutoff\033[0m:\n\nOverflowing the exceeding limit to cut the allowed extension (ex: Linux limit is 255 chars, A*251.php.jpeg = A*251.php - total 255 chars).")
    print("_" * terminal_width)
    print(f"\033[1m\npath_traversal\033[0m:\n\nBypassing .htaccess rules that apply in the current directory by uploading a file in a parent directory using path traversal vulnerability.")
    print("_" * terminal_width)    
    print(f"\033[1m\nhtaccess_overwrite (works only with the exploitation mode)\033[0m:\n\nOver-writing the .htaccess rules to allow arbitrary file extension in the current directory and its sub-directories.")
    print("_" * terminal_width)
    print(f"\033[1m\nsvg_xxe (works only with the exploitation mode)\033[0m:\n\nUploading SVG with XML-External-Entity that reads the passwd file system.")
    print("_" * terminal_width) 
    print(f"\033[1m\nsvg_xss (works only with the exploitation mode)\033[0m:\n\nUploading SVG with Cross-Site Scripting that executes an alert popup.")
    print("_" * terminal_width)
    exit(1)
