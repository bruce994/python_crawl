<?php
date_default_timezone_set('Asia/Shanghai');


//$domain = "http://m.azhibo.com/nbazhibo/jueshivskaituozhe.html";
$domain = $_GET['url'] ? base64_decode($_GET['url']) : "http://m.azhibo.com/";
//echo $domain;
$output = shell_exec('/home/python_vir1/bin/python /home/www/Test/live.zz.lanrenmb.com/tutorial/index.py '.$domain);
echo $output;


