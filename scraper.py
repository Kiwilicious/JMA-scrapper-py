from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import json

baseURL = "http://www.data.jma.go.jp/obd/stats/etrn/select/prefecture00.php?prec_no=&block_no=&year=&month=&day=&view=a1"
dataLinkText = "観測開始からの月ごとの値を表示"


def getAllPrefs(URL):
    content = urllib.request.urlopen(URL)
    soup = BeautifulSoup(content, features="html.parser")
    prefectures = {}

    for pref in soup.findAll('area', attrs={"shape": "rect"}):
        prefName = pref["alt"]
        prefLink = urllib.parse.urljoin(URL, pref["href"])
        prefectures[prefName] = prefLink

    return prefectures


def getAllPrefCities(prefURL):
    content = urllib.request.urlopen(prefURL)
    soup = BeautifulSoup(content, features="html.parser")
    cities = {}

    for city in soup.findAll("area", attrs={"shape": "rect"}):
        cityName = city["alt"]
        cityLink = urllib.parse.urljoin(prefURL, city["href"])
        cities[cityName] = cityLink

    return cities


def getTempDataLink(cityURL):
    content = urllib.request.urlopen(cityURL)
    soup = BeautifulSoup(content, features="html.parser")

    for anchor in soup.findAll("a"):
        if anchor.text.strip() == dataLinkText:
            return urllib.parse.urljoin(cityURL, anchor["href"])


def getCityTemps(dataURL):
    content = urllib.request.urlopen(dataURL)
    soup = BeautifulSoup(content, features="html.parser")
    tempsByYear = {}

    for tr in soup.findAll('tr', attrs={"class": "mtx"}):
        year = tr.find('a').text.strip()
        tempsByMonth = []

        for td in tr.findAll(
                'td', attrs={'class': ['data_0_0_0_0', 'data_1t_0_0_0', 'data_1t_0_0_1l']}):
            temp = td.text.strip()
            if temp != '':
                temp = temp.split()[0]
            if temp == "×":
                temp = ""
            tempsByMonth.append(temp)

        tempsByYear[year] = tempsByMonth

    return tempsByYear


def outputDataAsJSON(data):
    with open("data.json", 'w', encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)


def main():
    prefectureData = {}
    prefectures = getAllPrefs(baseURL)

    for prefName, prefLink in prefectures.items():
        cityData = {}
        cities = getAllPrefCities(prefLink)
        print(f"On {prefName}")

        for cityName, cityLink in cities.items():
            tempDataLink = getTempDataLink(cityLink)

            if tempDataLink is not None:
                cityTemps = getCityTemps(tempDataLink)
                cityData[cityName] = cityTemps

        prefectureData[prefName] = cityData

    outputDataAsJSON(prefectureData)


main()
