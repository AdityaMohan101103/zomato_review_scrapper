import requests
from bs4 import BeautifulSoup
import streamlit as st

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def extract_reviews_from_soup(soup):
    reviews = []
    names = soup.find_all("p", class_="sc-1hez2tp-0 sc-faswKr jihbqh")
    ratings = soup.find_all("div", class_="sc-1q7bklc-1 cILgox")
    order_types = soup.find_all("div", class_="sc-1q7bklc-9 dYrjiw")
    texts = soup.find_all("p", class_="sc-1hez2tp-0 sc-dTOuAs iuORyl")

    for name, rating, order_type, text in zip(names, ratings, order_types, texts):
        reviews.append({
            "name": name.get_text(strip=True),
            "rating": rating.get_text(strip=True),
            "order_type": order_type.get_text(strip=True),
            "review": text.get_text(strip=True)
        })

    return reviews

def get_total_pages(soup):
    pagination = soup.select("div.sc-dyKSPo.fzMVJV")
    return max([int(p.text) for p in pagination] or [1])

def scrape_reviews(url):
    all_reviews = []

    if not url.endswith("/reviews"):
        if url.endswith("/"):
            url = url + "reviews"
        else:
            url = url + "/reviews"

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    total_pages = get_total_pages(soup)

    for page in range(1, total_pages + 1):
        paged_url = f"{url}?page={page}&sort=dd&filter=reviews-dd"
        res = requests.get(paged_url, headers=headers)
        paged_soup = BeautifulSoup(res.text, "html.parser")
        page_reviews = extract_reviews_from_soup(paged_soup)
        if not page_reviews:
            break
        all_reviews.extend(page_reviews)

    return all_reviews


# 🟢 Streamlit Web App
st.title("🍔 Zomato Review Scraper (BeautifulSoup)")
url = st.text_input("Enter Zomato Restaurant Reviews URL:")

if url:
    with st.spinner("Fetching reviews, please wait..."):
        try:
            reviews = scrape_reviews(url)
            if reviews:
                st.success(f"Found {len(reviews)} reviews!")
                for r in reviews:
                    st.write(f"**{r['name']}** ({r['order_type']}) ⭐ {r['rating']}")
                    st.write(r['review'])
                    st.markdown("---")
            else:
                st.warning("No reviews found or scraping failed.")
        except Exception as e:
            st.error(f"Error occurred: {e}")
