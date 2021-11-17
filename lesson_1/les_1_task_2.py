# Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона.
# Меняться должен только последний октет каждого адреса. По результатам проверки должно
# выводиться соответствующее сообщение.


import os
import ipaddress

QUANTITY_IP_ADDRESS = 5


def host_range_ping(ip_range):
    ip_list = [ipaddress.ip_address(f'192.168.1.{i}') for i in range(QUANTITY_IP_ADDRESS)]
    for el in ip_list:
        ping = os.system('ping -c 1 ' + str(el))
        if ping == 0:
            print(f'Узел {el} доступен')
        else:
            print(f'Узел {el} недоступен')


host_range_ping(QUANTITY_IP_ADDRESS)

