import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_reviews(url, max_pages=1):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    all_reviews = []

    for page in range(1, max_pages + 1):
        paginated_url = f"{url}?page={page}&sort=dd&filter=reviews-dd"
        res = requests.get(paginated_url, headers=headers)

        if res.status_code != 200:
            print(f"Failed to load page {page}: Status code {res.status_code}")
            break

        soup = BeautifulSoup(res.text, "html.parser")

        users = soup.find_all("p", class_="sc-faswKr")
        ratings = soup.find_all("div", class_="sc-1q7bklc-1")
        texts = soup.find_all("p", class_="sc-dTOuAs")

        if not users:
            print(f"No reviews found on page {page}.")
            break

        for user, rating, review in zip(users, ratings, texts):
            all_reviews.append({
                "User": user.get_text(strip=True),
                "Rating": rating.get_text(strip=True),
                "Review": review.get_text(strip=True)
            })

        time.sleep(1)  # polite delay between page fetches

    return pd.DataFrame(all_reviews)

# Example usage
if __name__ == "__main__":
    url = "https://www.zomato.com/kolkata/burger-singh-big-punjabi-burgers-1-baguihati/reviews"
    df = scrape_reviews(url, max_pages=3)  # You can change number of pages
    print(df)
    df.to_csv("zomato_reviews.csv", index=False)
