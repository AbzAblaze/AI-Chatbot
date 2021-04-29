#Imports
from newspaper import Article
import random
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import string
import warnings
warnings.filterwarnings('ignore')
 
#Punkt 
nltk.download('punkt', quiet=True)
 
#Article
article = Article('https://www.northshore.org/family-medicine/patient-education/common-illnesses/')
article.download()
article.parse()
article.nlp()
corpus = article.text
 
#Tokenization
text = corpus
sentence_list = nltk.sent_tokenize(text) 

#Greeting Responses
def greeting_response(text):
    text = text.lower()
    #Bots greeting response
    bot_greetings = ['hey there', 'hi!', 'hello!', 'greetings!']
    #User greeting
    user_greetings = ['hi', 'hey', 'hello','hello there','greetings']
    #Bot Greets User Back
    for word in text.split():
        if word in user_greetings:
            return random.choice(bot_greetings)

 
#Index Sort 
def index_sort(list_var):
    lenght = len(list_var)
    list_index = list(range(0, lenght))
 
    x = list_var
    for i in range(lenght):
        for j in range(lenght):
            if x[list_index[i]] > x[list_index[j]]:
                #Swap
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp
 
    return list_index
 
#Medical Response
def medical_response(user_input):
    user_input = user_input.lower()
    sentence_list.append(user_input)
    medical_response = ''
    cm = CountVectorizer().fit_transform(sentence_list)
    similarity_scores = cosine_similarity(cm[-1], cm)
    similarity_scores_list = similarity_scores.flatten()
    index = index_sort(similarity_scores_list)
    index = index[1:]
    response_flag = 0
 
    j = 0
    for i in range(len(index)):
        if similarity_scores_list[index[i]] > 0.0:
            medical_response = medical_response+' '+sentence_list[index[i]]
            response_flag = 1
            j = j+1
        if j > 5:
            break
 
        if response_flag == 0:
            medical_response = medical_response+' '+"Sorry, I'm not able to help you with this. Try again."
        sentence_list.remove(user_input)
 
        return medical_response
 
#Chat Start
print('MediBot: Hello. I am MediBot. I will answer all your Medical enquiries. To exit, type [quit].') 
quit_words = ['exit', 'quit','stop']
while(True):
    user_input = input('User: ')
    if user_input.lower() in quit_words:
        print('MediBot: See you later.')
        break
    else:
        if greeting_response(user_input) != None:
            print('MediBot: '+greeting_response(user_input))
        else:
            print('MediBot: '+medical_response(user_input))
