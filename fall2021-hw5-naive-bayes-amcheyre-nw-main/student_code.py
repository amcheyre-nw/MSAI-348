import math
import re

class Bayes_Classifier:

    def __init__(self):
        self.pos_dictionary = {}
        self.neg_dictionary = {}
        self.overall_positive_probability = 0
        self.overall_negative_probability = 0
        self.vocabulary_list = []

    # Takes a list of lines from the dataset
    def train(self, lines):
        # Create dictionary for key: value -> num_review : rate
        rate_dictionary = separate_by_number_rate(lines)
        # Create dictionary for key: value -> rate : list(text)
        reviews_dictionary = separate_by_number_text(lines)
        # Normalize text
        reviews_dictionary = lower_case(reviews_dictionary)
        reviews_dictionary = delete_punctuation(reviews_dictionary)
        # Separate each text in tokens
        dataset = tokenize(reviews_dictionary)
        # Build vocabulary: Find unique words from data
        self.vocabulary_list = vocabulary(dataset)

        # Calculate probability P(+) and P(-) from all data
        positive_review = 0
        negative_review = 0
        total_review = 0
        for key, value in rate_dictionary.items():
            total_review += 1
            if value[0] == '5':
                positive_review += 1
            elif value[0] == '1':
                negative_review += 1

        self.overall_positive_probability = positive_review / total_review
        self.overall_negative_probability = negative_review / total_review

        # Calculate probabilities of + and - words
        positive_words = []
        negative_words = []

        for key, value in reviews_dictionary.items():
            classification = rate_dictionary[key]

            if classification == ['1']:
                negative_words.extend(value)
            elif classification == ['5']:
                positive_words.extend(value)

        positive_dictionary = {}
        negative_dictionary = {}

        for word in self.vocabulary_list:
            count = 0
            for positive in positive_words:
                if word == positive:
                    count += 1
            # P(w|+) = (count(w when +) + 1)/ (count(number all + words) + count(unique words))
            positive_dictionary[word] = (count + 1) / (len(positive_words) + len(self.vocabulary_list))

        for word in self.vocabulary_list:
            count = 0
            for negative in negative_words:
                if word == negative:
                    count += 1
            # P(w|-) = (count(w when -) + 1)/ (count(number all - words) + count(unique words))
            negative_dictionary[word] = (count + 1) / (len(negative_words) + len(self.vocabulary_list))

        self.pos_dictionary = positive_dictionary
        self.neg_dictionary = negative_dictionary

    # Returns a list of strings indicating the predicted class
    def classify(self, lines):
        # Predict the class for each review row
        rate_dictionary_test = separate_by_number_rate(lines)
        reviews_dictionary_test = separate_by_number_text(lines)
        reviews_dictionary_test = lower_case(reviews_dictionary_test)
        reviews_dictionary_test = delete_punctuation(reviews_dictionary_test)

        # Separate each text in tokens
        data_test = tokenize(reviews_dictionary_test)
        predicted_class = []

        for key, value in data_test.items():
            pos_prob = 0
            neg_prob = 0

            for word in value:
                if word in self.vocabulary_list:
                    neg_prob = neg_prob + math.log(self.neg_dictionary[word])
                    pos_prob = pos_prob + math.log(self.pos_dictionary[word])
                else:
                    pos_prob = pos_prob
                    neg_prob = neg_prob

            pos_prob = pos_prob + math.log(self.overall_positive_probability)
            neg_prob = neg_prob + math.log(self.overall_negative_probability)
            max_prob = max(pos_prob, neg_prob)

            if max_prob == pos_prob:
                predicted_class.append('5')

            elif max_prob == neg_prob:
                predicted_class.append('1')

        return predicted_class

# Split the dataset by class values, returns a dictionary
def separate_by_number_rate(dataset):
    separated = {}

    for i in dataset:
        num_review = i.split('|')[1].strip()
        class_value = i.split('|')[0].strip()
        if (num_review not in separated):
            separated[num_review] = []
        separated[num_review].append(class_value)
    return separated

def separate_by_number_text(dataset):
    separated = {}

    for i in dataset:
        num_review = i.split('|')[1]
        vector = i.split('|')[2]
        if (num_review not in separated):
            separated[num_review] = []
        separated[num_review].append(vector)
    return separated

def group_by_rate(dataset):
    separated = {}
    separated['5'] = []
    separated['1'] = []
    for i in dataset:
        class_value = i.split('|')[0].strip()
        vector = i.split('|')[2]
        if class_value =='1':
            if separated['1'] == []:
                separated['1'] = vector
                print(vector)
            else:
                aux = separated['1'] + vector
                print(aux)
                separated['1'] = aux

        elif class_value =='5':
            if separated['5'] == []:
                separated['5'] = vector
            else:
                aux = separated['5'] + vector
                separated['5'] = aux
    return separated

def lower_case(dictionary):

    for key, value in dictionary.items():
        aux = value[0].lower()
        value[0]=aux
    return dictionary

def delete_punctuation(dictionary):

    for key, value in dictionary.items():
        aux = value[0]
        aux = aux.replace('.', ' ')
        aux = aux.replace(')', '')
        aux = aux.replace('(', '')
        aux = aux.replace('!', '')
        aux = aux.replace('?', '')
        aux = aux.replace('-', ' ')
        aux = aux.replace("'s", "")
        aux = aux.replace("/", "")
        aux = aux.replace(":", "")
        aux = aux.replace("[", "")
        aux = aux.replace("]", "")
        aux = aux.replace("^", "")
        aux = aux.replace("@", "a")
        aux = aux.replace("}", "")
        aux = aux.replace("{", "")
        aux = aux.replace("'", "")
        aux = aux.replace('"', '')
        aux = aux.replace(";", "")
        aux = aux.replace(',', '')
        aux = aux.replace("\n", "")
        aux = re.sub(r"(.)\1+", r"\1",aux)
        value[0] = aux

    return dictionary

def tokenize(dictionary):
    for key, value in dictionary.items():
        tokenized_vector = value[0].split(' ')
        dictionary[key] = tokenized_vector
    for key, value in dictionary.items():
        for word in value:
            if word == "":
                value.remove("")
    return dictionary

def vocabulary(dictionary):
    vocab = []
    for key, value in dictionary.items():
        vocab.extend(value)
    vocab = set(vocab)
    vocab = list(vocab)
    #vocab.remove('')
    return vocab

