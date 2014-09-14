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
This is the web server that serves the angular app that we use for testing.
It is started by setup_package() in __init__.py
"""

import logging
import os
import signal
import SimpleHTTPServer
import SocketServer
import time

PORT = 8000

logger = logging.getLogger(__name__)


class TestServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """
    The handler for the web server. It has the same functionality as the
    server for protractor's test app.
    """
    def send_text_response(self, text):
        self.send_response(200)
        self.send_header("Content-type", 'text/plain')
        self.send_header("Content-Length", len(text))
        self.end_headers()
        return text

    def do_GET(self):
        if self.path == '/fastcall':
            return self.send_text_response('done')
        elif self.path == '/slowcall':
            time.sleep(5)
            return self.send_text_response('finally done')
        elif self.path == '/fastTemplateUrl':
            return self.send_text_response('fast template contents')
        elif self.path == '/slowTemplateUrl':
            time.sleep(5)
            return self.send_text_response('slow template contents')
        else:
            return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)


class SimpleWebServerProcess(object):
    """
    A simple webserver for serving pages for testing.
    """
    HOST = 'localhost'
    PORT = 9999
    APP_DIR = 'testapp'
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
        server_path = os.path.join(os.path.dirname(module_path), self.APP_DIR)
        logger.debug('Starting webserver for path {} on'
                     ' port {}'.format(server_path, self.PORT))
        os.chdir(server_path)
        handler = TestServerHandler
        httpd = SocketServer.TCPServer((self.HOST, self.PORT), handler)
        httpd.serve_forever()

    def stop(self):
        if self._pid != 0:
            logger.debug('Sending SIGTERM to webserver child with'
                         ' pid {}'.format(self._pid))
            os.kill(self._pid, signal.SIGTERM)
            os.waitpid(self._pid, 0)
