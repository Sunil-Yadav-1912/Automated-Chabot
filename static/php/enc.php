<?php
function wall_encrypt($message, $type = false, $key = '')
{
    try {

        if ($key == ''){
            $key ='CRDRIAF';
        }
        $cipher = "AES-128-CBC";
        //$ivlen = openssl_cipher_iv_length($cipher = "AES-128-CBC");
        //$iv = openssl_random_pseudo_bytes($ivlen);
        $iv = "lksdasfsaskllopl";
        $ciphertext_raw = openssl_encrypt($message, $cipher, $key, $options = OPENSSL_RAW_DATA, $iv); // openssl encryption
        $hmac = hash_hmac('sha256', $ciphertext_raw, $key, $as_binary = true);  // hashing using sha256
        $value = base64_encode($iv . $hmac . $ciphertext_raw);  // base64 encoding

        echo $value;
    }catch (Exception $e){
        echo $message;

    }
}

wall_encrypt($argv[1]);
// wall_encrypt('9920527883');