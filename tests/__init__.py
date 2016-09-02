import os
import sys


def setup_module():
    plugins_directory = os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))))

    sys.path.insert(0, plugins_directory)