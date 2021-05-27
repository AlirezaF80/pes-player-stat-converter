from typing import Dict

from bs4 import Tag

from pesPlayer import PESPlayer, PESPlayerStats
from scraper import Scraper


class pesScraper(Scraper):
    PESMASTER_URL = "https://pesmaster.com"
    PLAYER_STATS = ["offensive_awareness", "ball_control", "dribbling", "tight_possession", "low_pass",
                    "lofted_pass", "finishing", "heading", "place_kicking", "curl", "speed", "acceleration",
                    "kicking_power", "jump", "physical_contact", "balance", "stamina", "defensive_awareness",
                    "ball_winning", "aggression", "gk_awareness", "gk_catching", "gk_clearing", "gk_reflexes",
                    "gk_reach", "weak_foot_usage", "weak_foot_acc", "form", "injury_resistance"]

    @staticmethod
    def get_player_by_ID(ID: int) -> PESPlayer:
        url = f'https://www.pesmaster.com/l-messi/pes-2021/player/{ID}/'
        data = pesScraper.__scrape(url)
        return pesScraper.__data_to_player(data)

    @staticmethod
    def get_player_by_name(name: str) -> PESPlayer:
        url = pesScraper.__find_player_url(name)
        data = pesScraper.__scrape(url)
        return pesScraper.__data_to_player(data)

    @staticmethod
    def __find_player_url(name: str) -> str:
        name = name.lower()
        search_url = f'https://www.pesmaster.com/pes-2021/?q={name}'
        soup = pesScraper.get_page_souped(search_url)
        found_players = soup.find('div', class_='player-card-container').find_all('figure', class_='player-card')
        for i in found_players:
            i: Tag
            if not i:
                continue
            if 'player-card-large' in i.attrs['class']:
                continue
            for content in i.contents:
                content: Tag
                if content.name == 'a':
                    return pesScraper.PESMASTER_URL + content.attrs['href']

    @staticmethod
    def __scrape(url: str):
        url = url.lower()
        if url.find("pesmaster.com") == -1:
            raise Exception(f"{url} is not a PESMaster.com url")
        soup = pesScraper.get_page_souped(url)
        scraped_data: Dict[str, str] = {}
        name_overall = soup.find('h1', class_='top-header').text.strip().split('\n')
        scraped_data['overall'] = name_overall[0]
        scraped_data['name'] = name_overall[1].lower()

        player_info_table = soup.find('table', class_='player-info').find_all('tr')
        info_table_items = ['full name', 'nationality', 'team', 'position', 'age',
                            'stronger foot', 'height', 'weight', 'id']
        for tr in player_info_table:
            tr_info: str = tr.text.strip().replace('\n', ' ').lower()
            for item in info_table_items:
                if tr_info.startswith(item):
                    tr_info = tr_info[len(item):].strip()
                    scraped_data[item] = tr_info

        for stat in pesScraper.PLAYER_STATS:
            stat_pow = soup.find('span', class_=stat).text.strip()
            scraped_data[stat] = stat_pow
        return scraped_data

    @staticmethod
    def __data_to_player(scraped_data: Dict[str, str]) -> PESPlayer:
        name = scraped_data['name']
        ID = int(scraped_data['id'])
        if 'full name' in scraped_data:
            full_name = scraped_data['full name']
        else:
            full_name = name
        nation = scraped_data['nationality']
        team = scraped_data['team']
        age = int(scraped_data['age'])
        foot = scraped_data['stronger foot']
        weight = int(scraped_data['weight'])
        height = int(scraped_data['height'][len('(cm) '):])

        stats = pesScraper.__data_to_stats(scraped_data)
        return PESPlayer(name, full_name, age, ID, foot, height, weight, team, nation, stats)

    @staticmethod
    def __data_to_stats(scraped_data: Dict[str, str]) -> PESPlayerStats:
        overall = int(scraped_data['overall'])
        stats = PESPlayerStats(overall)

        for stat in pesScraper.PLAYER_STATS:
            stat_pow = int(scraped_data[stat])
            stats.__dict__[stat] = stat_pow
        return stats


if __name__ == '__main__':
    print(pesScraper.get_player_by_name("Kylian Mbappé").__dict__)
