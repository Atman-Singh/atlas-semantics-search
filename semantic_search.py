import os
import operator as op
import time
import numpy

def main():

    # source
    directory = r'C:\Users\Atman S\Documents\GitHub\embeddings\embeddings\sources\\'

    # list that will contain text from each page
    pages = []
    unique_words = []

    # write all filtered text from each file in directory to a new index in pages
    for files in os.listdir(directory):
        with open(directory + files, encoding="utf8") as f:
            page = filter(f.read()).lower().split()
            pages.append(page)
            for word in delete_duplicates(page):
                unique_words.append(word)
    
    # convert words to vectors
    vector_map = vectorize_words(unique_words, pages)

    while True:
        ui = input('Enter an FTC related word (eg. 3d): ')
        print(semantics_search(vector_map, ui))

# deletes unwanted characters
def filter(text):
    unwanted = ['-', '^', '\n', '~', 'Â°', '=', '<', '>', '*', '.', '{', '}', "\\", "(", ")", "/", ":", '`', ',', '+', '|', '@']

    for character in unwanted:
        replacement = ' '
        if character == 'Â°':
            replacement = ' degrees'
        text = text.replace(character, replacement)

    return text

# deletes all duplicate words and links from a list
def delete_duplicates(list):
    unique_words = []
    
    # check if word is unique and add to list
    for word in list:
        found = False
        for unique_word in unique_words:
            if word == unique_word:
                found = True
        if not found:
            unique_words.append(word)
    
    # remove any word that contains a link
    for word in unique_words:
        if 'http' in word or 'mgn' in word:
            unique_words.remove(word)     

    return unique_words

# return a list of frequencies of a given word 
def check_frequency(target, pages):
    frequencies = []
    for page in pages:
        frequencies.append(op.countOf(page, target))
    return frequencies

# vectorizes a list of words and places them in a hashmap
def vectorize_words(unique_words, pages):
    vector_map = {}
    start = time.time()
    for unique_word in unique_words:
            vector_map[unique_word] = [0] * 101
    for i, page in enumerate(pages):
        for word in page:
            if word in unique_words:
                vector_map[word][i] += 1
    end = time.time()
    print(f"Vectorization finished in {round(end-start,3)} seconds")
    return vector_map

# verifies if key is in hashmap to prevent KeyError and retrieved value if key is valid
def retrieve_vector(hashmap, key):
    if key.lower() in hashmap:
        return hashmap[key.lower()]
    else:
        return 'invalid key'
    
# returns 10 closest words based on vector
def semantics_search(hashmap, word):

    # check if vector is in hashmap and retrieve vector
    vector = retrieve_vector(hashmap, word)
    if type(vector) == str:
        return vector
    
    # get the similarity value between the chosen word and every other word in the hashmap, if similarity is greater than 0 then add to the similarities array
    similarities = {}
    for key, value in hashmap.items():
        similarity = get_similarity(vector, value)
        if similarity > 0 and not check_contain(key, word):
            similarities[key] = 0
            similarities[key] += similarity

    # sort similarities in descending order so most similar words come first
    sorted = sort_hashmap_by_value(similarities)

    # return the 10 most similar words
    if len(sorted) > 10:
        sorted = sorted[:10]
    return sorted

# returns the cosine angle between two vectors
def get_similarity(v1, v2):
    return numpy.dot(v1, v2) / (numpy.linalg.norm(v1) * numpy.linalg.norm(v2))

# checks if two words contain eachother
def check_contain(word_one, word_two):
    return word_one in word_two or word_two in word_one

# sorts hashmap via merge sort
def sort_hashmap_by_value(hashmap):
    return sorted(hashmap.items(), key=lambda x:x[1], reverse=True)

if __name__ == '__main__':
    main()
    