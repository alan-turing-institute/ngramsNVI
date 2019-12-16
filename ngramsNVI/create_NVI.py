import argparse
import logging
import os
import string

import pandas as pd

from ngramsNVI.constants import PACKAGE_LOCATION
from ngramsNVI.utils import rescale, download_nrgams_file, delete_ngrams_files

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_valence_data(language):
    """ Load valence data from the largest available sets of affective word norms for four languages.

    See Hills, T.T., Proto, E., Sgroi, D. et al. Historical analysis of national subjective wellbeing using millions of
    digitized books. Nat Hum Behav 3, 1271–1275 (2019) doi:10.1038/s41562-019-0750-z for more information on how this
    valence data has been gathered.

    For german, we correct the values so that it is in the same range as the other languages.

    Parameters
    ----------
    language: str
        Load valence data for one of the following languages 'ita', 'eng-gb', 'eng-us', 'spa', 'fre', 'ger'

    Returns
    -------
    valence_data: pd.dataframe
        Dataframe with index of words and their associated valence score

    """

    if language in ["eng-gb", "eng-us"]:
        language = "eng"

    valence_data = pd.read_csv("{}/data/ANEW/{}_valence.csv".format(PACKAGE_LOCATION, language), na_filter=False)

    if language == "ger":
        valence_data.rename(columns={'valence': 'valence_old'}, inplace=True)
        valence_data["valence"] = rescale(valence_data["valence_old"].values, -3, 3, 1, 9)

    return valence_data


def match_ngram_counts_with_valence_scores(valence_data, ngrams_fpath):
    """

    Parameters
    ----------
    ngrams_fpath

    Returns
    -------

    """
    ngrams_data = pd.read_table(ngrams_fpath, compression='gzip',
                                names=["ngram", "year", "match_count", "volume_count"])
    ngrams_data["ngram"] = ngrams_data["ngram"].str.lower()

    ANEW_words = [k for k in valence_data.word]
    ngrams_ANEW_words_data = ngrams_data[ngrams_data.ngram.isin(ANEW_words)]

    if len(ngrams_ANEW_words_data) > 0:
        ngrams_ANEW_words_by_year = ngrams_ANEW_words_data.groupby(['ngram', 'year']).sum()

        ngrams_valence_scores = pd.merge(ngrams_ANEW_words_by_year.reset_index(), valence_data, how='left',
                                         left_on=['ngram'], right_on=['word'])
        return ngrams_valence_scores


def add_valence_to_nrgams_data(temp_directory, language, valence_data, delete_files):
    """

    Parameters
    ----------
    temp_directory
    language
    valence_data
    delete_files

    Returns
    -------

    """
    letters = string.ascii_lowercase

    ngrams_valence_scores_all_letters = []

    for letter in letters:
        logger.info("Downloading data for {} {}".format(language, letter))

        ngrams_fpath = download_nrgams_file(temp_directory, language, letter)

        ngrams_valence_scores = match_ngram_counts_with_valence_scores(valence_data, ngrams_fpath)

        ngrams_valence_scores_all_letters.append(ngrams_valence_scores)

        if delete_files:
            os.remove(ngrams_fpath)

    ngrams_valence_data = pd.concat(ngrams_valence_scores_all_letters)

    return ngrams_valence_data


def create_NVI(language, valence_data, delete_files=False):
    """

    Parameters
    ----------
    language
    valence_data
    delete_files

    Returns
    -------

    """
    # Set up temporary directory to store large files
    temp_directory = "{}/googlebooksdata".format(PACKAGE_LOCATION)
    os.makedirs(temp_directory, exist_ok=True)

    ngrams_valence_data = add_valence_to_nrgams_data(temp_directory, language, valence_data, delete_files)

    logger.info("Calculating valence scores")

    total_words_per_year = ngrams_valence_data.groupby('year').agg(
        match_totals=("match_count", sum))

    ngrams_valence_data = pd.merge(ngrams_valence_data, total_words_per_year, how='left', on=['year'])
    ngrams_valence_data["val_score"] = ngrams_valence_data["valence"] * (
            ngrams_valence_data["match_count"] / ngrams_valence_data["match_totals"])

    # Saving valence score for all words
    ngrams_valence_data.to_csv("{}/data/{}_valence_ngram_words.csv".format(PACKAGE_LOCATION, language), index=False)

    # Saving NVI for all words
    NVI_data = ngrams_valence_data[["year", "match_count", "val_score"]].groupby(['year']).sum()
    NVI_data.to_csv("{}/data/{}_NVI.csv".format(PACKAGE_LOCATION, language), index=False)

    # Checking for any unprocessed words, as some words will not be found in google ngrams if they are compound words
    unprocessed_words = list(set(valence_data['word']) - set(ngrams_valence_data['ngram']))
    logger.info("These words could not be processed {}".format(unprocessed_words))
    pd.DataFrame(unprocessed_words).to_csv("{}/data/{}_unprocessed_words.csv".format(PACKAGE_LOCATION, language),
                                           index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create a National Valence Index for one of the following languages: Italian (ita), '
                    'EnglishGB (eng-gb), Engligh US (eng-us), Spanich (spa), Frence(fre), or German (ger).')

    parser.add_argument('-l', '--language', choices=['ita', 'eng-gb', 'eng-us', 'spa', 'fre', 'ger'],
                        help='The language to process')
    parser.add_argument("-d", "--delete_files", help="Whether to delete files as they are being processed to save "
                                                     "on disk space", action='store_true')

    args = parser.parse_args()

    valence_data = load_valence_data(language=args.language)

    create_NVI(language=args.language, valence_data=valence_data, delete_files=args.delete_files)
