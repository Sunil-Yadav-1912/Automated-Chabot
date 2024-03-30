import subprocess

from config import php_path


def encrypt(message):
    proc = subprocess.Popen("php " + php_path + "enc.php " + message, shell=True, stdout=subprocess.PIPE)
    script_response = proc.stdout.read()

    return script_response.decode("utf-8")


def decrypt(message):
    proc = subprocess.Popen(
        "php " + php_path + "dec.php " + message,
        shell=True, stdout=subprocess.PIPE)
    script_response = proc.stdout.read()

    return script_response.decode("utf-8")
