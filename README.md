# Upload_Bypass v3

![GPL-3.0 License](https://img.shields.io/badge/License-GPL3.0-green.svg) ![287245591-b1f3cdd6-3d00-4bbb-94c1-38a9204add71](https://github.com/sAjibuu/Upload_Bypass/assets/81802295/d654bec4-134b-4396-8a02-2480984e5aa7)

# About

**Upload Bypass** is a simple tool designed to assist penetration testers and bug hunters in testing file upload mechanisms. It leverages various bug bounty techniques to simplify the process of identifying and exploiting vulnerabilities, ensuring thorough assessments of web applications.

#### Developed by Sagiv
![2024-02-18_20h04_06](https://github.com/sAjibuu/Upload_Bypass/assets/81802295/46251ded-e89d-4ce6-b2a5-c229850fdf06)

### 🚀 Updates
- The code almost written from scratch, utilizes better file parsing and eliminates most of the bugs.
- Modular code! Now you can contribute to the code and add your own modules.
- Introducing 3 different modes, detection, exploitation and anti_malware check, choose your weapon!
- New state feature, you can now pause the code and resume from where you left off!
- New UI for an easy view.
- Docker file for an easy deployment.
- Various test files provided for internal testing.
- Debug mode. If you encounter a bug, you can save the stack trace and share it with me for further analysis.

### Attention
This tool is restricted in the OSCP exam!

# Features 
### Detection Mode:
   Suitable for real-world penetration tests. This mode will upload harmless files and will not attempt to exploit the target.

*New* - If a destination folder for the uploaded files is provided, the program will determine if the uploaded sample file is rendered.
For example, if you chose PHP, the program will try to determine if an echo command is executed and rendered successfully, if it does, it'll suggest to enter an interactive shell.

### Exploitation Mode:
   Suitable when you want to exploit the target and upload an interactive Web-shell (If a destination upload directory is provided), it will upload the file with a random UUID, so it will be harder for fuzzers to guess.    
### Anti-Malware mode:
   Suitable for an Anti-Malware presence test. Upload an Eicar(Anti-Malware test file) to the system, and if the user specifies the location of the uploaded file, the program will check if the file uploaded successfully and exists in the system in order to determine if an Anti-Malware is present on the system. 

# Customisation

###
Check out config.py in lib directory, you can add new extensions, mimetypes, magicbytes, configure your HTTP method and etc'...
###
To add a new module, simply add a function with your desired functionality to modules.py then add the function by name into the list "active_modules" in config.py
###
To add a new file extension, add a sample.{ext} file to assets/sample_files, then add the extension and its mimetype/magic bytes to config.py

# Download:
    git clone https://github.com/sAjibuu/Upload_Bypass.git

# Installation:

    pip install -r requirements.txt

# Installation from a Docker Hub
    sudo docker pull sajibuu/upload_bypass 

# Installation from a local docker file
    sudo docker build -t upload_bypass .

# Docker Usage
    # The docker is installed with Nano and Vim, so you can save the request file easily.
    sudo docker run -it --entrypoint /bin/bash sajibuu/upload_bypass
    
# Limitations: 
  The tool will not function properly with the following:
  1. CAPTCHA implementation is in place.
  2. A requirement for a CSRF token for each request.
  3. A destination folder is provided for the uploaded files, but, the uploaded files are saved with a GUID (Globally Unique Identifier) instead of their actual filenames, the program won't be able to work with it.

## Disclaimer

**Please note that the use of Upload Bypass and any actions taken with it are solely at your own risk. The tool is provided for educational and testing purposes only. The developer of Upload Bypass is not responsible for any misuse, damage, or illegal activities caused by its usage.**

# Usage:

## ***Attention***

The program works only with requests files generated by proxy tools, such as Burp Suite and ZAP OWASP.

Before saving the request file from the proxy you are using, for example, Burp Suite, replace the the following parameter values with their coressponding markers:

**File content:** *\*data\**

Example: Replace the image binary data with the string *\*data\**

**Filename:** *\*filename\**

Example: Replace the filename including its extension with the string *\*filename\**

**Content-Type header:** *\*mimetype\**.

Example: Replace the file's content-type (mimetype) with the string *\*mimetype\**

### Example 1:

How it should look like in a JSON request:

![image](https://github.com/sAjibuu/Upload_Bypass/assets/81802295/2d230bc7-38e6-4a78-a3ba-95678e15a704)

### Example 2:

How it should look like in a multi-part data request:

![2024-02-27_11h20_23](https://github.com/sAjibuu/Upload_Bypass/assets/81802295/4cd3b240-5359-4435-a2ea-e182fe16e012)

# User Options:

```console

Usage: Upload Bypass [OPTIONS]

Options:
  -h, --help     Print help (see more with '--help')
  -v, --version  Print version

Required Arguments: 
  -r, --request_file <REQUEST_FILE>    Provide a request file to be proccessed
  -E, --extension    <EXTENSION>       Forbidden extension to check (ex: php)
  -A, --allowed      <EXTENSION>       Allowed extension (ex: jpeg) - Optional - if not set the program will auto-detect the extension

  Choose only one from the options below:
  -s, --success      <MESSAGE>         Provide a success message when a file is uploaded (ex: File was uploaded successfully)
  -f, --failure      <MESSAGE>         Provide a failure message when a file is uploaded (ex: File is not allowed!)
  -S, --status_code  <STATUS_CODE>     Provide a status code for a success upload (ex: 200)

Mode Settings: 
  -d, --detect          Upload harmless sample files (Suitable for a real penetration test)
  -e, --exploit         Upload Web-Shells files when testing
  -a, --anti_malware    Upload Anti-Malware Test file (Eicar) when testing
      I.  If set with -E flag the program will test with the Eicar string along with the choosen extension
      II. If set without the -E flag the program will test with Eicar string and a com extension

Modules Settings:     
  -l, --list            List all modules  
  -i, --include_only <MODULES>   Include only modules to test from (ex: extension_shuffle, double_extension)
  -x, --exclude      <MODULES>   Exclude modules (ex: svg_xxe, svg_xss)

Request Settings: 
  --base64              Encode the file data with Base64 algorithm
  --allow_redirects     Follow redirects
  -P, --put             Use the HTTP PUT method for the requests (Default is POST)
  -R, --response        Print the response to the screen
  -c, --continue        Continue testing all files, even if a few uploads encountered success
  -t, --time_out <NUM>  Set the request timeout (Default is 8)
  -rl, --rate_limit <NUMBER>  Set a rate-limit with a delay in milliseconds between each request

Proxy Settings: 
  -p, --proxy <PROXY>   Proxy to use for requests (ex: http(s)://host:port, socks5(h)://host:port)
  -k, --insecure        Do not verify SSL certificates
  --burp                Set --proxy to 127.0.0.1:8080 and set --insecure to false

Optional Settings: 
  -D, --upload_dir <UPLOAD_DIR>  Provide a remote path where the Web-Shell should be uploaded (ex: /uploads)
  -o, --output  <OUTPUT_PATH>    Output file to write the results into - Default current directory (ex: ~/Desktop/results.txt)
  --debug  <NUM>                 Debug mode - Print the stack trace error to the screen and save it to a file (ex: --debug 1)
      I.  Level 1 - Saves only the stack trace error (default).
      II. Level 2 - Saves the stack trace error and user's arguments along with the request file.
  
Resume settings:
  --resume  <STATE_FILE>  State file from which to resume a partially complete scan

Update settings:
  -u, --update  Update the program to the latest version
```

# Examples
  ### Detection mode
     python upload_bypass.py -r test -s 'File uploaded successfully' -E php -D /uploads --burp --detect
  ### Exploitation mode
     python upload_bypass.py -r test -s 'File uploaded successfully' -E php -D /uploads --burp --exploit
  ### Anti_Malware mode
     python upload_bypass.py -r test -s 'File uploaded successfully' -E php -D /uploads --burp --anti_malware   

# Issues
If you encounter an issue, please use the debug mode with a flag value of 2 and share it with me (the debug file is saved with the user supplied arguments, the provided request file, and the stack-trace error). If the file contains sensitive information, you can use flag value of 1, which only saves the stack-trace error to the file.

# Contribution
If you would like to contirute to my code, please specify exactly what you added to the code and why, and make sure you perform multiple tests before submitting the merge request.

# Credits
- Hacktricks - Special thanks for providing valuable techniques and insights used in this tool.  
- Artemixer - Thank you for inspiring me with your lighter version of my tool to rewrite the entire code and make it modular!
