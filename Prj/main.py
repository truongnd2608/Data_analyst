import requests
from bs4 import BeautifulSoup

def crawl_premier_league_clubs():
    url = "https://www.premierleague.com/clubs"

    response = requests.get(url)
    dicClubUrls = {}
    if response.status_code == 200:
        soup_club = BeautifulSoup(response.content, 'html.parser')

        club_info = soup_club.find_all("a", class_="indexItem")
        for item in club_info:
            club_name = item.find("h2", class_="club-card__name").text.strip()
            club_url = "https://www.premierleague.com" + item['href']
            dicClubUrls[club_name]=club_url
            print("Club:", club_name)
            print("URL:", club_url)
    else:
        print("Failed to retrieve page:", response.status_code)


    for dicClubUrl in dicClubUrls.values():
        strUrl=dicClubUrl
        UrlSquad=""
        response = requests.get(strUrl)
        if response.status_code == 200:
            soup_squad = BeautifulSoup(response.content, 'html.parser')
            club_info = soup_squad.find_all("a", class_="club-navigation__link")
            for item in club_info:
                if item['data-text'] == "Squad":
                    UrlSquad=strUrl.replace("overview", item['href'])
        else:
            print("Failed to retrieve page:", response.status_code)

        response = requests.get(UrlSquad)
        dicPlayerUrls={}
        dicPositonPlayers=[]
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            position_players=soup.find_all("div", class_="squad-list__position-container")
            for item in position_players:
                position_player=""
                dicPlayerUrlsByPosition = {}
                if item.find("h1", class_="squad-list__position-header u-hide-mob-l"):
                    position_player=item.find("h1", class_="squad-list__position-header u-hide-mob-l").text.strip()
                    dicPositonPlayers.append(position_player)
                PlayerUrlsByPosition=soup.find_all("li", class_="stats-card")
                for item in PlayerUrlsByPosition:
                    club_info = soup.find_all("a", class_="stats-card__wrapper")
                    for item in club_info:
                        player_name = ""
                        if item.find("div", class_="stats-card__player-first"):
                            player_name = item.find("div", class_="stats-card__player-first").text.strip()
                        if item.find("div", class_="stats-card__player-last"):
                            if (not player_name.strip()):
                                player_name = item.find("div", class_="stats-card__player-last").text.strip()
                            else:
                                player_name = player_name + " " + item.find("div",
                                                                            class_="stats-card__player-last").text.strip()

                        player_url = "https://www.premierleague.com" + item['href']
                        dicPlayerUrls[player_name] = player_url
                        print("Player Name:", player_name)
                        print("Player URL:", player_url)
        else:
            print("Failed to retrieve page:", response.status_code)

        dicInfoPlayers={}
        for dicPlayerUrl in dicPlayerUrls.values():
            strPlayerUrl = dicPlayerUrl
            response = requests.get(strPlayerUrl)
            if response.status_code == 200:
                soup_info_player = BeautifulSoup(response.content, 'html.parser')
                infor_player=soup_info_player.find_all("a","generic-tabs-nav__link")
                for item in infor_player:
                    overview_stats=strPlayerUrl.replace("overview","").replace("stats","")+item['href']
            else:
                print("Failed to retrieve page:", response.status_code)


if __name__ == '__main__':
    crawl_premier_league_clubs()

