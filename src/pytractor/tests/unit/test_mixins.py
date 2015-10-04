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

import unittest

from mock import MagicMock, patch, PropertyMock, DEFAULT

from selenium.common.exceptions import NoSuchElementException

from pytractor.exceptions import AngularNotFoundException
from pytractor.mixins import (WebDriverMixin, angular_wait_required,
                              CLIENT_SCRIPTS_DIR)


class AngularWaitRequiredDecoratorTest(unittest.TestCase):
    @angular_wait_required
    def wrapped_function(self, *args, **kwargs):
        return self.check_function(*args, **kwargs)

    def check_function(self, *args, **kwargs):
        pass

    def test_angular_wait_required(self):
        with patch.multiple(self, wait_for_angular=DEFAULT,
                            check_function=DEFAULT, create=True) as patched:
            mock_wait_for_angular = patched['wait_for_angular']
            mock_check_function = patched['check_function']
            mock_arg = MagicMock()
            mock_kwarg = MagicMock()
            result = self.wrapped_function(mock_arg, kwarg=mock_kwarg)
        # result should be the result of the wrapped function
        self.assertIs(result, mock_check_function.return_value)
        # wait_for_angular() should have been called
        mock_wait_for_angular.assert_called_once_with()
        # the check function should have been called
        mock_check_function.assert_callled_once_with(mock_arg,
                                                     kwarg=mock_kwarg)


class WebDriverMixinConstructorTest(unittest.TestCase):
    class ConstructorTester(object):
        """Class for checking calls to __init__"""
        def __init__(self, *args, **kwargs):
            self.constructor_called(*args, **kwargs)

        def constructor_called(self, *args, **kwargs):
            """
            This function will be called by __init__. We can hook onto this
            to check for __init__ calls.
            """
            pass

    class TestDriver(WebDriverMixin, ConstructorTester):
        pass

    def test_constructor(self):
        base_url = 'BASEURL'
        root_element = 'ROOTEL'
        test_timeout = 'TESTTIMEOUT'
        script_timeout = 'SCRIPTTIMEOUT'

        with patch(
            '__builtin__.super'
        ) as mock_super, patch.object(
            self.TestDriver, 'set_script_timeout', create=True
        ) as mock_set_script_timeout:
            mock_super.return_value = MagicMock()
            instance = self.TestDriver(base_url, root_element,
                                       test_timeout=test_timeout,
                                       script_timeout=script_timeout)

        # verify that properties have been set
        self.assertIs(instance._base_url, base_url)
        self.assertIs(instance._root_element, root_element)
        self.assertIs(instance._test_timeout, test_timeout)
        # verify that the super class' constructor has been called
        mock_super.return_value.constructor_called.assert_called_once()
        # verify that set_script_timeout has been called
        mock_set_script_timeout.assert_called_once_with(script_timeout)


class WebDriverMixinTest(unittest.TestCase):
    def setUp(self):
        set_script_timeout_patcher = patch.object(
            WebDriverMixin, 'set_script_timeout', create=True
        )
        self.mock_set_script_timeout = set_script_timeout_patcher.start()
        self.addCleanup(set_script_timeout_patcher.stop)
        self.mock_root_element = MagicMock()
        self.instance = WebDriverMixin('http://localhost',
                                       self.mock_root_element)

    @patch('pytractor.mixins.resource_string')
    def verify__execute_client_script_call(self, async, mock_resource_string):
        with patch.multiple(
            self.instance,
            execute_async_script=DEFAULT, execute_script=DEFAULT,
            create=True
        ) as mock_execute:
            (mock_execute_script,
             mock_execute_async_script) = [mock_execute.get(func_name)
                                           for func_name in
                                           ('execute_script',
                                            'execute_async_script')]
            mock_arg = MagicMock()
            result = self.instance._execute_client_script('SCRIPT', mock_arg,
                                                          async=async)
        # the script was read correctly with resource_string()
        mock_resource_string.assert_called_once_with(
            'pytractor.mixins',
            '{}/{}.js'.format(CLIENT_SCRIPTS_DIR, 'SCRIPT')
        )
        # execute_async_script or execute_script were called (but not both)
        script_content = mock_resource_string.return_value
        if async:
            mock_execute_async_script.assert_called_once_with(script_content,
                                                              mock_arg)
            self.assertEqual(len(mock_execute_script.mock_calls), 0)
            # the result is the one from execute_async_script()
            self.assertIs(result, mock_execute_async_script.return_value)
        else:
            mock_execute_script.assert_called_once_with(script_content,
                                                        mock_arg)
            self.assertEqual(len(mock_execute_async_script.mock_calls), 0)
            # the result is the one from execute_script()
            self.assertIs(result, mock_execute_script.return_value)

    def test__execute_client_script_async(self):
        self.verify__execute_client_script_call(True)

    def test__execute_client_script_sync(self):
        self.verify__execute_client_script_call(False)

    def verify_function_executes_script_with(self, func_to_call,
                                             script_name, *script_args):
        with patch.object(
            self.instance, '_execute_client_script'
        ) as mock_execute_client_script:
            result = func_to_call()
        mock_execute_client_script.assert_called_once_with(
            script_name,
            *script_args
        )
        self.assertIs(result, mock_execute_client_script.return_value)

    def test_wait_for_angular(self):
        self.verify_function_executes_script_with(
            self.instance.wait_for_angular,
            'waitForAngular', self.mock_root_element
        )

    def test_wait_for_angular_does_not_call_script_if_ignore_synchronization(
        self
    ):
        """wait_for_angular() must not call the waitForAngular script, if
        ignore_synchronization is set to True."""
        self.instance.ignore_synchronization = True

        with patch.object(
            self.instance, '_execute_client_script'
        ) as mock_execute_client_script:

            self.instance.wait_for_angular()

        self.assertEqual(mock_execute_client_script.call_count, 0)

    def test__test_for_angular(self):
        self.instance._test_timeout = 5000
        self.verify_function_executes_script_with(
            self.instance._test_for_angular,
            'testForAngular', self.instance._test_timeout / 1000
        )

    def test__location_equals(self):
        with patch.object(
            self.instance, 'execute_script', create=True
        ) as mock_execute_script:
            mock_location = MagicMock()
            mock_execute_script.return_value = MagicMock(__eq__=MagicMock())
            result = self.instance._location_equals(mock_location)
        mock_execute_script.assert_called_once_with(
            'return window.location.href'
        )
        script_result = mock_execute_script.return_value
        script_result.__eq__.assert_called_once_with(mock_location)
        self.assertIs(result, script_result.__eq__.return_value)

    # The following tests test some properties that use the wait_for_angular
    # decorator and fetch the property from the super class.
    def verify_super_property_called_with_wait(self, prop_name):
        """
        Verifies that accessing the given property calls the equally
        named property on the super class.
        """
        with patch(
            '__builtin__.super'
        ) as mock_super, patch.object(
            self.instance, 'wait_for_angular'
        ) as mock_wait_for_angular:
            # setup the mocked property
            mock_prop = PropertyMock(name='super.{}'.format(prop_name))
            setattr(type(mock_super.return_value), prop_name, mock_prop)

            result = getattr(self.instance, prop_name)

        mock_wait_for_angular.assert_called_once()
        mock_super.assert_called_once_with(WebDriverMixin, self.instance)
        mock_prop.assert_called_once()
        self.assertIs(result, mock_prop.return_value)

    def test_current_url(self):
        self.verify_super_property_called_with_wait('current_url')

    def test_page_source(self):
        self.verify_super_property_called_with_wait('page_source')

    def test_title(self):
        self.verify_super_property_called_with_wait('title')

    # Tests for methods that delegate to the super method
    def verify_super_method_called_with_wait(self, method_name):
        """
        Verifies that calling the given method calls the equally
        named method on the super class.
        """
        mock_args = [MagicMock(), MagicMock()]
        with patch(
            '__builtin__.super'
        ) as mock_super, patch.object(
            self.instance, 'wait_for_angular'
        ) as mock_wait_for_angular:
            mock_super_method = getattr(mock_super.return_value, method_name)
            method = getattr(self.instance, method_name)
            result = method(*mock_args)

        mock_wait_for_angular.assert_called_once()
        mock_super.assert_called_once_with(WebDriverMixin, self.instance)
        mock_super_method.assert_called_once_with(*mock_args)
        self.assertIs(result, mock_super_method.return_value)

    def test_find_element(self):
        self.verify_super_method_called_with_wait('find_element')

    def test_find_elements(self):
        self.verify_super_method_called_with_wait('find_elements')

    # tests for other methods
    def test_find_elements_by_binding(self):
        mock_descriptor = MagicMock()
        mock_using = MagicMock()
        with patch.multiple(
            self.instance, wait_for_angular=DEFAULT,
            _execute_client_script=DEFAULT
        ) as mock_methods:
            result = self.instance.find_elements_by_binding(mock_descriptor,
                                                            mock_using)
        mock_methods['wait_for_angular'].assert_called_once()
        mock_methods['_execute_client_script'].assert_called_once_with(
            'findBindings', mock_descriptor, False, mock_using, async=False
        )
        self.assertIs(result,
                      mock_methods['_execute_client_script'].return_value)

    def test_find_element_by_binding_no_element(self):
        mock_descriptor = MagicMock()
        mock_using = MagicMock()
        with patch.object(
            self.instance, 'find_elements_by_binding'
        ) as mock_find_elements_by_binding:
            mock_find_elements_by_binding.return_value = []
            with self.assertRaises(NoSuchElementException):
                self.instance.find_element_by_binding(mock_descriptor,
                                                      mock_using)
        mock_find_elements_by_binding.assert_called_once_with(
            mock_descriptor, using=mock_using
        )

    def test_find_element_by_binding_with_element(self):
        mock_descriptor = MagicMock()
        mock_using = MagicMock()
        mock_element = MagicMock()
        with patch.object(
            self.instance, 'find_elements_by_binding'
        ) as mock_find_elements_by_binding:
            mock_find_elements_by_binding.return_value = [mock_element]
            result = self.instance.find_element_by_binding(mock_descriptor,
                                                           mock_using)
        mock_find_elements_by_binding.assert_called_once_with(
            mock_descriptor, using=mock_using
        )
        self.assertIs(result, mock_element)

    def test_get_with_angular(self):
        mock_url = MagicMock()
        with patch(
            '__builtin__.super'
        ) as mock_super, patch(
            'pytractor.mixins.WebDriverWait'
        ) as mock_webdriverwait_class, patch.multiple(
            self.instance, _test_for_angular=DEFAULT, execute_script=DEFAULT,
            create=True  # needed for execute_script
        ) as mock_methods:
            mock_test_for_angular = mock_methods['_test_for_angular']
            # return a truthy value to indicate that angular was found
            mock_test_for_angular.return_value = (True,)
            mock_execute_script = mock_methods['execute_script']

            self.instance.get(mock_url)
        mock_super.assert_called_once_with(WebDriverMixin, self.instance)
        mock_super.return_value.get.assert_called_once_with('about:blank')
        self.assertEqual(len(mock_execute_script.mock_calls), 2)
        mock_webdriverwait_class.assert_called_once_with(self.instance,
                                                         10)
        mock_webdriverwait_instance = mock_webdriverwait_class.return_value
        mock_webdriverwait_instance.until_not.assert_called_once_with(
            self.instance._location_equals, 'about:blank'
        )
        mock_test_for_angular.assert_called_once_with()

    def test_get_without_angular(self):
        mock_url = MagicMock()
        with patch(
            '__builtin__.super'
        ) as mock_super, patch(
            'pytractor.mixins.WebDriverWait'
        ) as mock_webdriverwait_class, patch.multiple(
            self.instance, _test_for_angular=DEFAULT, execute_script=DEFAULT,
            create=True  # needed for execute_script
        ) as mock_methods:
            mock_test_for_angular = mock_methods['_test_for_angular']
            # return a falsy value to indicate that angular was not found
            mock_test_for_angular.return_value = (False, 'ERROR')
            mock_execute_script = mock_methods['execute_script']

            with self.assertRaises(AngularNotFoundException):
                self.instance.get(mock_url)
        mock_super.assert_called_once_with(WebDriverMixin, self.instance)
        mock_super.return_value.get.assert_called_once_with('about:blank')
        self.assertEqual(len(mock_execute_script.mock_calls), 1)
        mock_webdriverwait_class.assert_called_once_with(self.instance,
                                                         10)
        mock_webdriverwait_instance = mock_webdriverwait_class.return_value
        mock_webdriverwait_instance.until_not.assert_called_once_with(
            self.instance._location_equals, 'about:blank'
        )
        mock_test_for_angular.assert_called_once_with()

    def test_get_does_not_test_for_angular_if_ignore_synchronization_is_true(
        self
    ):
        """Verify that get() does not call _test_for_angular if
        ignore_synchronization is set to True."""
        mock_url = MagicMock()
        with patch(
            '__builtin__.super'
        ) as mock_super, patch(
            'pytractor.mixins.WebDriverWait'
        ) as mock_webdriverwait_class, patch.multiple(
            self.instance, _test_for_angular=DEFAULT, execute_script=DEFAULT,
            create=True  # needed for execute_script
        ) as mock_methods:
            mock_test_for_angular = mock_methods['_test_for_angular']

            self.instance.ignore_synchronization = True
            self.instance.get(mock_url)

        self.assertEqual(mock_test_for_angular.call_count, 0)

    def test_refresh(self):
        with patch.multiple(
            self.instance, get=DEFAULT, execute_script=DEFAULT,
            create=True  # needed for execute_script()
        ) as mock_methods:
            self.instance.refresh()
        mock_execute_script, mock_get = (mock_methods['execute_script'],
                                         mock_methods['get'])
        mock_execute_script.assert_called_once()
        mock_get.assert_called_once_with(mock_execute_script.return_value)

    def test_find_element_by_exact_binding_calls_find_elements(self):
        mock_descriptor = MagicMock()
        mock_using = MagicMock()
        mock_element = MagicMock()
        with patch.object(
            self.instance, 'find_elements_by_exact_binding',
            return_value=[mock_element]
        ) as mock_find_elements_by_exact_binding:
            result = self.instance.find_element_by_exact_binding(
                mock_descriptor, mock_using
            )
        mock_find_elements_by_exact_binding.assert_called_once_with(
            mock_descriptor, using=mock_using
        )
        self.assertIs(result, mock_element)

    def test_find_element_by_exact_binding_raises_error_if_nothing_found(self):
        mock_descriptor = MagicMock()
        mock_using = MagicMock()
        with patch.object(
            self.instance, 'find_elements_by_exact_binding', return_value=[]
        ) as mock_find_elements_by_exact_binding:
            with self.assertRaises(NoSuchElementException):
                self.instance.find_element_by_exact_binding(
                    mock_descriptor, mock_using
                )
        mock_find_elements_by_exact_binding.assert_called_once_with(
            mock_descriptor, using=mock_using
        )

    def test_find_elements_by_exact_binding_calls_protractor_script(self):
        mock_descriptor = MagicMock()
        mock_using = MagicMock()

        with patch.multiple(
            self.instance, wait_for_angular=DEFAULT,
            _execute_client_script=DEFAULT
        ) as mock_methods:
            result = self.instance.find_elements_by_exact_binding(
                mock_descriptor, mock_using
            )

        mock_methods['wait_for_angular'].assert_called_once()
        mock_methods['_execute_client_script'].assert_called_once_with(
            'findBindings', mock_descriptor, True, mock_using, async=False
        )
        self.assertIs(result,
                      mock_methods['_execute_client_script'].return_value)

    def test_find_element_by_model_calls_find_elements(self):
        mock_descriptor = MagicMock()
        mock_using = MagicMock()
        with patch.object(
            self.instance, 'find_elements_by_model', return_value=[]
        ) as mock_find_elements_by_model:
            with self.assertRaises(NoSuchElementException):
                self.instance.find_element_by_model(
                    mock_descriptor, mock_using
                )
        mock_find_elements_by_model.assert_called_once_with(
            mock_descriptor, using=mock_using
        )

    def test_find_element_by_model_raises_error_if_nothing_found(self):
        mock_descriptor = MagicMock()
        mock_using = MagicMock()
        with patch.object(
            self.instance, 'find_elements_by_model', return_value=[]
        ) as mock_find_elements_by_model:
            with self.assertRaises(NoSuchElementException):
                self.instance.find_element_by_model(
                    mock_descriptor, mock_using
                )
        mock_find_elements_by_model.assert_called_once_with(
            mock_descriptor, using=mock_using
        )

    def test_find_elements_by_model_calls_protractor_script(self):
        mock_descriptor = MagicMock()
        mock_using = MagicMock()

        with patch.multiple(
            self.instance, wait_for_angular=DEFAULT,
            _execute_client_script=DEFAULT
        ) as mock_methods:
            result = self.instance.find_elements_by_model(
                mock_descriptor, mock_using
            )

        mock_methods['wait_for_angular'].assert_called_once()
        mock_methods['_execute_client_script'].assert_called_once_with(
            'findByModel', mock_descriptor, mock_using, async=False
        )
        self.assertIs(result,
                      mock_methods['_execute_client_script'].return_value)

    def test_location_abs_url_calls_protractor_script(self):
        with patch.multiple(
            self.instance, wait_for_angular=DEFAULT,
            _execute_client_script=DEFAULT
        ) as mock_methods:
            result = self.instance.location_abs_url

        mock_methods['wait_for_angular'].assert_called_once()
        mock_methods['_execute_client_script'].assert_called_once_with(
            'getLocationAbsUrl', self.instance._root_element, async=False
        )
        self.assertIs(result,
                      mock_methods['_execute_client_script'].return_value)

    def test_set_location_calls_protractor_script(self):
        url = 'http://a.new.locat.ion/'
        with patch.multiple(
            self.instance, wait_for_angular=DEFAULT,
            _execute_client_script=DEFAULT
        ) as mock_methods:
            result = self.instance.set_location(url)

        mock_methods['wait_for_angular'].assert_called_once()
        mock_methods['_execute_client_script'].assert_called_once_with(
            'setLocation', self.instance._root_element, url, async=False
        )
        self.assertIs(result,
                      mock_methods['_execute_client_script'].return_value)
