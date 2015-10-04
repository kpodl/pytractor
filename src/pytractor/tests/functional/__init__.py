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

import logging
import os
import os.path
import signal
import SimpleHTTPServer
import SocketServer
import time

from .testserver import SimpleWebServerProcess

WEBSERVER_PROCESS = None


def setup_package():
    global WEBSERVER_PROCESS  # pylint: disable=global-statement
    WEBSERVER_PROCESS = SimpleWebServerProcess()
    WEBSERVER_PROCESS.run()


def teardown_package():
    WEBSERVER_PROCESS.stop()
