# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


import requests
from bs4 import BeautifulSoup

dicUrl={}
Url=""

def crawl_premier_league_clubs():
    url = "https://www.premierleague.com/clubs"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        club_info = soup.find_all("a", class_="indexItem")
        for item in club_info:
            club_name = item.find("h2", class_="club-card__name").text.strip()
            club_url = "https://www.premierleague.com" + item['href']
            dicUrl[club_name]=club_url
            print("Club:", club_name)
            print("URL:", club_url)
    else:
        print("Failed to retrieve page:", response.status_code)

    print()

    for dic in dicUrl.values():
        strUrl=dic
        UrlSquad=""
        response = requests.get(strUrl)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            club_info = soup.find_all("a", class_="club-navigation__link")
            for item in club_info:
                if item['data-text'] == "Squad":
                    UrlSquad=strUrl.replace("overview", item['href'])
        else:
            print("Failed to retrieve page:", response.status_code)

        response = requests.get(UrlSquad)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            club_info = soup.find_all("a", class_="indexItem")
            for item in club_info:
                club_name = item.find("h2", class_="club-card__name").text.strip()
                club_url = "https://www.premierleague.com" + item['href']
                dicUrl[club_name] = club_url
                print("Club:", club_name)
                print("URL:", club_url)
        else:
            print("Failed to retrieve page:", response.status_code)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    crawl_premier_league_clubs()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
