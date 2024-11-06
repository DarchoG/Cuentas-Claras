<?php
    //Actualizar dinero reservado
    include_once ("Conecta.php");
    $con = Conect::conecta();
    $cantidad = $_REQUEST['dinero_reservado'];


    $sql = "UPDATE tarjetas
    SET dinero_reservado = $cantidad 
    WHERE id_tarjeta = 1";
    $res = $con->query($sql);
    if ($res) {
        
        header("Location: ahorros.php"); 
        exit(); 
    } else {
       
        echo "Error al actualizar el dinero reservado.";
    }

?>