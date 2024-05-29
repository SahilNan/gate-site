import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

def read_lines(file_name):
    file1 = open(file_name, 'r')
    lines = file1.readlines()
    file1.close()
    return lines

def read_questions(lines, data, category):
    prev_len = len(data)
    question = ""
    catflag = False
    catflagFound = False
    for line in lines:
        print(line)
        if(line.startswith("Question:")):
            if(question != ""):
                data.append(question)
                question = ""
                if(not catflagFound):
                    category.append("UnKnown")
            catflag = False
            catflagFound = False
        elif(line.startswith("Category:")):
            catflag = True
            catflagFound = True
        elif(catflag):
            category.append(line.strip())
            catflag = False
        elif(not line.startswith("Options:")):
            question += line

    if(question != ""):
        data.append(question)
        if(not catflagFound):
            category.append("UnKnown")
    print(f'Total questions:  {len(data) - prev_len}')

data = []
category = []
read_questions(read_lines('qp\\qp_2007.txt'), data, category)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data, category, test_size=0.2)

# Create a TfidfVectorizer to convert text to numerical features
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

# Train a logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)


# Evaluate the model on the test set
score = model.score(X_test, y_test)
print('Accuracy:', score)

P_test = ['''
The most efficient algorithm for finding the number of connected components in an undirected
graph on n vertices and m edges has time complexity
(A) &Theta;(n) 
(B) &Theta;(m) 
(C) &Theta;(m+n) 
(D) &Theta;(mn)
''','''
Let r denote number system radix. The only value(s) of r that satisfy the equation
&radic;121<sub>r</sub> =11<sub>r</sub> is/are
(A) decimal 10 
(B) decimal 11
(C) decimal 10 and 11 
(D) any value > 2
'''
]
P_test = vectorizer.transform(P_test)
print('Prediction :', model.predict(P_test))

read_questions(read_lines('qp/qp_2008.txt'), data, category)
read_questions(read_lines('qp/qp_2009.txt'), data, category)
read_questions(read_lines('qp/qp_2010.txt'), data, category)
read_questions(read_lines('qp/qp_2011.txt'), data, category)
read_questions(read_lines('qp/qp_2012.txt'), data, category)
read_questions(read_lines('qp/qp_2013.txt'), data, category)
read_questions(read_lines('qp/qp_2014_1.txt'), data, category)
read_questions(read_lines('qp/qp_2014_2.txt'), data, category)
read_questions(read_lines('qp/qp_2014_3.txt'), data, category)
read_questions(read_lines('qp/qp_2015_1.txt'), data, category)
read_questions(read_lines('qp/qp_2015_2.txt'), data, category)
read_questions(read_lines('qp/qp_2015_3.txt'), data, category)
read_questions(read_lines('qp/qp_2016_1.txt'), data, category)
read_questions(read_lines('qp/qp_2016_2.txt'), data, category)
read_questions(read_lines('qp/qp_2017_1.txt'), data, category)
read_questions(read_lines('qp/qp_2017_2.txt'), data, category)
read_questions(read_lines('qp/qp_2018.txt'), data, category)
read_questions(read_lines('qp/qp_2019.txt'), data, category)
read_questions(read_lines('qp/qp_2020.txt'), data, category)
read_questions(read_lines('qp/qp_2021_1.txt'), data, category)
read_questions(read_lines('qp/qp_2021_2.txt'), data, category)
read_questions(read_lines('qp/qp_2022.txt'), data, category)
read_questions(read_lines('qp/qp_2023.txt'), data, category)

print(f'Total questions:  {len(data)}')

cv = CountVectorizer(max_df=0.9, min_df=2, stop_words="english")
dtm = cv.fit_transform(data)
lda = LatentDirichletAllocation(n_components=10, random_state=42)
lda.fit(dtm)
print(len(cv.get_feature_names_out()))
print(len(lda.components_[0]))
n = 15
for index, topic in enumerate(lda.components_):
    print(f'The top {n} words for topic #{index}')
    print([cv.get_feature_names_out()[i] for i in topic.argsort()[-n:]])
topic_results = lda.transform(dtm)
print(topic_results.shape)
print(topic_results[0].round(2))
data_topics = topic_results.argmax(axis=1)
print(f'Question topics:  {len(data_topics)}')

for index, question in enumerate(data):
    if(data_topics[index] == 9):
        #print(question)
        pass
