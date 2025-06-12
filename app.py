import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

st.title("🍔 Zomato Review Scraper (BeautifulSoup)")
url = st.text_input("Enter Zomato Restaurant Reviews URL:")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

def scrape_reviews_bs4(zomato_url):
    try:
        response = requests.get(zomato_url, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        st.error(f"Request failed: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    reviewers = soup.find_all("p", class_=re.compile(r"sc-1hez2tp-0.*sc-faswKr"))
    ratings = soup.find_all("div", class_=re.compile(r"sc-1q7bklc-1.*"))
    types = soup.find_all("div", class_=re.compile(r"sc-1q7bklc-9.*"))
    comments = soup.find_all("p", class_=re.compile(r"sc-1hez2tp-0.*sc-dTOuAs"))

    results = []
    for i in range(min(len(reviewers), len(ratings), len(types), len(comments))):
        results.append({
            "Reviewer": reviewers[i].text.strip(),
            "Rating": ratings[i].text.strip(),
            "Type": types[i].text.strip(),
            "Comment": comments[i].text.strip()
        })
    return results

if url:
    st.write("Fetching reviews, please wait...")
    reviews = scrape_reviews_bs4(url)
    if reviews:
        for r in reviews:
            st.markdown(f"**{r['Reviewer']}** ({r['Type']})")
            st.markdown(f"⭐ {r['Rating']} — {r['Comment']}")
            st.markdown("---")
    else:
        st.warning("No reviews found or scraping failed.")
