import os

from ngramsNVI.create_NVI import load_valence_data, match_ngram_counts_with_valence_scores
from ngramsNVI.utils import download_nrgams_file
from ngramsNVI.constants import PACKAGE_LOCATION


def test_ngrams_valence_processing():
    """Test whether ngrams data is successfully loading and merging with the ANEW data

    """
    language = "ita"
    letter = "z"

    valence_data = load_valence_data(language)

    temp_directory = "{}/googlebooksdata".format(PACKAGE_LOCATION)
    os.makedirs(temp_directory, exist_ok=True)

    ngrams_fpath = download_nrgams_file(temp_directory, language, letter)

    ngrams_valence_scores = match_ngram_counts_with_valence_scores(valence_data, ngrams_fpath)

    zucchero_data = ngrams_valence_scores[
        (ngrams_valence_scores['ngram'] == "zucchero") & (ngrams_valence_scores['year'] == 2009)]

    os.remove(ngrams_fpath)

    assert float(zucchero_data['valence']) == 6.55
