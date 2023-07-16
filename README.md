# Upload_Bypass v2.0.0

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

**Upload_Bypass** is a powerful tool designed to assist Pentesters and Bug Hunters in testing file upload mechanisms. It leverages various bug bounty techniques to simplify the process of identifying and exploiting vulnerabilities, ensuring thorough assessments of web applications.

- Simplifies the identification and exploitation of vulnerabilities in file upload mechanisms.
- Leverages bug bounty techniques to maximize testing effectiveness.
- Enables thorough assessments of web applications.
- Provides an intuitive and user-friendly interface.
- Enhances security assessments and helps protect critical systems.
#### New PoC Video:
<a href="https://www.youtube.com/watch?v=MqVAABLNAa8&ab_channel=SagivMichael" target="_blank" rel="noopener noreferrer">Click me to be redirected to the video</a>

#### Developed by Sagiv
![Untitled video - Made with Clipchamp (3)](https://github.com/sAjibuu/Upload_Bypass/assets/81802295/6d5c5f2e-2cb0-42cd-bfcf-d8eceeff5054)
## Disclaimer

**Please note that the use of Upload_Bypass and any actions taken with it are solely at your own risk. The tool is provided for educational and testing purposes only. The developer of Upload_Bypass is not responsible for any misuse, damage, or illegal activities caused by its usage.**

While Upload_Bypass aims to assist Pentesters and Bug Hunters in testing file upload mechanisms, it is essential to obtain proper authorization and adhere to applicable laws and regulations before performing any security assessments. Always ensure that you have the necessary permissions from the relevant stakeholders before conducting any testing activities.

The results and findings obtained from using Upload_Bypass should be communicated responsibly and in accordance with established disclosure processes. It is crucial to respect the privacy and integrity of the tested systems and refrain from causing harm or disruption.

By using Upload_Bypass, you acknowledge that the developer cannot be held liable for any consequences resulting from its use. Use the tool responsibly and ethically to promote the security and integrity of web applications.


# Features 
1. Webshell mode:
       The tool will try to upload a Webshell with a random name, and if the user specifies the location of the uploaded file, the tool enters an "Interactive shell".
2. Eicar mode:
       The tool will try to upload an Eicar(Anti-Malware test file) instead of a Webshell, and if the user specifies the location of the uploaded file, the tool will check if the file 
       uploaded successfully and exists in the system in order to determine if an Anti-Malware is present on the system. 
3. A directory with the name of the tested host will be created in the Tool's directory upon success, with the results saved in Excel and Text files.

# Download:
  Download the latest version from Releases page.

# Installation:

    pip install -r requirements.txt

# Limitations: 
  The tool will not function properly if the file upload mechanism includes CAPTCHA implementation.
  
  Perhaps in the future the tool will include an OCR.

# Usage:

## ***Attension***

The Tool is compatible exclusively with output file requests generated by Burp Suite.

Before saving the Burp file, replace the file content with the string \*content\* and filename.ext with the string \*filename\* and Content-Type header with \*mimetype\*(only if the tool is not able to recognize it automatically).

How a request should look before the changes:

![2023-06-26_15h42_14](https://github.com/sAjibuu/Upload_Bypass/assets/81802295/acfbe9bc-16d3-4960-884a-e6706317dbbd)

How it should look after the changes:

![2023-06-26_15h42_52](https://github.com/sAjibuu/Upload_Bypass/assets/81802295/a1dc86df-5914-4f88-a2f9-b514647621f7)

If the tool fails to recognize the mime type automatically, you can add \*mimetype\* in the parameter's value of the Content-Type header.

Options:
  -h, --help            
  
     show this help message and exit

  -b BURP_FILE, --burp-file BURP_FILE
  
     Required - Read from a Burp Suite file
     Usage: -b / --burp-file ~/Desktop/output
        
  -s SUCCESS_MESSAGE, --success SUCCESS_MESSAGE
  
     Required if -f is not set - Provide the success message when a file is uploaded
     Usage: -s /--success 'File uploaded successfully.'
        
  -f FAILURE_MESSAGE, --failure FAILURE_MESSAGE
  
     Required if -s is not set - Provide a failure message when a file is uploaded
     Usage: -f /--failure 'File is not allowed!'     
        
  -e FILE_EXTENSION, --extension FILE_EXTENSION
  
     Required - Provide server backend extension
     Usage: -e / --extension php (Supported extensions: php,asp,jsp,perl,coldfusion)
      
  -a ALLOWED_EXTENSIONS, --allowed ALLOWED_EXTENSIONS 
  
     Required - Provide allowed extensions to be uploaded
     Usage: -a /--allowed jpeg, png, zip, etc'
        
   -l WEBSHELL_LOCATION, --location WEBSHELL_LOCATION 
  
      Provide a remote path where the WebShell will be uploaded (won't work if the file will be uploaded with a UUID).
      Usage: -l / --location /uploads/  
        
   -rl NUMBER, --rate-limit NUMBER
  
      Set rate-limiting with milliseconds between each request.
      Usage: -r / --rate-limit 700  
        
   -p PROXY_NUM, --proxy PROXY_NUM
  
      Channel the HTTP requests via proxy client (i.e Burp Suite).
      Usage: -p / --proxy http://127.0.0.1:8080
      
   -S, --ssl 
  
      If set, the tool will not validate TLS/SSL certificate.
      Usage: -S / --ssl
      
   -c, --continue  
  
      If set, the brute force will continue even if one of the methods gets a hit!
      Usage: -C /--continue  
      
   -E, --eicar  
  
      If set, an Eicar file(Anti Malware Testfile) will be uploaded only. WebShells will not be uploaded (Suitable for real environments).
      Usage: -E / --eicar
      
   -v, --verbose 
  
      If set, details about the test will be printed on the screen
      Usage: -v / --verbose   
      
  -r, --response
  
      If set, HTTP response will be printed on the screen
      Usage: -r / --response

  --version  
  
      Print the current version of the tool.     
      
  --update
  
      Checks for new updates. If there is a new update, it will be downloaded and updated automatically.     
      
# Examples
  ### Running the tool with Eicar and Bruteforce mode along with a verbose output     
     python upload_bypass.py -b ~/Desktop/burp_output -s 'file upload successfully!' -e php -a jpeg --response -v --eicar --continue
  ### Running the tool with Webshell mode along with a verbose output     
     python upload_bypass.py -b ~/Desktop/burp_output -s 'file upload successfully!' -e asp -a zip -v
  ### Running the tool with a Proxy client   
     python upload_bypass.py -b ~/Desktop/burp_output -s 'file upload successfully!' -e jsp -a png -v --proxy http://127.0.0.1:8080
