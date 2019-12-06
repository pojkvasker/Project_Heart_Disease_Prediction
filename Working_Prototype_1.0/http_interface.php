<?php
    $age = $_GET['Age'];
    $sex = $_GET['Sex'];
    $bp = $_GET['BP'];
    $chol = $_GET['Chol'];
    $ecg = $_GET['Ecg'];
    $exang = $_GET['Exang'];
    $id = $_GET['Id'];
    
    exec('C:\xampp\htdocs\Working_Prototype_1.0\server_prediction.py '.  $age." ".$sex." ". $bp." ". $chol." ". $ecg." ". $exang);

    $fh = fopen('Output.txt','r');
    //while ($line = fgets($fh)) {
        // <... Do your work with the line ...>
    //    echo($line);
    //}
    $output = fgets($fh);
    fclose($fh);

    $array = explode(", ", $output);
    $pred = $array[1];
    $prob = $array[2];
    
    exec('C:\xampp\htdocs\Working_Prototype_1.0\writeDB.py '.  $age." ".$sex." ". $bp." ". $chol." ". $ecg." ". $exang." ". $id. " ". $pred." ". $prob);
    
    echo $output;
    
?>