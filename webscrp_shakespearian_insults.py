import requests
from bs4 import BeautifulSoup

page = requests.get("https://www.nosweatshakespeare.com/resources/shakespeare-insults/")
soup = BeautifulSoup(page.content, 'html.parser')

s = soup.find_all('h3')

insult_collection = []
insult_collection_refined = []


for insults in s:
    insult_collection.append(insults)
    if(len(insult_collection)==51):
        break
# print(type(str(insult_collection[0])))
for i in range(51):
    refined_insult = str(insult_collection[i])
    index_1 = refined_insult.index("“")
    refined_insult = refined_insult[index_1+1:len(refined_insult)-6]

