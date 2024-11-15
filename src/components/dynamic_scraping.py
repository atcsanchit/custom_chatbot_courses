from requests_html import HTMLSession
import sys
import io
import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

url="https://brainlox.com/courses/category/technical"

s = HTMLSession()
r = s.get(url)

r.html.render(sleep=1)

courses = r.html.xpath('//*[@class="row"]',first=True)
name = []
course_desc = []
session_price = []
lesson = []
duration = []
price = []


for links in courses.absolute_links:
    r = s.get(links)
    try:
        name.append(r.html.find("div.page-title-content h2")[0].text)
    except:
        name.append(None)
    
    try:
        course_desc.append(r.html.find("div.courses-overview p")[0].text)
        # course_desc = ''.join(char for char in course_desc.text if unicodedata.category(char) != 'So')
        # print(filtered_text)
    except:
        course_desc.append(None)
    try:
        ul = r.html.find("ul.info",first=True)
        # print(lesson)
        if ul:
            li_items=ul.find("li")
            if li_items[0]:
                session_price.append(int(li_items[0].text[12:14]))
            else:
                session_price.append(None)

            if li_items[1]:
                lesson.append(int(li_items[1].text[7:9]))
            else:
                lesson.append(None)
            
            if li_items[2]:
                duration.append(li_items[2].text[8:])
            else:
                duration.append(None)
            
            if li_items[3]:
                price.append(int(li_items[3].text[6:]))
            else:
                price.append(None)
            
    except:
        session_price.append(None)
        lesson.append(None)
        duration.append(None)
        price.append(None)

    # name=name_element[0].text
    # course_desc=course_descrip_element[0].text
    # price=price_element[0].text

# print(lesson)

df=pd.DataFrame({
    "Name":name,
    "Description":course_desc,
    "Session_Price":session_price,
    "Lessons":lesson,
    "Duration":duration,
    "Price":price
})

print(df)

df.to_csv("Web Scraping\wechatbot.csv")
df.to_excel("Web Scraping\chatbot.xlsx")    
    