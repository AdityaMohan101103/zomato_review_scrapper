import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape reviews from Zomato
def scrape_reviews(url):
    response = requests.get(url)
    if response.status_code != 200:
        st.error("Failed to retrieve the page. Please check the URL.")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    reviews = []

    # Find the review section
    review_section = soup.find_all('div', class_='sc-1hez2tp-0')  # Adjust this class as needed
    for review in review_section:
        user_name = review.find('p', class_='sc-faswKr').text if review.find('p', class_='sc-faswKr') else 'Unknown User'
        review_text = review.find('p', class_='sc-dTOuAs').text if review.find('p', class_='sc-dTOuAs') else 'No Review'
        rating = review.find('div', class_='sc-1q7bklc-1').text if review.find('div', class_='sc-1q7bklc-1') else 'No Rating'
        reviews.append({'User   ': user_name, 'Review': review_text, 'Rating': rating})

    return reviews

# Streamlit UI
st.title("Zomato Review Scraper")

# User input for Zomato URL
url = st.text_input("Enter Zomato URL:")

if st.button("Scrape Reviews"):
    if url:
        reviews = scrape_reviews(url)
        if reviews:
            df = pd.DataFrame(reviews)
            st.write(df)

            # Save to CSV
            csv = df.to_csv(index=False)
            st.download_button("Download CSV", csv, "reviews.csv", "text/csv")
    else:
        st.warning("Please enter a valid Zomato URL.")
