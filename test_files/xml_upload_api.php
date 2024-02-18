<?php 

/*
Install first:
sudo apt-get install php-simplexml

Upload request for an example:
    
POST /xml_upload_api.php HTTP/1.1
Host: 127.0.0.1:8080
Content-Type: application/xml; charset=utf-8
Content-Length: [length]

<\?xml version="1.0" encoding="UTF-8"?>
<fileUpload>
    <filename>example.jpg</filename>
    <file_base64>base64_encoded_file_content_here</file_base64>
    <mime_type>image/jpeg</mime_type>
</fileUpload>
*/

error_reporting(E_ALL);
ini_set('display_errors', 1);
header('Content-Type: application/json; charset=utf-8');
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: PUT, GET, POST");

$response = array();
$upload_dir = 'uploads/';
$server_url = 'http://127.0.0.1:8000';

$inputXML = file_get_contents('php://input');

// Parse the XML to extract filename and file content
$xml = simplexml_load_string($inputXML);

if ($xml !== false) {
    $filename = (string) $xml->filename;
    $file_base64 = (string) $xml->file_base64;
    $mime_type = (string) $xml->mime_type;

    // Decode base64-encoded file content
    $file_data = base64_decode($file_base64);

    // Generate the upload path
    $upload_name = $upload_dir . $filename;

    // Save the file
    if (file_put_contents($upload_name, $file_data) !== false) {
        $response = array(
            "status" => "success",
            "error" => false,
            "message" => "File uploaded successfully",
            "url" => $server_url . "/" . $filename
        );
    } else {
        $response = array(
            "status" => "error",
            "error" => true,
            "message" => "Error uploading the file!"
        );
    }
} else {
    $response = array(
        "status" => "error",
        "error" => true,
        "message" => "Invalid XML input!"
    );
}

echo json_encode($response);
?>
