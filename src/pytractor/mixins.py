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
Mixin to add the capability of testing angular.js apps with selenium
webdrivers.
"""

from functools import wraps
from math import floor
from urlparse import urljoin

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.command import Command
from selenium.webdriver.support.wait import WebDriverWait

from pkg_resources import resource_string

from .exceptions import AngularNotFoundException

CLIENT_SCRIPTS_DIR = 'protractor/extracted'
DEFER_LABEL = 'NG_DEFER_BOOTSTRAP!'
# These are commands that need synchronization with the angular app.
COMMANDS_NEEDING_WAIT = [
    Command.CLICK_ELEMENT,
    Command.SEND_KEYS_TO_ELEMENT,
    Command.GET_ELEMENT_TAG_NAME,
    Command.GET_ELEMENT_VALUE_OF_CSS_PROPERTY,
    Command.GET_ELEMENT_ATTRIBUTE,
    Command.GET_ELEMENT_TEXT,
    Command.GET_ELEMENT_SIZE,
    Command.GET_ELEMENT_LOCATION,
    Command.IS_ELEMENT_ENABLED,
    Command.IS_ELEMENT_SELECTED,
    Command.IS_ELEMENT_DISPLAYED,
    Command.SUBMIT_ELEMENT,
    Command.CLEAR_ELEMENT
]


def angular_wait_required(wrapped):
    @wraps(wrapped)
    def wait_for_angular(driver, *args, **kwargs):
        driver.wait_for_angular()
        return wrapped(driver, *args, **kwargs)
    return wait_for_angular


class WebDriverMixin(object):
    """A mixin for Selenium Webdrivers."""
    ignore_synchronization = False
    """If True, pytractor will not attempt to synchronize with the page before
    performing actions. This can be harmful because pytractor will not wait
    until $timeouts and $http calls have been processed, which can cause
    tests to become flaky. This should be used only when necessary, such as
    when a page continuously polls an API using $timeout.
    """  # docstring adapted from protractor.js
    _root_element = None
    _base_url = None

    def __init__(self, base_url, root_element, script_timeout=10,
                 test_timeout=10, *args, **kwargs):
        self._base_url = base_url
        self._root_element = root_element
        self._test_timeout = test_timeout
        super(WebDriverMixin, self).__init__(*args, **kwargs)
        self.set_script_timeout(script_timeout)

    def _execute_client_script(self, script_name, *args, **kwargs):
        async = kwargs.pop('async', True)
        file_name = '{}.js'.format(script_name)
        js_script = resource_string(__name__,
                                    '{}/{}'.format(CLIENT_SCRIPTS_DIR,
                                                   file_name))
        if async:
            result = self.execute_async_script(js_script, *args)
        else:
            result = self.execute_script(js_script, *args)
        return result

    def wait_for_angular(self):
        if self.ignore_synchronization:
            return
        else:
            return self._execute_client_script('waitForAngular',
                                               self._root_element)

    def execute(self, driver_command, params=None):
        # We also get called from WebElement methods/properties.
        if driver_command in COMMANDS_NEEDING_WAIT:
            self.wait_for_angular()
        return super(WebDriverMixin, self).execute(driver_command,
                                                   params=params)

    def _test_for_angular(self):
        return self._execute_client_script('testForAngular',
                                           floor(self._test_timeout / 1000))

    def _location_equals(self, location):
        result = self.execute_script('return window.location.href')
        return result == location

    @property
    @angular_wait_required
    def current_url(self):
        return super(WebDriverMixin, self).current_url

    @property
    @angular_wait_required
    def page_source(self):
        return super(WebDriverMixin, self).page_source

    @property
    @angular_wait_required
    def title(self):
        return super(WebDriverMixin, self).title

    @property
    @angular_wait_required
    def location_abs_url(self):
        return self._execute_client_script('getLocationAbsUrl',
                                           self._root_element, async=False)

    @angular_wait_required
    def find_element(self, *args, **kwargs):
        return super(WebDriverMixin, self).find_element(*args, **kwargs)

    @angular_wait_required
    def find_elements(self, *args, **kwargs):
        return super(WebDriverMixin, self).find_elements(*args, **kwargs)

    @angular_wait_required
    def find_elements_by_binding(self, descriptor, using=None):
        elements = self._execute_client_script('findBindings', descriptor,
                                               False, using, async=False)
        return elements

    def find_element_by_binding(self, descriptor, using=None):
        elements = self.find_elements_by_binding(descriptor, using=using)
        if len(elements) == 0:
            raise NoSuchElementException(
                "No element found for binding descriptor"
                " '{}'".format(descriptor)
            )
        else:
            return elements[0]

    def find_element_by_exact_binding(self, descriptor, using=None):
        elements = self.find_elements_by_exact_binding(descriptor, using=using)
        if len(elements) == 0:
            raise NoSuchElementException(
                "No element found for binding descriptor"
                " '{}'".format(descriptor)
            )
        else:
            return elements[0]

    def find_elements_by_exact_binding(self, descriptor, using=None):
        elements = self._execute_client_script('findBindings', descriptor,
                                               True, using, async=False)
        return elements

    def find_element_by_model(self, descriptor, using=None):
        elements = self.find_elements_by_model(descriptor, using=using)
        if len(elements) == 0:
            raise NoSuchElementException(
                "No element found for model descriptor"
                " {}".format(descriptor)
            )
        else:
            return elements[0]

    def find_elements_by_model(self, descriptor, using=None):
        elements = self._execute_client_script('findByModel', descriptor,
                                               using, async=False)
        return elements

    def get(self, url):
        super(WebDriverMixin, self).get('about:blank')
        full_url = urljoin(self._base_url, url)
        self.execute_script(
            """
            window.name = "{}" + window.name;
            window.location.replace("{}");
            """.format(DEFER_LABEL, full_url)
        )
        wait = WebDriverWait(self, 10)
        wait.until_not(self._location_equals, 'about:blank')

        if not self.ignore_synchronization:
            test_result = self._test_for_angular()
            angular_on_page = test_result[0]
            if not angular_on_page:
                message = test_result[1]
                raise AngularNotFoundException(
                    'Angular could not be found on page: {}:'
                    ' {}'.format(full_url, message)
                )
            # TODO: inject scripts here
            # return self.execute_script(
            #     'angular.resumeBootstrap(arguments[0]);'
            # )
            self.execute_script('angular.resumeBootstrap();')

    def refresh(self):
        url = self.execute_script('return window.location.href')
        self.get(url)

    def set_location(self, url):
        result = self._execute_client_script('setLocation', self._root_element,
                                             url, async=False)
        return result
