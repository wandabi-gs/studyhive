import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import string
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import RidgeClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report


df = pd.read_csv("dataset.csv")

# Drop unnecessary columns
df = df.drop(columns=['count','index'])

# Convert text to lowercase
df['clean_tweet'] = df['tweet'].str.lower()

# Remove punctuation and special characters
df['clean_tweet'] = df['clean_tweet'].apply(lambda x: x.translate(str.maketrans('', '', string.punctuation)))

# Tokenize the text
df['clean_tweet'] = df['clean_tweet'].apply(word_tokenize)


# Initialize stemming
stemmer = PorterStemmer()

lemmatizer = WordNetLemmatizer()
df['clean_tweet'] = df['clean_tweet'].apply(lambda x: [lemmatizer.lemmatize(word) for word in x])
df['clean_tweet'] = df['clean_tweet'].apply(lambda x: ' '.join(x))

# Save the cleaned dataset
df.to_csv("cleaned_dataset.csv", index=False)

df = pd.read_csv('cleaned_dataset.csv')
print(df.head())

# Split the dataset into features and labels
X = df['clean_tweet']
y = df['class']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert text data to TF-IDF features
vectorizer = TfidfVectorizer(max_features=10000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train and test K-Nearest Neighbors (KNN) classifier
knn_classifier = KNeighborsClassifier()
knn_classifier.fit(X_train_tfidf, y_train)
y_pred_knn = knn_classifier.predict(X_test_tfidf)
accuracy_knn = accuracy_score(y_test, y_pred_knn)

# Train and test Ridge Regression (RR) classifier
rr_classifier = RidgeClassifier()
rr_classifier.fit(X_train_tfidf, y_train)
y_pred_rr = rr_classifier.predict(X_test_tfidf)
accuracy_rr = accuracy_score(y_test, y_pred_rr)

# Train and test Naive Bayes classifier
nb_classifier = MultinomialNB()
nb_classifier.fit(X_train_tfidf, y_train)
y_pred_nb = nb_classifier.predict(X_test_tfidf)
accuracy_nb = accuracy_score(y_test, y_pred_nb)

linear_classifier = LinearSVC()
linear_classifier.fit(X_train_tfidf, y_train)
y_pred_linear = linear_classifier.predict(X_test_tfidf)
accuracy_linear = accuracy_score(y_test, y_pred_linear)

print("Classification Report - KNN:")
print(classification_report(y_test, y_pred_knn))

# Print classification report for Ridge Regression classifier
print("Classification Report - Ridge Regression:")
print(classification_report(y_test, y_pred_rr))

# Print classification report for Naive Bayes classifier
print("Classification Report - Naive Bayes:")
print(classification_report(y_test, y_pred_nb))

# Print classification report for Linear SVC classifier
print("Classification Report - Linear SVC:")
print(classification_report(y_test, y_pred_linear))

# Save the best performing model using Joblib
best_model = None
best_accuracy = max(accuracy_knn, accuracy_rr, accuracy_nb, accuracy_linear)
if best_accuracy == accuracy_knn:
    best_model = knn_classifier
elif best_accuracy == accuracy_rr:
    best_model = rr_classifier
elif best_accuracy == accuracy_linear:
    best_model = linear_classifier
else:
    best_model = nb_classifier

import joblib
joblib.dump(best_model, "hate_speech_detection_model.pkl")
joblib.dump(vectorizer, "hate_speech_detection_vectorizer.pkl")