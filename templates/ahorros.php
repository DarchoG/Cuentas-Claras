<?php
    include_once ("Conecta.php");
    $con = Conect::conecta();
    $sql = "SELECT * FROM vista_ahorros_usuario";
    $res = $con->query($sql);
    $row = $res->fetch(PDO::FETCH_ASSOC);

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ahorros</title>
    <link rel="stylesheet" href="CSS/stylesahorros.css">
    <link rel="stylesheet" href="CSS/StyleContenidos.CSS">
    <link rel="stylesheet" href="CSS/normalize.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" />
    <script src="js/jquery-3.3.1.min.js"></script>
</head>
<body>

    {% extends "menu.html" %}

    <main>
        <h2>Ahorros</h2>
            
    </main>
    <div class= "Contenedor-padre"> 
        <div class= "Contenedor-hijo">
            <?php
                $id_usuario = $row["id_usuario"];
                $dinero_reservado = $row["dinero_reservado"];

                echo "<div class='cuadrito' >";
                echo "<div id=dinero_signo>";
                echo "<div id='signo'>$</div>";
                echo "<div><input type='number' id='dinero_modificado' class='dinero' value='$dinero_reservado' step='0.01'></div>";
                echo "</div>";

                echo "<div id=ahorro>Ahorro Total</div>";
                
                echo "<div><button class='btn secondary' onclick='enviaDatos()'>Modificar</button></div>";
                echo "</div>";
             

            ?>
        </div>

    </div>
    <form name="Forma01" method="POST" action="dinero_reservado_actualizar.php" style="display:none;" submit = false>
        <input type="hidden" name="dinero_reservado" id="dinero_reservado">
    </form>
    <script>
           function enviaDatos() {
            // Obtener el valor del dinero modificado desde el campo de entrada
            var cantidad = $('#dinero_modificado').val();  // Capturamos el valor del campo input

            // Validar que la cantidad no sea negativa
            if (cantidad < 0) {
                $('#mensaje').html('No puede ingresar números negativos');
                setTimeout(function() { $('#mensaje').html(''); }, 3000);
            } else {
                // Asignar el valor al campo oculto del formulario
                $('#dinero_reservado').val(cantidad);

                // Enviar el formulario
                document.Forma01.submit();
            }
        }
    </script>
    <script src="js/script.js"></script>
</body>
</html>