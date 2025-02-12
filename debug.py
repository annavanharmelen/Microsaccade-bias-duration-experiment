"""
This script is used to test random aspects of
the 'microsaccade bias duration' experiment.
To run the experiment, see main.py.

made by Anna van Harmelen, 2025
"""
from set_up import get_monitor_and_dir, get_settings
from practice import practice

monitor, directory = get_monitor_and_dir(True)

settings = get_settings(monitor, directory)
practice(None, settings)
