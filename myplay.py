#!/usr/bin/env python
#

# import system modules
#
import random
import os
import sys
import time
from pathlib import Path
import pprint

# define global variables
#
FHIST = "_HISTORY.txt"
FEXT = ".mp3"
ERR = int(1)

# set the filename using basename
#
__FILE__ = os.path.basename(__file__)

# function: check_dir
#
# arguments:
#   path: directory path given as command line argument
#
# This method checks if directory path exists and prints error message if not
#
def check_dir(path):

    if os.path.isdir(path) == False:
        print("Error: %s: directory does not exist (%s)" % (__FILE__, path))
        return False
    else:
        return True
    
# function: load_mp3s
#
# arguments:
#   path: directory path given as command line argument
#   ext: file extension
#
# This method loads all mp3 files into the mp3s dictionary
#
def load_mp3s(path, ext):

    # initialize a dictionary
    #
    mp3s = {}
    
    # walks through directory tree to get full path
    #
    for root, dirs, files in os.walk(path):
        for file in files:

            # if the filename contains .mp3, add it to mp3s dictionary
            #
            if file.endswith(ext):
                fname = root + "/" + file
                abs_path = os.path.abspath(fname)
                mp3s[abs_path] = int(0)

    # check the size of the dictionary
    #
    if len(mp3s) == int(0):
        print("Error: %s: no mp3s to play (%s, %s)" % (__FILE__, path, ext))
        sys.exit(ERR)

    # exit gracefully
    #
    return mp3s

# function: load_history
#
# argumemts:
#   path: directory path given as command line argument
#   fhist: history text file
#
# This method loads the history text file 
def load_history(path, fhist):
    
    # intialize history dictionary
    #
    hist = {}
    
    # create the full filename
    #
    ffname = Path(path + "/" + fhist)

    # check if it exists
    #
    if os.path.exists(ffname) is True:

        # open history file and read it line by line
        #
        with open(ffname) as f:
            for line in f:
                (song, count) = line.split()
                hist[song] = int(count)
        
    # exit gracefully
    #
    return hist

# function: clean_history
#
# arguments:
#   hist: history dictionary
#   mp3s: mp3s dictionary
#
# This method merges two dictionaries and deletes keys that are in hist but not
# in mp3s
#
def clean_history(hist, mp3s):
    
    # copy all contents of mp3s into mhist
    #
    
    mhist = hist
    for mp3 in mp3s:
        if mp3 not in mhist:
            mhist[mp3] = int(0)

    
    # if a song is in hist but not mp3s, then delete the song from hist
    #
    for song in mhist:
        if song not in mp3s:
            del(song)

    # exit gracefully
    #
    return mhist
# function: write_history
#
# arguments:
#   path: directory path as command line argument
#   bname: history text file
#   hist: history dictionary
#
# This method writes all mp3s files in directory to history with a count. If 
# the history file does not exist, it is created.
#
def write_history(path, bname, hist):

    # create the full pathname
    #
    ffname = Path(path + "/" + bname)
    with open(ffname, 'w') as f:
        for song, count in hist.items():
            f.write('%s %d\n' % (song, count))

    # exit gracefully
    #
    return True

# function: main                                                              
#
def main(argv):
    
    # check if directory exists and print error message if not
    #
    if check_dir(argv[1]) is False:
        sys.exit(ERR)

    # load the songs to play into a dictionary
    #
    mp3s = load_mp3s(argv[1], FEXT)
    
    # load the history
    #
    hist = load_history(argv[1], FHIST)
    
    # merge mp3s and history dictionaries into only history dictionary
    #
    mhist = clean_history(hist, mp3s)
    
    # neatly print out merged dictionary
    #
    pprint.pprint(mhist)
    print("\n ----------------------------------------------- \n")

    # randomly shuffle the songs
    #
    l = list(mhist.keys())
    random.shuffle(l)
    
    # iterate over the list
    #
    while True:
        for song in l:
            
            # write history
            #
            mhist[song] += 1
            write_history(argv[1], FHIST, mhist)
            
            # print the name of the song to be played
            #
            print("playing...", song)
            
            # play the song
            #
            time.sleep(3)
        
# begin gracefully                                                 
#
if __name__ == '__main__':
    main(sys.argv[0:])
#                                                                              
# end of file           








