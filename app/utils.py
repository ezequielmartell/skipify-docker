import json
import logging

SKELETON_FILE = 'app/skeleton.json'

logger = logging.getLogger(__name__)

def load_data(file):
    try:
        with open(file) as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warn(f"data file not found, creating {file}")
        with open(file, 'w') as data_file:
            with open(SKELETON_FILE, 'r') as skeleton_file:
                data = json.load(skeleton_file)
                json.dump(data, data_file, indent=4)
        logger.info(f"created {file} from {SKELETON_FILE}")
        return load_data(file)

def save_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)