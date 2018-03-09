import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import csv

NUMBEROFPAGE=10
url="http://jieshaowang.com/jobs/restaurant/"


def pageList(url):
	html = requests.get(url).text
	detailPageLink = []
	soup = BeautifulSoup(html, 'html.parser')
	for link in soup.find_all('h3'):
		detailPageLink.append(link.a["href"].split("/")[3])
	detailPageCompleteLink = []
	for link in detailPageLink:
		detailPageCompleteLink.append("http://jieshaowang.com/jobs/"+link)
	return detailPageCompleteLink

#infourl=detailLinkList[0]

def singleInformation(url):
	html = requests.get(url).text
	soup = BeautifulSoup(html, 'html.parser')
	liList = []
	for link in soup.find_all('ul',attrs={'class':'details'}):
		liList.append(link.find_all('li'))
	position = liList[0][2].get_text().split(":")[1]
	remark = liList[0][9].get_text().split(":")[1]
	state = liList[1][0].get_text().split(":")[1]
	number = liList[1][1].get_text().split(":")[1].strip()
	return [position,remark,state,number]


urlList = []
for i in range(1,NUMBEROFPAGE+1):
	urlList.append("http://jieshaowang.com/jobs/restaurant/"+str(i)+".html")


with open('jieshaowang.csv', 'a', newline='',encoding='utf-8') as csvfile:
	spamwriter = csv.writer(csvfile)
	for url in tqdm(urlList):
		detailLinkList = pageList(url)
		for infourl in tqdm(detailLinkList):
			spamwriter.writerow(singleInformation(infourl))