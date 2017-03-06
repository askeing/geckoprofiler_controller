from geckoprofiler_controller.control_client import *
from geckoprofiler_controller.control_server import *

logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    try:
        CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

        # Starting server ...
        my_server = ServerController()
        my_server.start_server()

        time.sleep(5)

        # Starting client ...
        my_client = ControllerClient(my_server, save_path=CURRENT_PATH)
        my_client.connect()

        # Opening profiling page ...
        my_client.open_profiling_page()
        my_client.open_profiling_page()

        # Getting profiling file ...
        filepath = my_client.get_profiling_file()

        # Getting profiling link ...
        link = my_client.get_profiling_link()

        # Close server and disconnect
        my_client.disconnect()

        print('file path: ' + filepath)
        print('link: ' + link)

    finally:
        print('stop server.')
        my_client.stop_server()
