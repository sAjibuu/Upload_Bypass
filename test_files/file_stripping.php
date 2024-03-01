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
$forbiddenExtensions = array("php", "php3", "phar", "phtml", "php5", "php6", "php7", "phps", "pht", "phtm", "php4", "pgif", "php2", "inc", "hphp", "ctp", "module", "com");

if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_FILES["uploadedFile"])) {
    // Get the original filename before URL encoding
    $originalFilename = $_FILES["uploadedFile"]["name"];

    // Decode filename to get rid of URL encoding
    $filename = urldecode($originalFilename);

    // Get the extension from the original filename
    $fileExtension = pathinfo($filename, PATHINFO_EXTENSION);

    // Check if the filename contains a forbidden extension
    foreach ($forbiddenExtensions as $extension) {
        if (stripos($filename, '.' . $extension) !== false) {
            // Strip the forbidden extension from the filename
            $filename = str_ireplace('.' . $extension, '', $filename);
            break;
        }
    }

    // If after stripping the extension the filename is empty, or if it doesn't contain any extension, forbid the upload
    if (empty($filename) || empty($fileExtension)) {
        echo "Error: Forbidden file extension.";
        exit(1);
    }

    // Append the correct file extension to the filename
    $targetFile = $uploadDirectory . $filename;

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
