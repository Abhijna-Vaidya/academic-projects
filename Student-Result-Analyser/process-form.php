  
<?php

if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    exit('POST request method required');
}

$usn=strtoupper($_POST["usn"]); 



if ($_FILES["pdffile"]["error"] !== UPLOAD_ERR_OK) {

    switch ($_FILES["pdffile"]["error"]) {
        case UPLOAD_ERR_PARTIAL:
            exit('File only partially uploaded');
            break;
        case UPLOAD_ERR_NO_FILE:
            exit('No file was uploaded');
            break;
        case UPLOAD_ERR_EXTENSION:
            exit('File upload stopped by a PHP extension');
            break;
        case UPLOAD_ERR_FORM_SIZE:
            exit('File exceeds MAX_FILE_SIZE in the HTML form');
            break;
        case UPLOAD_ERR_INI_SIZE:
            exit('File exceeds upload_max_filesize in php.ini');
            break;
        case UPLOAD_ERR_NO_TMP_DIR:
            exit('Temporary folder not found');
            break;
        case UPLOAD_ERR_CANT_WRITE:
            exit('Failed to write file');
            break;
        default:
            exit('Unknown upload error');
            break;
    }
}

if ( $_FILES["pdffile"]["type"]!="application/pdf") {
    
    exit("Invalid file type");
}

$pathinfo = pathinfo($_FILES["pdffile"]["name"]);

$filename = $usn . "." . $pathinfo["extension"];

$destination = __DIR__ ."//uploads//". $filename;



if ( ! move_uploaded_file($_FILES["pdffile"]["tmp_name"], $destination)) {

    exit("Can't move uploaded file");

}

echo "File uploaded successfully.";

$output=exec("python C://wamp64//www//result_analysis//uploads//dbimport.py $usn $destination");
// var_dump($output);
echo  "<br/>";
echo  $output;


?>
