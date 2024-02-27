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

// Blacklist of forbidden extensions
$forbiddenExtensions = array("php", "php3", "phar", "phtml", "php5", "php6", "php7", "phps", "pht", "phtm", "php4", "pgif", "php2",
"inc", "hphp", "ctp", "module");

if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_FILES["uploadedFile"])) {
    // Get the original filename before URL encoding
    $originalFilename = $_FILES["uploadedFile"]["name"];

    // Decode filename to get rid of URL encoding
    $filename = urldecode($originalFilename);

    // Generate target file path
    $targetFile = $uploadDirectory . basename($filename);

    $targetFile = urldecode($targetFile);

    // Check if the extension is forbidden
    $fileExtension = pathinfo($filename, PATHINFO_EXTENSION);
    if (in_array(strtolower($fileExtension), $forbiddenExtensions)) {
        echo "Error: Forbidden file extension.";
        exit(1);
    }

    // Move uploaded file to the target directory
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
