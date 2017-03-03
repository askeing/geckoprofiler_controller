"""
Control the Gecko-Profiler Add-on by sending commands to Web Socket server.
Step:
1. start Web Socket server by ServerController.start_server()
2. connect()
3. open_profiling_page()
4. get_profiling_file() or get_profiling_link()
5. disconnect()
"""

import os
import json
import logging
from websocket import create_connection

from server import commands

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))


class ControllerClient:

    def __init__(self, control_server, save_path=None):
        self.hostname = 'ws://localhost:8888/py'
        self.control_server = control_server
        self.is_online = False
        self.profile_ready = False
        self.ws_conn = None
        if save_path:
            self.save_path = save_path
        else:
            self.save_path = CURRENT_PATH

    def connect(self):
        logger.info('Connecting Web Socket server {} ...'.format(self.hostname))
        self.ws_conn = create_connection(self.hostname)
        self.is_online = True

    def set_save_path(self, path):
        self.save_path = path

    def open_profiling_page(self):
        logger.info('Opening profiling page ...')
        data = {
            commands.KEY_NAME: commands.VALUE_START,
            commands.KEY_DATA: ''
        }
        self._send_and_recv(data)
        self.profile_ready = True
        return True

    def stop_server(self):
        self.control_server.stop_server()

    def disconnect(self):
        self.stop_server()
        logger.info('Stopping Web Socket server ...')
        data = {
            commands.KEY_NAME: commands.VALUE_STOP,
            commands.KEY_DATA: ''
        }
        self._send(data)
        self.is_online = False
        self.profile_ready = False
        logger.info('Stopped.')

    def get_profiling_file(self):
        logger.info('Getting profiling file ...')
        data = {
            commands.KEY_NAME: commands.VALUE_GET_FILE,
            commands.KEY_DATA: self.save_path
        }
        if self.profile_ready:
            return self._send_and_recv(data)
        else:
            logger.error('Profiling Data is not ready.')

    def get_profiling_link(self):
        logger.info('Getting profiling link ...')
        data = {
            commands.KEY_NAME: commands.VALUE_GET_LINK,
            commands.KEY_DATA: ''
        }
        if self.profile_ready:
            return self._send_and_recv(data)
        else:
            logger.error('Profiling Data is not ready.')

    def _send_and_recv(self, data):
        self._send(data)
        return self._recv()

    def _send(self, data):
        if not self.is_online:
            raise Exception('The client does not connect to server.')
        if isinstance(data, dict):
            message = json.dumps(data)
        else:
            message = data
        logger.debug('Sending {} ...'.format(message))
        self.ws_conn.send(message)
        logger.debug('Sent.')

    def _recv(self):
        if not self.is_online:
            raise Exception('The client does not connect to server.')
        logger.debug('Receiving...')
        result = self.ws_conn.recv()
        logger.debug('Received {}'.format(result))
        try:
            result_dict = json.loads(result)
            message = result_dict.get(commands.KEY_DATA, '')
            return message
        except:
            return result
