import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split

# Sample email data and labels
sample_data = [
    ("Get rich quick! Earn $1000s with our amazing offer.", "Spam"),
    ("Hi there, just checking in. How are you?", "Not Spam"),
    ("URGENT: Your account needs verification.", "Spam"),
    ("Let's meet for coffee this weekend.", "Not Spam"),
]

# Create a DataFrame from the sample data
data = pd.DataFrame(sample_data, columns=['email', 'label'])

# Split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(data['email'], data['label'], test_size=0.2, random_state=42)

# Initialize the TfidfVectorizer
vectorizer = TfidfVectorizer()

# Fit and transform the vectorizer on the training data
X_train_vectorized = vectorizer.fit_transform(X_train)

# Train the classifier
classifier = MultinomialNB()
classifier.fit(X_train_vectorized, y_train)

# Streamlit app
def main():
    st.title("Custom Spam Email Detection")
    email_input = st.text_area("Enter an email:")

    if st.button("Predict"):
        vectorized_email = vectorizer.transform([email_input])
        prediction = classifier.predict(vectorized_email)[0]

        st.write("Prediction:", prediction)

if __name__ == "__main__":
    main()
