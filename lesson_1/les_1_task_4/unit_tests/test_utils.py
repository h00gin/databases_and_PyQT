"""Unit-tests utils"""

import sys
import os
import unittest
import json
sys.path.append(os.path.join(os.getcwd(), '..'))
from common.utils import get_message, send_message

from common.variables import TIME, ACTION, PRESENCE, USER, ACCOUNT_NAME, RESPONSE, ERROR, ENCODING


class TestSocket:
    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.reserved_message = None

    def send(self, message_to_send):
        json_test_message = json.dumps(self.test_dict)
        self.encoded_message = json_test_message.encode(ENCODING)
        self.reserved_message = message_to_send

    def recv(self, max_len):
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode(ENCODING)


class Tests(unittest.TestCase):
    test_dict_send = {
        ACTION: PRESENCE,
        TIME: 111111.111111,
        USER: {ACCOUNT_NAME: 'test_user'}
    }

    test_dict_receive_good = {RESPONSE: 200}
    test_dict_receive_error = {RESPONSE: 400, ERROR: 'Bad request'}

    def test_send_message(self):
        test_socket = TestSocket(self.test_dict_send)
        send_message(test_socket, self.test_dict_send)
        self.assertEqual(test_socket.encoded_message, test_socket.reserved_message)
        with self.assertRaises(Exception):
            send_message(test_socket, test_socket)

    def test_get_message(self):
        test_sock_good = TestSocket(self.test_dict_receive_good)
        test_sock_error = TestSocket(self.test_dict_receive_error)
        self.assertEqual(get_message(test_sock_good), self.test_dict_receive_good)
        self.assertEqual(get_message(test_sock_error), self.test_dict_receive_error)


if __name__ == '__main__':
    unittest.main()


