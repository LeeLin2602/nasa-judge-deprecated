import os
import logging

# Setup basic logging
logging.basicConfig(level=logging.DEBUG, filename='application.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')

def create_directory(path):
    try:
        os.makedirs(path, exist_ok=True)
        logging.info(f"Successfully created/accessed the directory {path}")
    except Exception as e:
        logging.error(f"Failed to create the directory {path}: {e}")