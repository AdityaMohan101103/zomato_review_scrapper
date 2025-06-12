import streamlit as st
import requests
import re
import json
import pandas as pd

def extract_reviews_from_zomato(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        st.error("Failed to load page. Check URL.")
        return []

    # Extract embedded JSON from script tag
    match = re.search(r'window\.__PRELOADED_STATE__\s*=\s*({.*});', response.text)
    if not match:
        st.error("Could not find embedded data in the page.")
        return []

    data = json.loads(match.group(1))

    try:
        reviews_data = data["pages"]["restaurant"]["sections"]["REVIEWS"]["sectionData"]["data"]["userReviewList"]
        reviews = []
        for review in reviews_data:
            user = review.get("userName", "Unknown")
            text = review.get("reviewText", "No review")
            rating = review.get("reviewRating", {}).get("rating", "No rating")
            reviews.append({
                "User": user,
                "Review": text,
                "Rating": rating
            })
        return reviews
    except Exception as e:
        st.error("Failed to parse reviews. Zomato page structure may have changed.")
        return []

# Streamlit UI
st.title("Zomato Review Scraper (Web-Friendly)")

url = st.text_input("Enter Zomato Restaurant URL:")

if st.button("Scrape Reviews"):
    if url:
        reviews = extract_reviews_from_zomato(url)
        if reviews:
            df = pd.DataFrame(reviews)
            st.write(df)
            csv = df.to_csv(index=False)
            st.download_button("Download CSV", csv, "zomato_reviews.csv", "text/csv")
        else:
            st.warning("No reviews found.")
    else:
        st.warning("Please enter a valid Zomato URL.")
