import nltk
import requests
from bs4 import BeautifulSoup
import string
import syllapy

nltk.download('punkt')

#get_url = "https://en.wikipedia.org/wiki/Readability"


def text_complexity(response):

    list1=[]
    count_difficult_word = 0
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text(strip=True, separator="\n")

   
    words = nltk.word_tokenize(text)

    sentences = nltk.sent_tokenize(text)
    num_of_sentences = len(sentences)

    word_list = []
    for i in words:
        syllable_count = syllapy.count(i)
        word_list.append(i)
        if syllable_count >= 3:
            count_difficult_word += 1

    new_list_word = [''.join(char for char in item if char not in string.punctuation)
                     for item in word_list if any(char.isalpha() or char.isspace() for char in item)]

    percentage_difficult_word = (count_difficult_word / len(new_list_word)) * 100

    print("Number of words", len(new_list_word))
    print("Num of Sentences:", num_of_sentences)

    average_words_per_sentence = len(new_list_word) / num_of_sentences

    gunning_fog_index = (average_words_per_sentence + percentage_difficult_word) * 0.4

    list1.append(len(new_list_word))
    list1.append(num_of_sentences)
    list1.append(gunning_fog_index)

    return gunning_fog_index
