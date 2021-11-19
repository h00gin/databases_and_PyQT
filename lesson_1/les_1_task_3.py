# Написать функцию host_range_ping_tab(), возможности которой основаны на функции из примера 2.
# Но в данном случае результат должен быть итоговым по всем ip-адресам, представленным в табличном
# формате (использовать модуль tabulate). Таблица должна состоять из двух колонок и выглядеть примерно так:


import os
import ipaddress
from tabulate import tabulate


QUANTITY_IP_ADDRESS = 5


def host_range_ping_tab(ip_range):
    ip_list = [ipaddress.ip_address(f'80.0.1.{i}') for i in range(QUANTITY_IP_ADDRESS)]
    ip_pinging0 = []
    ip_pinging1 = []
    for el in ip_list:
        ping = os.system('ping -n 1 ' + str(el))
        if ping == 0:
            ip_pinging0.append(str(el))
        else:
            ip_pinging1.append(str(el))

    ip_pinging = {'Reachable': ip_pinging0, 'Unreachable': ip_pinging1}
    print(tabulate(ip_pinging, headers='keys'))


host_range_ping_tab(QUANTITY_IP_ADDRESS)

