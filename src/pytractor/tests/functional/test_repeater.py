# encoding: utf-8
# Copyright 2015 Michal Walkowski
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

from pytractor.tests.functional.testdriver import TestDriver
from pytractor.tests.functional.testserver import SimpleWebServerProcess

from selenium.common.exceptions import NoSuchElementException

class RepeaterTestCase(unittest.TestCase):
    """Test case class for testing repeater."""

    @classmethod
    def setUpClass(cls):
        cls.driver = TestDriver('http://localhost:{}/'.format(SimpleWebServerProcess.PORT))

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.get('index.html#/repeater')

    def test_find_elements_by_repeater_returns_correct_element(self):
        element = self.driver.find_elements_by_repeater('allinfo in days')
        self.assertEqual(len(element), 5)
        self.assertEqual(element[0].text, 'M Monday')
        self.assertEqual(element[1].text, 'T Tuesday')
        self.assertEqual(element[2].text, 'W Wednesday')
        self.assertEqual(element[3].text, 'Th Thursday')
        self.assertEqual(element[4].text, 'F Friday')

    def test_find_element_by_repeater_returns_empty_list(self):
        self.assertFalse(self.driver.find_elements_by_repeater('no-such in days'))
