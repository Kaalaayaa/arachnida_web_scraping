from bs4 import BeautifulSoup

with open("index.html", "r") as f:
    doc = BeautifulSoup(f, "html.parser")

print(doc.prettify())
tag = doc.title
print(tag) #Print the title tag
print(tag.string)
tag.string = "hello" #print inside the tag
print(tag)
print('\n')
tags= doc.find_all("p")[0] #print(tags) #print the first p tag
print(tags.find_all("b")) #print all the p tags

