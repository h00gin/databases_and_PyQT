# Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться доступность
# сетевых узлов. Аргументом функции является список, в котором каждый сетевой узел должен быть
# представлен именем хоста или ip-адресом. В функции необходимо перебирать ip-адреса и проверять
# их доступность с выводом соответствующего сообщения («Узел доступен», «Узел недоступен»).
# При этом ip-адрес сетевого узла должен создаваться с помощью функции ip_address().

import os
import ipaddress

QUANTITY_IP_ADDRESS = 5

ip_list = [ipaddress.ip_address(f'192.168.1.{i}') for i in range(QUANTITY_IP_ADDRESS)]


def host_ping(list_ip):
    for el in list_ip:
        ping = os.system('ping -c 1 ' + str(el))
        if ping == 0:
            print(f'Узел {el} доступен')
        else:
            print(f'Узел {el} недоступен')


host_ping(ip_list)


