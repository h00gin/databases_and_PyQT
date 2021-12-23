# -*- coding: utf8 -*-
"""Unit-tests client"""

import sys
import os
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from client import create_presence, answer_server

from common.variables import TIME, ACTION, PRESENCE, USER, ACCOUNT_NAME, RESPONSE, ERROR


class TestClass(unittest.TestCase):
    def test_presence(self):
        test = create_presence()
        test[TIME] = 1.1
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_answer_200(self):
        self.assertEqual(answer_server({RESPONSE: 200}), 'Ответ от сервера получен 200: OK')

    def test_answer_400(self):
        self.assertEqual(answer_server({RESPONSE: 400, ERROR: 'Bad Request'}), '400: Bad Request')

    def test_not_response(self):
        self.assertRaises(ValueError, answer_server, {ERROR: 'Bad Request'})


if __name__ == '__main__':
    unittest.main()
