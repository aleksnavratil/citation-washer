##Google Scholar Citation Washer
##Columbia University
##Energy and Tribology Lab
##Department of Mechanical Engineering
##By Aleks Navratil
##1 December 2013
##If you have dirty citations in your bibliography, eg. with bad capitalization, weird parenthesis, etc,
##you can use this program to automatically wash all replace all your citations with the bibtex info from
##google scholar.
##
##Limitations:
##    0)Note that the gscholar.py readme and documentation on github are wrong as of 1 Dec 2013.
##        You have to feed 2 arguments to gscholar.py, instead of 1 argument as they suggest.
##        See here for more details:
##        http://stackoverflow.com/questions/13200709/extract-google-scholar-results-using-python-or-r
##    1) If you have too many citations (>50 ish) and don't delay your queries, you might get banned by
##       google's servers because they
##       think you're a bot. You stay banned for ~24 hours. Rate limit yourself to avoid this.
##    2) This program just grabs the title from your bibtex file and searches for it on google scholar.
##        It then returns the first hit for that title and replaces your bibtex with it. This method
##        will probably fail badly if you have malformed titles.
##    3) It is querying, scraping, and parsing google scholar http results, because there is no
##        scholar API yet. If they later invent that, you should quit using this and rewrite a similar
##        solution to take advantage of the API.
##    4) The documentation for the gscholar.py file is wrong. You have to give it two arguments, not one.
##        The second argument is "outformat=4", in which 4 stands for bibtex formatted replies.

import os
import re
import sys
import traceback
import random
from time import sleep ##We need to slow down on purpose so as
## to fool google into thinking that we're a human, not a program.
##Without this, our account will get banned after ~50 queries.
##Generally you will stay banned for 24 hours.
import gscholar ##This is the query/scraper library that gets bibtex info from google scholar
from pybtex.database.input import bibtex ##This is a parser that lets us read bibtex files

def acquire_target_bibliography():
    target_bibliography_path = "/home/aleks/Desktop/Bibliographies/gscholar-master/gscholar/test.bib"
    return target_bibliography_path

def define_output_bibliography():
    output_bibliography_path = acquire_target_bibliography()[0:-4]+"_washed.bib"
    return output_bibliography_path

def open_bibtex_file():
    parser = bibtex.Parser()
    bib_data = parser.parse_file(acquire_target_bibliography())
    return bib_data

def get_original_unique_ids():
    bib_data = open_bibtex_file()
    uniqe_ids_for_bibtex = list()
    for key in bib_data.entries.keys():
        uniqe_ids_for_bibtex.append(key)
    return uniqe_ids_for_bibtex

def get_list_of_titles_to_feed_google():
    bib_data = open_bibtex_file()
    list_of_titles_to_feed_google = list()
    for key in bib_data.entries.keys():
        list_of_titles_to_feed_google.append(bib_data.entries[key].fields['title'])
    return list_of_titles_to_feed_google

def countdown_timer(lowerlim, upperlim):
    for remaining in range(random.randrange(lowerlim, upperlim), 0, -1):
        sys.stdout.write("\r")
        print "Waiting a few seconds to trick Google."
        sys.stdout.write("{:2d} seconds remaining.\n".format(remaining)) 
        sys.stdout.flush()
        sleep(1)
    sys.stdout.write("\r            \n\n")

def ask_google_for_clean_citations():
    washed_bibdata_from_google=list()
    counter = 0
    for dirty_title in get_list_of_titles_to_feed_google():
        try:
            print dirty_title
            counter += 1
            ##Note that the readme and documentation on github are wrong as
            ##of 1 Dec 2013. You have to feed 2 arguments to gscholar.py,
            ##instead of 1 argument as they suggest. See here for more
            ##details: http://stackoverflow.com/questions/13200709/extract-google-scholar-results-using-python-or-r
            washed_bibdata_from_google.append(gscholar.query(dirty_title,outformat=4))
        except Exception:
            print "\nYou have hit Google scholar with too many queries and they banned you. The program will now wait a few hours and try again."
            print "The relevant error message is \n"
            print traceback.format_exc()
            countdown_timer(9999,10000)
            pass
        if counter > 25:
            if not dirty_title == get_list_of_titles_to_feed_google()[-1]:
                countdown_timer(207,503)##you can turn this off if you only have a few citations (approx. 50 or fewer).
    ##        Otherwise you have to rate limit yourself to avoid a ban.
    return washed_bibdata_from_google

def reintegrate_original_unique_ids(): ##A "unique ID" is just the thing you put in the \cite command in latex.
    ##Ie. to cite Elon, you write \cite{Terrell2006}. So "Terrell2006" is the unique ID.
    bibdata = ask_google_for_clean_citations()
    unique_ids_for_bibtex = get_original_unique_ids()
    for i, citation in enumerate(bibdata):
        re.sub('({)(.*)(,)', unique_ids_for_bibtex[i],citation[0])
    return bibdata

def write_washed_bibliography():
    washed_bib_file = open(define_output_bibliography(),'w')
    for citation in reintegrate_original_unique_ids():
        washed_bib_file.writelines(citation)
        washed_bib_file.write(",\n")
    washed_bib_file.close()

if __name__ == "__main__":
    print "Now washing citations from file"
    print acquire_target_bibliography()
    print "The washed bibliography will be stored in"
    print define_output_bibliography()
    write_washed_bibliography()
    print "Successfully washed your bibliography. The washed .bib file is stored in "
    print define_output_bibliography()

#The core of this program is just this:
#gscholar.query("Elon Terrell",outformat=4)
##which returns the google scholar bibtex for elon's paper.
##you can also search by title.
