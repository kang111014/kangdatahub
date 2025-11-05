<?php
$servername = "localhost";   // 您的資料庫主機
$username = "root";          // 您的資料庫使用者名稱
$password = "willkang11727";              // 您的資料庫密碼
$dbname = "your_database";   // 您的資料庫名稱

// 建立連線
$conn = new mysqli($servername, $username, $password, $dbname);

// 檢查連線
if ($conn->connect_error) {
    die("資料庫連線失敗: " . $conn->connect_error);
}

// 設定字元集為 utf8mb4
$conn->set_charset("utf8mb4");
?>