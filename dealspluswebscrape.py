import requests
from bs4 import BeautifulSoup

#TODO make the program so it parses through all data not just most

#finds the number of pages to be searched through
def findNumOfPages(page,url):
    soup = BeautifulSoup(page.content,'html.parser')
    nxt = soup.find('li', class_="next")
    while(nxt != None):
        pageNums = soup.find_all('li',class_="number")
        size = len(pageNums) - 1
        pageNum = pageNums[size].find('a').get_text()       
        newUrl = url + "&page=" + pageNum
        newPage = requests.get(newUrl)
        soup = BeautifulSoup(newPage.content,'html')
        nxt = soup.find('li',class_="next")
    number = soup.find_all('li',class_="number")
    size = len(number) - 1
    strNumber = number[size].find('a').get_text()
    intNumber = int(strNumber)
    intNumber += 1
    return intNumber

def searchForGoodDeals(url,profitMargin,cost):
    page = requests.get(url)
    numOfPages = findNumOfPages(page,url)
    intervals = 0
    titles = []
    while numOfPages >= intervals:
        soup = BeautifulSoup(page.content, 'html.parser')
        middle = soup.find_all('div',class_="itemTileV5")
        
        for i in middle:
            current = i.find(class_="currentPrice").get_text()
            original = i.find(class_="originalPrice").get_text() 
            currentF = 0.0
            #originalF = 0.0
            dif = 0.0
            if current != '' and original != '':
                try:
                    currentF = float(current[1:6])
                    dif = float(original[1:6])-float(current[1:6])
                except:
                    top = i.find(class_="top")
                    href = top.find('a',href=True)
                    print("Incorrect Price Format.Cannot use data. URL:(" + "dealsplus.com" + href['href'] + ')')
                

            if dif > profitMargin and currentF < cost:
                top = i.find(class_="top")
                href = top.find('a',href=True)
                titles.append(i.find(class_="tileDealTitle").get_text() + '\n' +'(' + 'dealsplus.com' + href['href'] + ') ' + "margin: " + str(dif) )
        
        intervals += 1
        newUrl = url + "&page=" + str(intervals)
        page = requests.get(newUrl)
    for i in titles:
            print(i)

searchForGoodDeals("https://www.dealsplus.com/All-Electronics_deals?sort=newest",150,50)