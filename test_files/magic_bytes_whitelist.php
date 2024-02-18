<!DOCTYPE html>
<html>
<head>
    <title>File Uploader</title>
</head>
<body>

<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
$uploadDirectory = "uploads/";

function is_png($file_path) {
    // Open the file in binary mode
    $file_handle = fopen($file_path, 'rb');

    // Read the first 8 bytes to check the signature
    $signature = fread($file_handle, 8);

    // Close the file handle
    fclose($file_handle);

    // Check if the signature matches the PNG signature
    return $signature === "\x89\x50\x4E\x47\x0D\x0A\x1A\x0A";
}

function is_jpg($file_path) {
    // Open the file in binary mode
    $file_handle = fopen($file_path, 'rb');

    // Read the first 4 bytes to check the signature
    $signature = fread($file_handle, 4);

    // Close the file handle
    fclose($file_handle);

    // Check if the signature matches the JPG signature
    return $signature === "\xFF\xD8\xFF\xE0";
}


function is_gif($file_path) {
    // Open the file in binary mode
    $file_handle = fopen($file_path, 'rb');

    // Read the first 3 bytes to check the signature
    $signature = fread($file_handle, 3);

    // Close the file handle
    fclose($file_handle);

    // Check if the signature matches "GIF"
    return $signature === "GIF";
}

if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_FILES["uploadedFile"])) {
    $targetFile = $uploadDirectory . basename($_FILES["uploadedFile"]["name"]);

    if (!is_jpg($_FILES["uploadedFile"]["tmp_name"])) {
        echo "Error uploading file.";
        exit(1);
    }
    
    if (move_uploaded_file($_FILES["uploadedFile"]["tmp_name"], $targetFile)) {
        echo "File uploaded successfully.";
    } else {
        echo "Error uploading file.";
        exit(1);
    }
}
?>

<form action="<?php echo $_SERVER["PHP_SELF"]; ?>" method="post" enctype="multipart/form-data">
    <label for="uploadedFile">Choose a file to upload:</label>
    <input type="file" name="uploadedFile" id="uploadedFile" required>
    <br>
    <input type="submit" value="Upload File">
</form>

</body>
</html>
