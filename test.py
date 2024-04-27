import joblib

loaded_model = joblib.load("hate_speech_detection_model.pkl")
loaded_vectorizer = joblib.load("tfidf_vectorizer.pkl")

while True:
    new_text = input("Enter a text: ")
    new_text_tfidf = loaded_vectorizer.transform([new_text])
    prediction = loaded_model.predict(new_text_tfidf)
    print(prediction)
    if prediction == 2:
        print("The text is classified as neither hate speech nor offensive language.")
    elif prediction == 1:
        print("The text is classified as offensive language.")
    elif prediction == 0:
        print("The text is classified as hate speech.")