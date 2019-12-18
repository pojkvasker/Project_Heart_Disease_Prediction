<?php
    // Start the training script
    exec('C:\xampp\htdocs\Working_Prototype_Dwnld_ML_1.0\logreg_training.py ');

    $fh = fopen('ParametersLogReg.txt','r');
    $output = fgets($fh);
    fclose($fh);

    // Echo the parameters
    echo $output; 
?>