<?php 

/*
Upload request example:

POST /json_upload_api.php HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/json; charset=utf-8
Content-Length: 124

{
    "file_base64": "base64_encoded_file_content_here",
    "filename": "example.jpg",
    "mime_type": "image/jpeg"
} 
*/

header('Content-Type: application/json; charset=utf-8');
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: PUT, GET, POST");

$response = array();
$upload_dir = 'uploads/';
$server_url = 'http://127.0.0.1:8000';

$inputJSON = file_get_contents('php://input');
$input = json_decode($inputJSON, true);

if(isset($input['file_base64']) && isset($input['filename']) && isset($input['mime_type'])) {
    $file_base64 = $input['file_base64'];
    $filename = $input['filename'];
    $mime_type = $input['mime_type'];

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
        "message" => "Incomplete JSON input!"
    );
}

echo json_encode($response);
?>
