from bs4 import BeautifulSoup

with open("/Users/shivam/Desktop/Sleepyheads/index.html", "r") as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

body_content = soup.body
print(body_content)

new_soup = BeautifulSoup(str(body_content), 'html.parser')

with open("/Users/shivam/Desktop/Sleepyheads/indivaani-backend/out/out.html", "w") as outfile:
    outfile.write(str(new_soup))
