#  ngramsNVI
Code to be able reproduce the National Valence Indices created using Google Ngrams data (http://storage.googleapis.com/books/ngrams/books/datasetsv2.html) and the affective word norms (ANEW) for one of the following languages: Italian (ita), EnglishGB (eng-gb) English US (eng-us), Spanish (spa), French (fre), or German( ger)
 
 For more info on this method read:
 Hills, T.T., Proto, E., Sgroi, D. et al. Historical analysis of national subjective wellbeing using millions of
    digitized books. Nat Hum Behav 3, 1271–1275 (2019) doi:10.1038/s41562-019-0750-z 


**Installation instructions**

* git clone https://github.com/alan-turing-institute/ngramsNVI.git
* cd ngramsNVI
* sudo pip install -r requirements.txt
* pip install -e ./

**How to create a National Valence Index**
* cd ngramsNVI
* python create_NVI.py -l "ger" -d
    * -l --language {ita,eng-gb,eng-us,spa,fre,ger} The language to process
    * -d --delete_files Whether to delete downloaded ngrams files after processing



