# upload_bypass_carnage

POC video:

   https://www.youtube.com/watch?v=quFoDysbDto&ab_channel=SagivMichael

File upload restrictions bypass by using different bug bounty techniques!
Tool must be running with all its assets!

 Installation:

    pip3 install -r requirements.txt

Usage: upload_bypass.py [options]

Options:
  -h, --help            
  
      show this help message and exit
  
  -u URL, --url=URL    
  
      Supply the login page, for example: -u http://192.168.98.200/login.php'
  
  -s , --success
  
     Success message when upload an image, example: -s 'Image uploaded successfully.'
      
  -e , --extension 
  
     Provide server backend extension, for example: --extension php (Supported extensions: php,asp,jsp,perl,coldfusion)
      
   -a , --allowed
   
     Provide allowed extensions to be uploaded, for example: php,asp,jsp,perl
  
  -H , --header 
       
     (Optional) - for example: '"X-Forwarded-For":"10.10.10.10"' - Use double quotes around the data and wrapp it all with single quotes. Use comma to separate multi headers.

  -l , --location
        
     (Optional) - Supply a remote path where the webshell suppose to be. For exmaple: /uploads/
  
  -S, --ssl
       
     (Optional) - No checks for TLS or SSL
  
  -p, --proxy
     
     (Optional) - Channel the requests through proxy
  
  -c, --continue
      
     (Optional) - If set, the brute force will continue even if one or more methods found!
  
  -v, --verbose
    
     (Optional) - Printing the http response in terminal
    
  -U , --username
  
     (Optional) - Username for authentication. For exmaple: --username admin
  
  -P , --password 
  
     (Optional) - - Password for authentication. For exmaple: --username 12345
