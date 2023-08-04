import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd

# Sample email data and labels
sample_data = [
    ("Get rich quick! Earn $1000s with our amazing offer.", "Spam"),
    ("Hi there, just checking in. How are you?", "Not Spam"),
    ("URGENT: Your account needs verification.", "Spam"),
    ("Let's meet for coffee this weekend.", "Not Spam"),
]

# Create a DataFrame from the sample data
data = pd.DataFrame(sample_data, columns=['email', 'label'])

# Initialize the TfidfVectorizer
vectorizer = TfidfVectorizer()

# Fit and transform the vectorizer on the sample data
X_train_vectorized = vectorizer.fit_transform(data['email'])

# Train the classifier
classifier = MultinomialNB()
classifier.fit(X_train_vectorized, data['label'])

# Streamlit app
def main():
    st.title("Email Spam Checker")

    # Input field for email text
    email_input = st.text_area("Enter an email:")

    if st.button("Check for Spam"):
        vectorized_email = vectorizer.transform([email_input])
        prediction = classifier.predict(vectorized_email)[0]
        
        if prediction == "Not Spam":
            st.write("This email is likely not spam.")
        else:
            st.write("This email is likely spam.")

if __name__ == "__main__":
    main()
