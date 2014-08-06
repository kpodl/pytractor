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

logger = logging.getLogger(__name__)


class SimpleWebServerProcess(object):
    """
    A simple webserver for serving pages for testing.
    """
    HOST = 'localhost'
    PORT = 9999
    RUN_DIR = 'angular-app'
    _pid = None

    def run(self):
        self._pid = os.fork()
        if self._pid == 0:
            self.start_server()
        else:
            logger.debug('Started webserver child as pid {} on'
                         ' port {}'.format(self._pid, self.PORT))
            # wait 5 seconds for server to start
            time.sleep(5)

    def start_server(self):
        module_path = __file__
        server_path = os.path.join(os.path.dirname(module_path), self.RUN_DIR)
        logger.debug('Starting webserver for path {} on'
                     ' port {}'.format(server_path, self.PORT))
        os.chdir(server_path)
        handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        httpd = SocketServer.TCPServer((self.HOST, self.PORT), handler)
        httpd.serve_forever()

    def stop(self):
        if self._pid != 0:
            logger.debug('Sending SIGTERM to webserver child with'
                         ' pid {}'.format(self._pid))
            os.kill(self._pid, signal.SIGTERM)
            os.waitpid(self._pid, 0)

webserver_process = None


def setup_package():
    global webserver_process
    webserver_process = SimpleWebServerProcess()
    webserver_process.run()


def teardown_package():
    webserver_process.stop()
