import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.feature_extraction.text import CountVectorizer


"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""


url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/spambase/spambase.data'

column_names = [
    'word_freq_make', 'word_freq_address', 'word_freq_all', 'word_freq_3d',
    'word_freq_our', 'word_freq_over', 'word_freq_remove', 'word_freq_internet',
    'word_freq_order', 'word_freq_mail', 'word_freq_receive', 'word_freq_will',
    'word_freq_people', 'word_freq_report', 'word_freq_addresses', 'word_freq_free',
    'word_freq_business', 'word_freq_email', 'word_freq_you', 'word_freq_credit',
    'word_freq_your', 'word_freq_font', 'word_freq_000', 'word_freq_money',
    'word_freq_hp', 'word_freq_hpl', 'word_freq_george', 'word_freq_650',
    'word_freq_lab', 'word_freq_labs', 'word_freq_telnet', 'word_freq_857',
    'word_freq_data', 'word_freq_415', 'word_freq_85', 'word_freq_technology',
    'word_freq_1999', 'word_freq_parts', 'word_freq_pm', 'word_freq_direct',
    'word_freq_cs', 'word_freq_meeting', 'word_freq_original', 'word_freq_project',
    'word_freq_re', 'word_freq_edu', 'word_freq_table', 'word_freq_conference',
    'char_freq_;', 'char_freq_(', 'char_freq_[', 'char_freq_!', 'char_freq_$',
    'char_freq_#', 'capital_run_length_average', 'capital_run_length_longest',
    'capital_run_length_total', 'label'
]

dataset = pd.read_csv(url, header=None, names=column_names)

X = dataset.drop('label', axis=1)  # Features
y = dataset['label'] 

X_train, y_train = load_and_preprocess_data()


# Fit the TfidfVectorizer on training data
vectorizer = TfidfVectorizer()
X_train_vectorized = vectorizer.fit_transform(X_train)


# Initialize the CountVectorizer
classifier = train_classifier(X_train_vectorized, y_train)

def predict_spam_or_ham(email_text, classifier, vectorizer):
    # Preprocess the email text
    preprocessed_text = preprocess_text(email_text)
    # Transform the preprocessed text using the fitted vectorizer
    vectorized_text = vectorizer.transform([preprocessed_text])
    # Use the trained classifier to predict
    prediction = classifier.predict(vectorized_text)[0]
    return prediction


def main():
    st.title("Spam Email Detection App")
    st.write("Enter an email to check if it's spam or not:")

    # Text input for user to enter email
    email_input = st.text_area("Email Text")

    if st.button("Check"):
        if email_input.strip():  # Ensure input is not empty
            prediction = predict_spam_or_ham(email_input, classifier)
            result = "Spam" if prediction == 1 else "Ham"
            st.write(f"Prediction: {result}")

if __name__ == "__main__":
    main()
    
