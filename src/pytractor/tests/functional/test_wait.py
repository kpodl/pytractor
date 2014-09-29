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


class AngularWaitTest(TestCase):
    """Test case class for testing waiting for angular."""
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
        self.driver.get('index.html#/async')

    def test_waits_for_http_calls(self):
        status = self.driver.find_element_by_binding('slowHttpStatus')
        button = self.driver.find_element_by_css_selector(
            '[ng-click="slowHttp()"]'
        )
        self.assertEqual(status.text, 'not started')

        button.click()

        self.assertEqual(status.text, 'done')

    def test_waits_for_long_javascript_execution(self):
        status = self.driver.find_element_by_binding('slowFunctionStatus')
        button = self.driver.find_element_by_css_selector(
            '[ng-click="slowFunction()"]'
        )
        self.assertEqual(status.text, 'not started')

        button.click()

        self.assertEqual(status.text, 'done')

    def test_does_not_wait_for_timeout(self):
        status = self.driver.find_element_by_binding('slowTimeoutStatus')
        button = self.driver.find_element_by_css_selector(
            '[ng-click="slowTimeout()"]'
        )
        self.assertEqual(status.text, 'not started')

        button.click()

        self.assertEqual(status.text, 'pending...')

    def test_waits_for_timeout_service(self):
        status = self.driver.find_element_by_binding(
            'slowAngularTimeoutStatus'
        )
        button = self.driver.find_element_by_css_selector(
            '[ng-click="slowAngularTimeout()"]'
        )
        self.assertEqual(status.text, 'not started')

        button.click()

        self.assertEqual(status.text, 'done')

    def test_waits_for_timeout_service_then_a_promise(self):
        status = self.driver.find_element_by_binding(
            'slowAngularTimeoutPromiseStatus'
        )
        button = self.driver.find_element_by_css_selector(
            '[ng-click="slowAngularTimeoutPromise()"]'
        )
        self.assertEqual(status.text, 'not started')

        button.click()

        self.assertEqual(status.text, 'done')

    def test_waits_for_long_http_call_then_a_promise(self):
        status = self.driver.find_element_by_binding('slowHttpPromiseStatus')
        button = self.driver.find_element_by_css_selector(
            '[ng-click="slowHttpPromise()"]'
        )
        self.assertEqual(status.text, 'not started')

        button.click()

        self.assertEqual(status.text, 'done')

    def test_waits_for_slow_routing_changes(self):
        status = self.driver.find_element_by_binding('routingChangeStatus')
        button = self.driver.find_element_by_css_selector(
            '[ng-click="routingChange()"]'
        )
        self.assertEqual(status.text, 'not started')

        button.click()

        self.assertIn('polling mechanism', self.driver.page_source)

    def test_waits_for_slow_ng_include_templates_to_load(self):
        status = self.driver.find_element_by_css_selector('.included')
        button = self.driver.find_element_by_css_selector(
            '[ng-click="changeTemplateUrl()"]'
        )
        self.assertEqual(status.text, 'fast template contents')

        button.click()

        # need to refetch status as the element has been removed from the DOM
        status = self.driver.find_element_by_css_selector('.included')
        self.assertEqual(status.text, 'slow template contents')
