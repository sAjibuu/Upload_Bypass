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

if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_FILES["uploadedFile"])) {
    $targetFile = $uploadDirectory . basename($_FILES["uploadedFile"]["name"]);
    
    if (move_uploaded_file($_FILES["uploadedFile"]["tmp_name"], $targetFile)) {
        echo "File uploaded successfully.";
    } else {
        echo "Error uploading file. Details: " . print_r(error_get_last(), true);
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
