import logging
import os
import wget
import glob

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def download_nrgams_file(temp_directory, language, letter):
    """ Download ngrams data from http://storage.googleapis.com/books/ngrams/books/datasetsv2.html

    Parameters
    ----------
    temp_directory: str
        Path of temporary directory
    language: str
       Which of the following languages to process 'ita', 'eng-gb', 'eng-us', 'spa', 'fre', 'ger'
    letter: str
        Letter which needs to be processed

    Returns
    -------
    ngrams_fpath: str
        Path of nrgams file which needs to be processed


    """
    ngrams_url = "http://storage.googleapis.com/books/ngrams/books/googlebooks-{}-all-1gram-20120701-{}.gz".format(
        language, letter)
    ngrams_fpath = "{}/googlebooks-{}-all-1gram-20120701-{}.gz".format(temp_directory, language, letter)

    if not os.path.exists(ngrams_fpath):
        logger.info("Downloading {}".format(ngrams_fpath))
        wget.download(ngrams_url, ngrams_fpath)

    return ngrams_fpath


def delete_ngrams_files(temp_directory):
    """

    Parameters
    ----------
    temp_directory: str
        Path of temporary directory

    Returns
    -------

    """
    files = glob.glob("{}/*".format(temp_directory))
    for file_ in files:
        logger.info("Deleting {}".format(file_))
        os.remove(file_)


def rescale(values, old_min, old_max, new_min, new_max):
    """Rescale a set of values into a new min and max

    """
    output = []

    for v in values:
        new_v = (new_max - new_min) * (v - old_min) / (old_max - old_min) + new_min
        output.append(new_v)

    return output
