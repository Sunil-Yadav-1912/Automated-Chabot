<?php

function wall_decrypt($msg_bundle, $type = false, $key = '')
{
    if ($key == ''){
        $key ='CRDRIAF';
    }

    try {
        $c = base64_decode($msg_bundle);
        $ivlen = openssl_cipher_iv_length($cipher = "AES-128-CBC"); //AES-256-CBC
        $iv = substr($c, 0, $ivlen);
        $hmac = substr($c, $ivlen, $sha2len = 32);
        $ciphertext_raw = substr($c, $ivlen + $sha2len);
        $value = openssl_decrypt($ciphertext_raw, $cipher, $key, $options = OPENSSL_RAW_DATA, $iv);
        $calcmac = hash_hmac('sha256', $ciphertext_raw, $key, $as_binary = true);
        if (hash_equals($hmac, $calcmac)) {
            echo $value;
        }else{
            echo ($type) ? false : $msg_bundle;
        }
    }catch(Exception $e){
        echo ($type) ? false : $msg_bundle;

    }
}

wall_decrypt($argv[1]);
