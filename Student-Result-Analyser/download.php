<?php
$output=exec("python C://wamp64//www//result_analysis//db_to_excel.py ");

// Path to the file to be downloaded
$file_url = 'C://wamp64//www//result_analysis//result_analysis.xlsx'; // Replace this with the actual path to your file

// Check if the file exists
if (file_exists($file_url)) {
    // Set headers for file download
    header('Content-Type: application/octet-stream');
    header('Content-Disposition: attachment; filename="' . basename($file_url) . '"');
    header('Content-Length: ' . filesize($file_url));
    
    // Read the file and output its contents
    readfile($file_url);
    exit;
} else {
    echo "File not found.";
}
?>
