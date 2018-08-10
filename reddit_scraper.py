import requests
import csv
from bs4 import BeautifulSoup

if __name__ == "__main__":
    url = "https://old.reddit.com/r/datascience/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')

    attrs = {'class': 'thing', 'data-domain': 'self.datascience'}
    counter = 1
    while counter <= 100:
        for post in soup.find_all("div", attrs=attrs):
            title = post.find("p", class_="title").text
            print(title)
            forward_link = post.find("a", class_="title").attrs["href"]
            print(forward_link)
            
            try:
                author = post.find("a", class_="author").text
            except:
                author = "[deleted]"
            
            print(author)
            likes = post.find("div", attrs={"class": "score unvoted"}).text
            print(likes)
            comments = post.find("a", class_="comments").text.split()[0]
            print(comments)
            print('=========================')

            post_line = [counter, title, author, likes, comments]

            with open('output.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(post_line)
            
            counter += 1
        
        next_button = soup.find("span", class_="next-button")
        next_page_link = next_button.find("a").attrs['href']
        page = requests.get(next_page_link, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
