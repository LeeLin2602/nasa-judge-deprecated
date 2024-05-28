import os
import logging

# Setup basic logging
logging.basicConfig(level=logging.DEBUG, filename='application.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')

def create_directory(path):
    try:
        os.makedirs(path, exist_ok=True)
        logging.info("Successfully created/accessed the directory %s", path)
    except OSError as e:
        logging.error("Failed to create the directory %s: %s", path, e)
