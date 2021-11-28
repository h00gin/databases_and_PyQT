# -*- coding: utf8 -*-
"""Program-client"""

import json
import socket
import sys
import time
import argparse
import logging
import threading
import dis


from errors import IncorrectDataRecivedError, ReqFieldMissingError, ServerError
from decos import log
from common.variables import USER, ACTION, PRESENCE, TIME, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_IP_ADDRESS, \
    DEFAULT_PORT, MESSAGE, SENDER, MESSAGE_TEXT, DESTINATION, EXIT
from utils import send_message, get_message

CLIENT_LOGGER = logging.getLogger('client')


class ClientVerifier(type):

    def __init__(self, clsname, bases, clsdict):
        try:
            for key, value in clsdict.items():
                if type(value) is socket.socket:
                    raise Exception
        except Exception as e:
            print('Неверный тип данных!')

        list_ip = []
        for el in dis.Bytecode(clsname):
            el = list(el)
            try:
                for i in el:
                    if i == 'listen' or i == 'accept':
                        raise Exception
                    elif i == 'AF_INET':
                        list_ip.append(i)
            except Exception as e:
                print('Таких конструкций быть не должно!')
        try:
            if len(list_ip) > 1:
                raise Exception
        except Exception as e:
            print('Не использован протокол TCP для сокета!')

        type.__init__(self, clsname, bases, clsdict)


class Client(metaclass=ClientVerifier):

    def __init__(self, server_address, server_port, client_name):
        self.server_address = server_address
        self.server_port = server_port
        self.client_name = client_name

    @log
    def create_exit_message(self, account_name):
        return {
            ACTION: EXIT,
            TIME: time.time(),
            ACCOUNT_NAME: account_name
        }

    @log
    def message_from_server(self, sock, my_username):
        while True:
            try:
                message = get_message(sock)
                if ACTION in message and message[ACTION] == MESSAGE and SENDER in message and MESSAGE_TEXT in message\
                        and message[DESTINATION] == my_username:
                    print(f'\nПолучено сообщение от пользователя {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
                    CLIENT_LOGGER.info(f'Получено сообщение от пользователя {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
                else:
                    CLIENT_LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')
            except IncorrectDataRecivedError:
                CLIENT_LOGGER.error(f'Не удалось декодировать полученное сообщение.')
            except (OSError, ConnectionError, ConnectionAbortedError, ConnectionResetError, json.JSONDecodeError):
                CLIENT_LOGGER.critical(f'Потеряно соединение с сервером. ')
                break

    @log
    def create_message(self, sock, account_name='Guest'):
        to_user = input('Введите получателя сообщения: ')
        message = input('Введите сообщение для отправки: ')
        message_dict = {
            ACTION: MESSAGE,
            SENDER: account_name,
            DESTINATION: to_user,
            TIME: time.time(),
            MESSAGE_TEXT: message
        }
        CLIENT_LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')
        try:
            send_message(sock, message_dict)
            CLIENT_LOGGER.info(f'Отправлено сообщения для пользователя {to_user}')
        except:
            CLIENT_LOGGER.critical('Потеряно соединение с сервером. ')
            sys.exit(1)

    @log
    def user_interactive(self, sock, username):
        self.print_help()
        print(f'Имя пользователя: {username}')
        while True:
            command = input('Введите команду: ')
            if command == 'message':
                self.create_message(sock, username)
            elif command == 'help':
                self.print_help()
            elif command == 'exit':
                send_message(sock, self.create_exit_message(username))
                print('Завершение соединения. ')
                CLIENT_LOGGER.info('Завершение работы по команде пользователя. ')
                time.sleep(0.5)
                break
            else:
                print('Команда не распознана, попробуйте снова. Введите "help", чтобы вывести команды. ')

    @log
    def create_presence(self, account_name):
        out_dict = {
            ACTION: PRESENCE,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: account_name
            }
        }
        CLIENT_LOGGER.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
        return out_dict

    @log
    def print_help(self):
        print('Поддерживаемые команды: ')
        print('message - отправить сообщение. ')
        print('help - помощь. ')
        print('exit - выход. ')

    @log
    def answer_server(self, message):
        CLIENT_LOGGER.debug(f'Разбор сообщения от сервера: {message}')
        if RESPONSE in message:
            if message[RESPONSE] == 200:
                return 'Ответ от сервера получен 200: OK'
            elif message[RESPONSE] == 400:
                raise ServerError(f'400: {message[ERROR]}')
        raise ReqFieldMissingError(RESPONSE)

    @log
    def create_arg_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
        parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
        parser.add_argument('-n', '--name', default=None, nargs='?')
        namespace = parser.parse_args(sys.argv[1:])
        server_address = namespace.addr
        server_port = namespace.port
        client_name = namespace.name

        if not 1023 < server_port < 65536:
            CLIENT_LOGGER.critical(
                f'Попытка запуска клиента с неподходящим номером порта: {server_port}.'
                f'Допустипы адреса с 1024 до 65535. Клиент завершается')
            sys.exit(1)

        return server_address, server_port, client_name


def main():
    client_1 = Client(DEFAULT_IP_ADDRESS, DEFAULT_PORT, '1')
    # client_1 = Client()
    server_address, server_port, client_name = client_1.create_arg_parser()

    print(f'Консольный мессенджер. Клиентский модуль. ')

    if not client_name:
        client_name = input('Введите имя пользователя: ')

    CLIENT_LOGGER.info(
        f'Запущен клиент с парамертами: адрес сервера: {server_address}, '
        f'порт: {server_port}, имя пользователя: {client_name}')

    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        send_message(transport, client_1.create_presence(client_name))
        answer = client_1.answer_server(get_message(transport))
        CLIENT_LOGGER.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
        print(f'Установлено соединение с сервером.')
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать полученную Json строку.')
        sys.exit(1)
    except ServerError as error:
        CLIENT_LOGGER.error(f'При установке соединения сервер вернул ошибку: {error.text}')
        sys.exit(1)
    except ReqFieldMissingError as missing_error:
        CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
        sys.exit(1)
    except (ConnectionRefusedError, ConnectionError):
        CLIENT_LOGGER.critical(
            f'Не удалось подключиться к серверу {server_address}:{server_port}, '
            f'конечный компьютер отверг запрос на подключение.')
        sys.exit(1)
    else:
        receiver = threading.Thread(target=client_1.message_from_server, args=(transport, client_name))
        receiver.daemon = True
        receiver.start()

        user_interface = threading.Thread(target=client_1.user_interactive, args=(transport, client_name))
        user_interface.daemon = True
        user_interface.start()
        CLIENT_LOGGER.debug('Запущены процессы. ')

        while True:
            time.sleep(1)
            if receiver.is_alive() and user_interface.is_alive():
                continue
            break


if __name__ == '__main__':
    main()
