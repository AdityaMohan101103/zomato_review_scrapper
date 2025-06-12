import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time


def scrape_reviews_with_selenium(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Automatically install ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "sc-1hez2tp-0"))
        )
    except:
        st.error("Failed to load reviews. Zomato may have blocked automation or changed its layout.")
        driver.quit()
        return None

    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    reviews_elements = driver.find_elements(By.CLASS_NAME, "sc-1hez2tp-0")

    reviews = []
    for review_element in reviews_elements:
        try:
            user = review_element.find_element(By.CLASS_NAME, "sc-faswKr").text
        except:
            user = "Unknown User"
        try:
            review_text = review_element.find_element(By.CLASS_NAME, "sc-dTOuAs").text
        except:
            review_text = "No Review"
        try:
            rating = review_element.find_element(By.CLASS_NAME, "sc-1q7bklc-1").text
        except:
            rating = "No Rating"

        reviews.append({"User": user, "Review": review_text, "Rating": rating})

    driver.quit()
    return reviews


# Streamlit UI
st.title("Zomato Review Scraper (Selenium)")

url = st.text_input("Enter Zomato Restaurant URL:")

if st.button("Scrape Reviews"):
    if url:
        reviews = scrape_reviews_with_selenium(url)
        if reviews:
            df = pd.DataFrame(reviews)
            st.write(df)
            csv = df.to_csv(index=False)
            st.download_button("Download CSV", csv, "zomato_reviews.csv", "text/csv")
        else:
            st.warning("No reviews found or scraping failed.")
    else:
        st.warning("Please enter a valid Zomato URL.")
