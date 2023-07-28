#Loading packages
import pandas as pd
import os
import openai
import string

# Read CSV file into DataFrame df
df1 = pd.read_csv('videos_detail_with_names.csv')
df2 = pd.read_csv('videos_detail_without_names.csv')

# Input questions
question = input("Enter your question for chatGPT: ")
print("Your question: " + question)
query_pool1 = []
for description in df1['title_description']:
    query = question + description
    query_pool1.append(query)

query_pool2 = []
for description in df2['title_description']:
    query = question + description
    query_pool2.append(query)

results1 = []
for query in query_pool1:
    openai.organization = ""
    openai.api_key = ""
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role" : "user",
             "content" : query}
        ]
    )
    result = response.choices[0].message.content
    results1.append(result)

results2 = []
for query in query_pool2:
    openai.organization = ""
    openai.api_key = ""
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role" : "user",
             "content" : query}
        ]
    )
    result = response.choices[0].message.content
    results2.append(result)

predicted = [x.lower() for x in results1]
new_predicted1 = []
for answer in predicted:
    for character in answer:
        if character in string.punctuation:
            answer = answer.replace(character,"")
    new_predicted1.append(answer)

predicted = [x.lower() for x in results2]
new_predicted2 = []
for answer in predicted:
    for character in answer:
        if character in string.punctuation:
            answer = answer.replace(character,"")
    new_predicted2.append(answer)

actual1 = df1["label1"]
actual2 = df2["label1"]

def count_matching_pairs(column1, column2):
    # Create pandas DataFrame from the lists/arrays representing the columns
    df = pd.DataFrame({'Column1': column1, 'Column2': column2})

    # Compare the two columns using the == operator
    matches_df = df['Column1'] == df['Column2']

    # Count the number of True values, i.e., the number of matching pairs
    num_matches = matches_df.sum()

    return num_matches

num_matching_pairs1 = count_matching_pairs(actual1, new_predicted1)
num_matching_pairs2 = count_matching_pairs(actual2, new_predicted2)

TP = num_matching_pairs1
FN = len(actual1) - TP
TN = num_matching_pairs2
FP = len(actual2) - TN
precision = TP/(TP + FP)
recall = TP/(TP + FN)
F1 = 2* precision * recall / (precision + recall)
print('TP is ' + str(TP))
print('FN is ' + str(FN))
print('TN is ' + str(TN))
print('FP is ' + str(FP))
print('precision is ' + str(precision))
print('recall is ' + str(recall))
print('F1 score is ' + str(F1))