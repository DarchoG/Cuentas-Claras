<?php
// funciones/conecta.php
class Conect
{   
    public static function conecta(){
        $host = "localhost";
        $dbname = "SelfBank";
        $username = "postgres";
        $pasword = "depajo";
    
        try {
            $conn = new PDO("pgsql:host=$host;dbname=$dbname", $username, $pasword);
            $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            return $conn;
        } catch (PDOException $exp) {
            echo "No se conectó correctamente: " . $exp->getMessage();
            return null;
        }
    }
}
?>
