# app.py
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_zomato_reviews(url):
    headers = {
        "User-Agent": "Mozilla/5.0",
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return "Failed to load page", []

        soup = BeautifulSoup(response.text, 'html.parser')

        users = soup.find_all("p", class_="sc-1hez2tp-0 sc-faswKr")
        ratings = soup.find_all("div", class_="sc-1q7bklc-1")
        reviews = soup.find_all("p", class_="sc-1hez2tp-0 sc-dTOuAs")

        data = []
        for user, rating, review in zip(users, ratings, reviews):
            data.append({
                "User": user.get_text(strip=True),
                "Rating": rating.get_text(strip=True),
                "Review": review.get_text(strip=True)
            })

        return None, data

    except Exception as e:
        return str(e), []

# Streamlit app UI
st.title("Zomato Review Scraper (BeautifulSoup)")

url = st.text_input("Enter Zomato Restaurant Reviews URL:")

if st.button("Scrape Reviews"):
    if url:
        error, reviews = scrape_zomato_reviews(url)
        if error:
            st.error(error)
        elif not reviews:
            st.warning("No reviews found or scraping failed.")
        else:
            df = pd.DataFrame(reviews)
            st.write(df)
            csv = df.to_csv(index=False)
            st.download_button("Download CSV", csv, "reviews.csv", "text/csv")
    else:
        st.warning("Please enter a valid Zomato review URL.")
