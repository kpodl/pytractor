# Copyright 2014 Konrad Podloucky
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
"""
Contains tests that wait for angular's processing to finish.
"""

from unittest import TestCase

from .testdriver import TestDriver
from .testserver import SimpleWebServerProcess


class HelperFunctionTestCase(TestCase):
    """Tests for helper functions."""
    driver = None

    @classmethod
    def setUpClass(cls):
        cls.driver = TestDriver(
            'http://localhost:{}/'.format(SimpleWebServerProcess.PORT),
            'body'
        )

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.get('index.html')

    def test_location_abs_url_returns_absolute_url(self):
        url = self.driver.location_abs_url
        self.assertIn('/form', url)

        repeater_button = self.driver.find_element_by_link_text('repeater')
        repeater_button.click()
        url = self.driver.location_abs_url

        self.assertIn('/repeater', url)

    def test_set_location_navigates_to_another_url(self):
        self.driver.set_location('/repeater')
        url = self.driver.location_abs_url

        self.assertIn('/repeater', url)
