# -*- coding: utf8 -*-
# Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона.
# Меняться должен только последний октет каждого адреса. По результатам проверки должно
# выводиться соответствующее сообщение.


import os
import ipaddress

RANGE_IP_ADDRESS = 28


def host_range_ping(ip_range):
    ip_list = ipaddress.ip_network(f'80.0.1.0/{ip_range}')
    print(ip_list)
    for el in ip_list:
        ping = os.system('ping -n 1 ' + str(el))
        if ping == 0:
            print(f'Узел {el} доступен')
        else:
            print(f'Узел {el} недоступен')


host_range_ping(RANGE_IP_ADDRESS)

