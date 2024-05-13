import requests
import os
from bs4 import BeautifulSoup

url = "https://www.premierleague.com/clubs"
dicClubUrls={}
dicPlayerUrls = {}
directory="D:/Data_analyst/Data/"

def crawlClubs():
    responseClubs=requests.get(url);
    if responseClubs.status_code == 200:
        soup_club = BeautifulSoup(responseClubs.content, 'html.parser')

        club_info = soup_club.find_all("a", class_="indexItem")
        for item in club_info:
            club_name = item.find("h2", class_="club-card__name").text.strip()
            club_url = "https://www.premierleague.com" + item['href']
            dicClubUrls[club_name]=club_url
            print("Club:", club_name)
            print("URL:", club_url)
            club_directory=directory+club_name
            # Kiểm tra xem thư mục đã tồn tại chưa
            if not os.path.exists(club_directory):
                # Tạo thư mục mới
                os.makedirs(club_directory)
                print("Thư mục đã được tạo thành công!")
            else:
                print("Thư mục đã tồn tại.")
            crawlPositions(club_name,club_url,club_directory)
    else:
        print("Failed to retrieve page:", responseClubs.status_code)

def crawlPositions(positionName,urlPosition,positionDirectory):
    responseSquad=requests.get(urlPosition)
    UrlSquad = ""
    if responseSquad.status_code == 200:
        soup_squad = BeautifulSoup(responseSquad.content, 'html.parser')
        club_info = soup_squad.find_all("a", class_="club-navigation__link")
        for item in club_info:
            if item['data-text'] == "Squad":
                UrlSquad = urlPosition.replace("overview", item['href'])
    else:
        print("Failed to retrieve page:", responseSquad.status_code)
    responsePosition = requests.get(UrlSquad)
    dicPositonPlayers = []
    if responsePosition.status_code == 200:
        soup = BeautifulSoup(responsePosition.content, 'html.parser')
        position_players = soup.find_all("div", class_="squad-list__position-container")
        for item in position_players:
            position_player = ""
            dicPlayerUrlsByPosition = {}
            if item.find("h1", class_="squad-list__position-header u-hide-mob-l"):
                position_player = item.find("h1", class_="squad-list__position-header u-hide-mob-l").text.strip()
                dicPositonPlayers.append(position_player)
                player_directory=positionDirectory+"/"+position_player
                # Kiểm tra xem thư mục đã tồn tại chưa
                if not os.path.exists(player_directory):
                    # Tạo thư mục mới
                    os.makedirs(player_directory)
                    print("Thư mục đã được tạo thành công!")
                else:
                    print("Thư mục đã tồn tại.")
            PlayerUrlsByPosition = soup.find_all("li", class_="stats-card")
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
                    crawlInfoPlayer(player_name,player_url,player_directory)
    else:
        print("Failed to retrieve page:", responsePosition.status_code)

def crawlInfoPlayer(playerName,playerUrl,playerDirectory):
    responseInfoPlayer = requests.get(playerUrl)
    if responseInfoPlayer.status_code == 200:
        soup_info_player = BeautifulSoup(responseInfoPlayer.content, 'html.parser')
        infor_player = soup_info_player.find_all("a", "generic-tabs-nav__link")
        for item in infor_player:
            overview_stats = playerUrl.replace("overview", "").replace("stats", "") + item['href']
            if(item['href']=="overview"):
                responseInfoOverViewPlayer = requests.get(overview_stats)
                if responseInfoOverViewPlayer.status_code == 200:
                    soup_info_player_overview = BeautifulSoup(responseInfoPlayer.content, 'html.parser')
                    infor_player_overview = soup_info_player_overview.find_all("div", "player-overview__col")
                    for item in infor_player_overview:
                        # Tìm nhãn và thông tin bên trong thẻ div
                        label = item.find(class_='player-overview__label').text.strip()
                        info = item.find(class_='player-overview__info').text.strip()
                        # kiểm tra thẻ span
                        spans=item.find_all("span",class_=lambda x: x and 'player-overview_' in x)
                        if spans.count()>0:
                            info=spans[0].text.strip()
                        print(label)
                        print(info)
                else:
                    print("Failed to retrieve page:", responseInfoOverViewPlayer.status_code)

            else:
                responseInfoStatsPlayer = requests.get(overview_stats)
                if responseInfoStatsPlayer.status_code == 200:
                    soup_info_player_stats = BeautifulSoup(responseInfoPlayer.content, 'html.parser')
                    infor_player_stats = soup_info_player_stats.find_all("a", "player-stats__stat-value")
                    for item in infor_player_stats:
                        # Tìm nhãn và thông tin bên trong thẻ div
                        title = item.text.strip().split('\n')[0]
                        content = item.span.text.strip()
                        print(title)
                        print(content)
                else:
                    print("Failed to retrieve page:", responseInfoStatsPlayer.status_code)

    else:
        print("Failed to retrieve page:", responseInfoPlayer.status_code)
if __name__ == '__main__':
    crawlClubs()