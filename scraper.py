from bs4 import BeautifulSoup
import urllib.request
import json

prefURL = "http://www.data.jma.go.jp/obd/stats/etrn/index.php?prec_no=44&block_no=47662&year=&month=&day=&view="
dataURL = "http://www.data.jma.go.jp/obd/stats/etrn/view/monthly_s3.php?prec_no=44&block_no=47662&year=&month=&day=&view="

prefContent = urllib.request.urlopen(prefURL)
soup = BeautifulSoup(prefContent, features="html.parser")
data = {}

prefCityCombo = soup.find('span', attrs={
    "class": "selected", "style": "font-weight:bold;padding-left:1em;padding-right:1em"}).text.strip()
[pref, city] = prefCityCombo.split()
data["pref"] = pref
data["city"] = city


def getCityTemps(dataURL):
    content = urllib.request.urlopen(dataURL)
    soup = BeautifulSoup(content, features="html.parser")
    tempsByYear = {}

    for tr in soup.findAll('tr', attrs={"class": "mtx"}):
        year = tr.find('a').text.strip()
        tempsByMonth = []

        for td in tr.findAll('td', attrs={'class': 'data_0_0_0_0'}):
            temp = td.text.strip()
            if temp != '':
                temp = temp.split()[0]
            tempsByMonth.append(temp)

        tempsByYear[year] = tempsByMonth

    return tempsByYear


def outputDataAsJSON(data):
    with open("data.json", 'w', encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)


def main():
    data = getCityTemps(dataURL)
    outputDataAsJSON(data)


main()
