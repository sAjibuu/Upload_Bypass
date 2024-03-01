<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $target_dir = "uploads/";
    $uploadOk = 1;

    // Check if file is an SVG file
    $fileType = strtolower(pathinfo($_FILES["fileToUpload"]["name"], PATHINFO_EXTENSION));
    if ($fileType != "svg") {
        echo "Sorry, only SVG files are allowed.";
        $uploadOk = 0;
    }

    // Check file size (you can modify this based on your needs)
    if ($_FILES["fileToUpload"]["size"] > 500000) {
        echo "Sorry, your file is too large.";
        $uploadOk = 0;
    }

    // Check if file already exists
    $target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
    if (file_exists($target_file)) {
        echo "Sorry, file already exists.";
        $uploadOk = 0;
    }

    // If everything is OK, try to upload the file
    if ($uploadOk == 1) {
        if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
            echo "The file ". htmlspecialchars(basename($_FILES["fileToUpload"]["name"])). " has been uploaded.";

            // Display the contents of the uploaded SVG file
            $svg_content = file_get_contents($target_file);
            echo "<br><br>SVG Content:<br>";
            echo $svg_content;
        } else {
            echo "Sorry, there was an error uploading your file.";
        }
    }
}
?>

<!DOCTYPE html>
<html>
<body>

<h2>Upload SVG File</h2>
<form action="<?php echo $_SERVER["PHP_SELF"]; ?>" method="post" enctype="multipart/form-data">
  Select SVG file to upload:
  <input type="file" name="fileToUpload" id="fileToUpload" accept=".svg">
  <input type="submit" value="Upload" name="submit">
</form>

</body>
</html>
