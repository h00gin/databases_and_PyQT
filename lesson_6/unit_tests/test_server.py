"""Unit-tests server"""

import sys
import os
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from server import client_message

from common.variables import TIME, ACTION, PRESENCE, USER, ACCOUNT_NAME, RESPONSE, ERROR


class TestServer(unittest.TestCase):
    error_dict = {
        RESPONSE: 400,
        ERROR: 'Bad request'
    }

    good_dict = {RESPONSE: 200}

    def test_not_action(self):
        self.assertEqual(client_message({TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}}), self.error_dict)

    def test_wrong_action(self):
        self.assertEqual(client_message({ACTION: 'Wrong', TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}}), self.error_dict)

    def test_not_time(self):
        self.assertEqual(client_message({ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Guest'}}), self.error_dict)

    def test_no_user(self):
        self.assertEqual(client_message({ACTION: PRESENCE, TIME: '1.1'}), self.error_dict)

    def test_unknown_user(self):
        self.assertEqual(client_message(
            {ACTION: PRESENCE, TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest_1'}}), self.error_dict)

    def test_good_request(self):
        self.assertEqual(client_message({ACTION: PRESENCE, TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}}), self.good_dict)


if __name__ == '__main__':
    unittest.main()