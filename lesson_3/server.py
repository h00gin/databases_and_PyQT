# -*- coding: utf8 -*-
"""Program-server"""
import argparse
import dis
import logging
import select
import socket
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import ClientOnServer, ClientHistory, Base

from datetime import datetime

from common.utils import send_message, get_message
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, ERROR, DEFAULT_PORT, \
    MAX_CONNECTIONS, MESSAGE, MESSAGE_TEXT, SENDER, DESTINATION, RESPONSE_200, RESPONSE_400, EXIT, DEFAULT_IP_ADDRESS
from decos import log

SERVER_LOGGER = logging.getLogger('server')


class ServerPort:

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError("Номер порта должен быть больше 0!")
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class ServerVerifier(type):
    def __init__(self, clsname, bases, clsdict):
        list_ip = []
        for el in dis.Bytecode(clsname):
            el = list(el)
            try:
                for i in el:
                    if i == 'connect':
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


class Server(metaclass=ServerVerifier):

    listen_port = ServerPort()

    def __init__(self, listen_port):
        self.listen_port = listen_port

    @log
    def client_message(self, message, message_list, client, clients, names):
        SERVER_LOGGER.debug(f'Разбор сообщения от клиента: {message}')
        if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message:
            if message[USER][ACCOUNT_NAME] not in names.keys():
                names[message[USER][ACCOUNT_NAME]] = client
                send_message(client, RESPONSE_200)
            else:
                response = RESPONSE_400
                response[ERROR] = 'Имя пользователя уже занято. '
                send_message(client, response)
                clients.remove(client)
                client.close()
            return
        elif ACTION in message and message[ACTION] == MESSAGE and DESTINATION in message and \
                TIME in message and SENDER in message and MESSAGE_TEXT in message:
            message_list.append(message)
            return
        elif ACTION in message and message[ACTION] == EXIT and ACCOUNT_NAME in message:
            clients.remove(names[message[ACCOUNT_NAME]])
            names[message[ACCOUNT_NAME]].close()
            del names[message[ACCOUNT_NAME]]
            return
        else:
            response = RESPONSE_400
            response[ERROR] = 'Запрос некорректен. '
            send_message(client, response)
            return

    @log
    def process_message(self, message, names, listen_socks):
        if message[DESTINATION] in names and names[message[DESTINATION]] in listen_socks:
            send_message(names[message[DESTINATION]], message)
            SERVER_LOGGER.info(f'Отправлено сообщение пользователю {message[DESTINATION]} '
                               f'от пользователя {message[SENDER]}. ')
        elif message[DESTINATION] in names and names[message[DESTINATION]] not in listen_socks:
            raise ConnectionError
        else:
            SERVER_LOGGER.error(f'Пользователь {message[DESTINATION]} '
                                f'не зарегестрирован на сервере, отправка сообщений невозможна. ')

    @log
    def create_arg_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
        parser.add_argument('-a', default='', nargs='?')
        namespace = parser.parse_args(sys.argv[1:])
        listen_address = namespace.a
        listen_port = namespace.p
        if not 1023 < listen_port < 65536:
            SERVER_LOGGER.critical(f'Попытка запуска сервера с указанием неподходящего порта '
                                   f'{listen_port}. Допустимы адреса с 1024 по 65535.')
            sys.exit(1)
        return listen_address, listen_port


def main():
    server_1 = Server(DEFAULT_PORT)

    listen_address, listen_port = server_1.create_arg_parser()

    engine = create_engine('sqlite:///clients.db', echo=True)
    metadata = Base.metadata
    metadata.create_all(engine)

    SERVER_LOGGER.info(f'Запушен сервер, порт для подключений: {listen_port}'
                       f'Адрес, с которого принимаются подключения: {listen_address}'
                       f'Если не указан адрес, принимаются соединения с любых адресов.')

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    transport.settimeout(0.5)

    clients = []
    messages = []
    names = dict()

    transport.listen(MAX_CONNECTIONS)

    while True:
        try:
            client, client_address = transport.accept()

        except OSError:
            pass
        else:
            SERVER_LOGGER.info(f'Установлено соединение с ПК {client_address}')
            clients.append(client)

        recv_data_lst = []
        send_data_lst = []
        err_lst = []

        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass

        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    server_1.client_message(get_message(client_with_message),
                                            messages, client_with_message, clients, names)
                    with Session(engine) as session:
                        session.begin()
                        try:
                            if client_with_message.getpeername() != ClientOnServer.login:
                                session.add(ClientOnServer(client_with_message.getpeername(), ' '))
                                session.add(ClientHistory(datetime.now(), DEFAULT_IP_ADDRESS))
                            else:
                                session.add(ClientHistory(datetime.now(), DEFAULT_IP_ADDRESS))
                        except:
                            session.rollback()
                            raise
                        else:
                            session.commit()
                except Exception:
                    SERVER_LOGGER.info(f'Клиент {client_with_message.getpeername()} отключился от сервера.')
                    clients.remove(client_with_message)

        for i in messages:
            try:
                server_1.process_message(i, names, send_data_lst)
            except Exception:
                SERVER_LOGGER.info(f'Связь с клиентом с именем {i[DESTINATION]} была потеряна. ')
                clients.remove(names[i[DESTINATION]])
                del names[i[DESTINATION]]
        messages.clear()


if __name__ == '__main__':
    main()
    



