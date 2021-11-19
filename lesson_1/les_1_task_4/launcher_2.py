# -*- coding: utf8 -*-
"""Launcher"""

import subprocess

PROCESS = []

while True:
    ACTION = input('Выберите действие: s - запустить сервер и клиенты, x - закрыть все окна, q - выход: ')
    if ACTION == 'q':
        break
    elif ACTION == 's':

        QUANTITY_ACTION = int(input('Введите количество клиентских приложений: '))
        for i in range(QUANTITY_ACTION):
            PROCESS.append(subprocess.Popen('python server.py', creationflags=subprocess.CREATE_NEW_CONSOLE))
            PROCESS.append(subprocess.Popen(f'python client.py -n test{i+1}', creationflags=subprocess.CREATE_NEW_CONSOLE))

    elif ACTION == 'x':
        while PROCESS:
            VICTIM = PROCESS.pop()
            VICTIM.kill()

