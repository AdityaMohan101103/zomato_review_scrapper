import streamlit as st
from requests_html import HTMLSession

def fetch_reviews(url):
    session = HTMLSession()
    try:
        r = session.get(url)
        r.html.render(timeout=20, sleep=2)
    except Exception as e:
        return f"Error rendering page: {e}", []

    reviews = []

    names = r.html.find('p.sc-1hez2tp-0.sc-faswKr')
    ratings = r.html.find('div.sc-1q7bklc-1')
    tags = r.html.find('div.sc-1q7bklc-9')
    comments = r.html.find('p.sc-1hez2tp-0.sc-dTOuAs')

    for i in range(min(len(names), len(comments))):
        review = {
            "name": names[i].text,
            "rating": ratings[i].text if i < len(ratings) else '',
            "tag": tags[i].text if i < len(tags) else '',
            "comment": comments[i].text
        }
        reviews.append(review)

    return "Success", reviews

# Streamlit UI
st.title("🍔 Zomato Review Scraper (requests-html)")

url = st.text_input("Enter Zomato Restaurant Reviews URL:")

if st.button("Fetch Reviews"):
    if url:
        st.info("Fetching reviews, please wait...")
        status, results = fetch_reviews(url)
        if status != "Success" or not results:
            st.error("No reviews found or scraping failed.")
        else:
            for r in results:
                st.markdown(f"**{r['name']}** - ⭐ {r['rating']} - *{r['tag']}*")
                st.write(r["comment"])
                st.markdown("---")
    else:
        st.warning("Please enter a URL.")
