from typing import Dict

from bs4 import Tag

from Scrapers.scraper import Scraper
from pesPlayer import PESPlayer, PESPlayerStats, PESPosition


class PESScraper(Scraper):
    '''
    Get Player's data from PESMaster.com\n
    Note: This scraper only works for PES 2021 players
    '''
    PESMASTER_URL = "https://pesmaster.com"
    PLAYER_STATS = ["offensive_awareness", "ball_control", "dribbling", "tight_possession", "low_pass",
                    "lofted_pass", "finishing", "heading", "place_kicking", "curl", "speed", "acceleration",
                    "kicking_power", "jump", "physical_contact", "balance", "stamina", "defensive_awareness",
                    "ball_winning", "aggression", "gk_awareness", "gk_catching", "gk_clearing", "gk_reflexes",
                    "gk_reach", "weak_foot_usage", "weak_foot_acc", "form", "injury_resistance"]

    @staticmethod
    def get_player(input) -> PESPlayer:
        '''
        get player object by it's ID or Name
        :param input: Player's name in str or ID in int
        :return: player's object (PESPlayer)
        '''
        if type(input) == str:
            url = PESScraper.__search_player_url(input)
        elif type(input) == int:
            url = f'https://www.pesmaster.com/l-messi/pes-2021/player/{input}/'
        else:
            raise Exception(f"Invalid Input: {input}")
        data = PESScraper.__scrape(url)
        return PESScraper.__data_to_player(data)

    @staticmethod
    def __search_player_url(name: str) -> str:
        '''
        find the player's pesmaster page url
        :param name: player's name
        :return: player's pesmaster page url
        '''
        name = name.lower()
        search_url = f'https://www.pesmaster.com/pes-2021/?q={name}'
        soup = PESScraper.get_page_souped(search_url)
        try:
            found_players = soup.find('div', class_='player-card-container').find_all('figure', class_='player-card')
        except:
            raise Exception(f"No Player Found!: {name}")

        # Find and return the first default found player
        for i in found_players:
            i: Tag
            if not i:
                continue
            # If player card is an event card or other things
            if 'player-card-large' in i.attrs['class']:
                continue
            # If player card is a default one
            for content in i.contents:
                content: Tag
                if content.name == 'a':
                    return PESScraper.PESMASTER_URL + content.attrs['href']

    @staticmethod
    def __scrape(url: str) -> Dict[str, str]:
        '''
        scrape and extract data from the given pesmaster url
        :param url: pesmaster PES2021 player page url
        :return: scraped data in a dictionary
        '''
        url = url.lower()
        if url.find("pesmaster.com") == -1:
            raise Exception(f"{url} is not a PESMaster.com url")
        soup = PESScraper.get_page_souped(url)
        scraped_data: Dict[str, str] = {}
        try:
            name_overall = soup.find('h1', class_='top-header').text.strip().split('\n')
        except Exception:
            raise Exception(f"Player ({url}) was not found!")
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

        for stat in PESScraper.PLAYER_STATS:
            stat_pow = soup.find('span', class_=stat).text.strip()
            scraped_data[stat] = stat_pow
        return scraped_data

    @staticmethod
    def __data_to_player(scraped_data: Dict[str, str]) -> PESPlayer:
        '''
        convert extracted data to player object
        :param scraped_data: scraped data gotten from PESScraper.__scrape (Dict[str, str])
        :return: player's object (PESPlayer)
        '''
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

        stats = PESScraper.__data_to_stats(scraped_data)
        return PESPlayer(name, full_name, age, ID, foot, height, weight, team, nation, stats)

    @staticmethod
    def __data_to_stats(scraped_data: Dict[str, str]) -> PESPlayerStats:
        '''
        convert extracted data to player stats
        :param scraped_data: scraped data gotten from PESScraper.__scrape (Dict[str, str])
        :return: player's stats (PESPlayerStats)
        '''
        overall = int(scraped_data['overall'])
        stats = PESPlayerStats(overall)

        # Find Player Position Enum
        for position in PESPosition:
            if scraped_data['position'].find(position.name.lower()) != -1:
                stats.position = position
                break

        # Assigning Extracted Stats to PlayerStats Object
        for stat in PESScraper.PLAYER_STATS:
            stat_pow = int(scraped_data[stat])
            stats.__dict__[stat] = stat_pow

        return stats


if __name__ == '__main__':
    print(PESScraper.get_player(7511))
