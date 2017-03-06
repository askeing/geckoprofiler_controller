import unittest

from test.mock_addon import MockAddon
from geckoprofiler_controller.control_client import *
from geckoprofiler_controller.control_server import *


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

        # create Mock Add-on
        self.mockaddon = MockAddon()

        # Starting server ...
        self.my_server = ServerController()
        self.my_server.start_server()
        time.sleep(5)

        # start Mock Add-on
        self.mockaddon.start_addon()

        # create Python client
        self.my_client = ControllerClient(self.my_server, save_path=self.CURRENT_PATH)
        # Python client connect to server
        self.my_client.connect()

    def test_client(self):
        # Opening profiling page ...
        self.my_client.open_profiling_page()
        # Getting profiling file ...
        filepath = self.my_client.get_profiling_file()
        self.assertEqual(filepath, os.path.join(self.CURRENT_PATH, 'FirefoxProfile.json.gz'))

        # Opening profiling page ...
        self.my_client.open_profiling_page()
        # Getting profiling link ...
        link = self.my_client.get_profiling_link()
        self.assertEqual(link, 'https://perfht.ml/2lQhjU8')

    def tearDown(self):
        # stop Mock Add-on
        self.mockaddon.stop_addon()

        # Close server and disconnect
        self.my_client.disconnect()
        time.sleep(5)


if __name__ == '__main__':
    unittest.main()
