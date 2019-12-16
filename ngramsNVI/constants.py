import os

# Various folder locations




PACKAGE_LOCATION = os.path.dirname(os.path.dirname(__file__))
DATA_FOLDER = os.path.join(PACKAGE_LOCATION, 'data')
TEMP_FOLDER = PACKAGE_LOCATION
STORAGE_FOLDER = os.path.join(PACKAGE_LOCATION, 'processed_files')


