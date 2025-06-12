import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_reviews(url, max_pages=3):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    all_reviews = []

    for page in range(1, max_pages + 1):
        paginated_url = f"{url}?page={page}&sort=dd&filter=reviews-dd"
        res = requests.get(paginated_url, headers=headers)

        if res.status_code != 200:
            st.warning(f"Failed to load page {page}: Status code {res.status_code}")
            break

        soup = BeautifulSoup(res.text, "html.parser")

        users = soup.find_all("p", class_="sc-faswKr")
        ratings = soup.find_all("div", class_="sc-1q7bklc-1")
        texts = soup.find_all("p", class_="sc-dTOuAs")

        if not users:
            break

        for user, rating, review in zip(users, ratings, texts):
            all_reviews.append({
                "User": user.get_text(strip=True),
                "Rating": rating.get_text(strip=True),
                "Review": review.get_text(strip=True)
            })

        time.sleep(1)

    return pd.DataFrame(all_reviews)

# Streamlit UI
st.title("Zomato Review Scraper (Requests + BeautifulSoup)")

url = st.text_input("Enter Zomato Restaurant URL (e.g., ending in /reviews):")

if st.button("Scrape Reviews"):
    if not url:
        st.warning("Please enter a Zomato review URL.")
    else:
        with st.spinner("Scraping reviews..."):
            df = scrape_reviews(url)
        if not df.empty:
            st.success(f"Found {len(df)} reviews.")
            st.dataframe(df)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", data=csv, file_name="zomato_reviews.csv", mime="text/csv")
        else:
            st.warning("No reviews found or failed to scrape.")
