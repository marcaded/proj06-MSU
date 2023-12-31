
#################################
## Python project 06


# Uncomment the following lines if you run the optional run_file tests locally
# so the input shows up in the output file. Do not copy these lines into Codio.
#
# import sys
# def input( prompt=None ):
#    if prompt != None:
#        print( prompt, end="" )
#    aaa_str = sys.stdin.readline()
#    aaa_str = aaa_str.rstrip( "\n" )
#    print( aaa_str )
#    return aaa_str



import csv
import string
from operator import itemgetter

def open_file(message):
    '''Tries to open a file using a given string as the filename, and returns either the filepointer or the file, depending on if the file was found or not.
    Re-prompting for file input is handled in the main() function
    
    ARGUMENTS: 
    message: The input string for the filename
    RETURNS:
    None: If the file is not found, this function will return none
    fp: If file is found, function returns a file pointer '''
    try:
        fp = open(message, 'r')
        return fp
    except FileNotFoundError:
        print("\nFile is not found! Try Again!")
        return None

    
    

def read_stopwords(fp):
    ''' DocStrings goes here.'''
    unique = set()
    for line in fp:
        lines = line.lower().strip().split()
        for word in lines:
            if word not in unique:
                unique.add(word)
    fp.close()
    return unique
        

def validate_word(word, stopwords):
    ''' DocStrings goes here.'''
    
## Was Struggling to get punctuation picked up by a single if statement, kept returning True for "all", so I had to swap to any function
## Because I wasn't sure what I was doing wrong
    if any(punctuation in word for punctuation in string.punctuation):
        return False
    elif any(digits in word for digits in string.digits):
        return False
    elif word in stopwords:
        return False
    else:
        return True

        

def process_lyrics(lyrics, stopwords):
    ''' DocStrings goes here.'''
    
    lyrics_list = []  
    valid_set = set()  
    lyric = lyrics.lower().strip().split()
    for word in lyric:
        for punc in string.punctuation:
            if punc in word:
               word =  word.replace(punc, '')
        lyrics_list.append(word)
    for lyric in lyrics_list:
        if validate_word(lyric, stopwords):
            valid_set.add(lyric)
    return valid_set
    
            
        
        


def read_data(fp, stopwords):
    ''' DocStrings goes here.'''
    data_dict = {}
    reader = csv.reader(fp)
    next(reader)
    for row in reader:
        singer = row[0]
        song = row[1]
        lyrics = process_lyrics(row[2], stopwords)
        update_dictionary(data_dict, singer, song, lyrics)
    return data_dict

    

def update_dictionary(data_dict, singer, song, words):
    ''' DocStrings goes here.'''

    intro_dict = {singer:{song:set(words)}}
    for singer in intro_dict:
        if singer not in data_dict:
            data_dict[singer] = {}
    
    for song in intro_dict[singer]:
        if song not in data_dict[singer]:
            data_dict[singer].update({song: set()})
    
    for word in intro_dict[singer][song]:
        if word not in data_dict[singer][song]:
            data_dict[singer][song].add(word)
    return data_dict

        


        

        
def calculate_average_word_count(data_dict):
    ''' DocStrings goes here.'''
    averages_dict_unclean = {}
    clean = {}
    for singers in data_dict:
        averages_dict_unclean[singers] = 0
        song_count = 0
        for song in data_dict[singers]:
            song_count += 1
            lyric_count = 0
            for lyric in data_dict[singers][song]:
                        lyric_count += 1
                        averages_dict_unclean[singers] += song_count
    for singer, l in averages_dict_unclean.items():
        clean[singer] = l/ song_count
    return clean
        

                    




def find_singers_vocab(data_dict):
    ''' DocStrings goes here.'''
    vocab = {}
    for singer in data_dict:
        if singer not in vocab:
            vocab[singer] = set()
            for song in data_dict[singer]:
                for lyric in data_dict[singer][song]:
                    if lyric not in vocab[singer]:
                        vocab[singer].add(lyric)
    return vocab

def display_singers(combined_list):
    ''' DocStrings goes here.'''

    print("\n{:^80s}".format("Singers by Average Word Count (TOP - 10)"))
    print("{:<20s}{:>20s}{:>20s}{:>20s}".format("Singer","Average Word Count", "Vocabulary Size", "Number of Songs"))
    print('-' * 80)
    # This function sorts the list by average word count in descending order. If two tuples have the same average, it
    # sorts them by the vocabulary size, again in descending order. If two tuples have the same average and same
    # vocabulary size, keep the same order as it appears in the combined_list list.
    for i in combined_list:
        print("{:<20s}{:>20s}{:>20s}{:>20s}".format(i[0],i[1],i[2],i[3]))


def search_songs(data_dict, words):
    ''' Comment goes here.''' 
    search_query = []
    for singer in data_dict:
        for song in data_dict[singer]:
            if words.issubset(data_dict[singer][song]):
                q = (singer, song)
                search_query.append(q)
    return search_query

def main():
    while True:
        
        stopwords_filename = input('\nEnter a filename for the stopwords: ')
        
        stopwords_fp = open_file(stopwords_filename)
        
        if stopwords_fp != None:
            break
    stopwords = read_stopwords(stopwords_fp)
    
    while True:
        
        songdata_filename = input('\nEnter a filename for the song data: ')
        
        songdata_fp = open_file(songdata_filename)
        
        if songdata_fp != None:
            break
    
    
    data_dict = read_data(songdata_fp, stopwords)
    avg_word_count = calculate_average_word_count(data_dict)
    vocab = find_singers_vocab(data_dict)

 # # (singer name, average word count, number of songs, vocabulary size)
    display_singers_list = []
    iterated_song = {}
    number_of_songs = {}
    for singer in data_dict:
        if singer not in number_of_songs:
            number_of_songs[singer] = 0
            iterated_song[singer] = ''
            for song in data_dict[singer]:
                if song not in iterated_song[singer]:
                    iterated_song[singer] = song
                    number_of_songs[singer] += 1
        
            
        singer_info = singer, str(round(avg_word_count[singer], 2)), str(len(vocab[singer])), str(number_of_songs[singer])
        display_singers_list.append(singer_info)

    display_singers(display_singers_list)
    print("\nSearch Lyrics by Words")
    
    while True:
        try:
            words_set = set(input("\nInput a set of words (space separated), press enter to exit: ").lower())
            vocab = search_songs(data_dict, words_set)
            print("\nThere are {} songs containing the given words!".format(len(vocab)))
            print("{:<20s} {:<s}".format("Singer", "Song"))
            for ele in vocab:
                print("{:<20s} {:<s}".format(ele[0], ele[1]))
            if words_set != None or words_set == '':
                break
                
        except ValueError:
            print('\nError in words!')
            words_set = set(input("\nInput a set of words (space separated), press enter to exit: "))
    
if __name__ == '__main__':
    main()           
