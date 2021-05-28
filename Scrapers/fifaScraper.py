import re
from typing import Dict

from bs4 import Tag

from Scrapers.scraper import Scraper
from fifaPlayer import FIFAPlayer, FIFAPlayerStats, FIFAPosition


class FIFAScraper(Scraper):
    '''
    Get Player's data from fifaindex.com\n
    Note: This scraper only works for fifaindex players
    '''
    FIFAINDEX_URL = "https://fifaindex.com"
    PLAYER_STATS = ["Ball Control", "Dribbling", "Crossing", "Short Pass", "Long Pass", "GK Positioning", "GK Diving",
                    "GK Handling", "GK Kicking", "GK Reflexes", "Marking", "Slide Tackle", "Stand Tackle",
                    "Acceleration", "Stamina", "Strength", "Balance", "Sprint Speed", "Agility", "Jumping", "Heading",
                    "Shot Power", "Finishing", "Long Shots", "Curve", "FK Acc.", "Penalties", "Volleys", "Aggression",
                    "Reactions", "Att. Position", "Interceptions", "Vision", "Composure"]

    @staticmethod
    def get_player(input) -> FIFAPlayer:
        '''
        get player object by it's ID or Name
        :param input: Player's name in str or ID in int
        :return: player's object (FIFAPlayer)
        '''
        if type(input) == str:
            url = FIFAScraper.__search_player_url(input)
        elif type(input) == int:
            url = f'https://fifaindex.com/player/{input}/player/'
        else:
            raise Exception(f"Invalid Input: {input}")
        data = FIFAScraper.__scrape(url)
        return FIFAScraper.__data_to_player(data)

    @staticmethod
    def __search_player_url(name: str) -> str:
        '''
        search and return the best found player's page url
        :param name: player's name
        :return: player's fifaindex page url
        '''
        name = name.lower()
        search_url = f'https://www.fifaindex.com/players/?name={name}&order=desc'
        soup = FIFAScraper.get_page_souped(search_url)
        found_players = soup.find('table', class_='table-players').find('tbody').find_all('tr')
        for p in found_players:
            p: Tag
            if 'data-playerid' in p.attrs:
                player_link = FIFAScraper.FIFAINDEX_URL + p.find('a', class_='link-player').attrs['href']
                return player_link

        raise Exception(f"No Player Found!: {name}")

    @staticmethod
    def __scrape(url: str) -> Dict[str, str]:
        '''
        scrape and extract data from the given fifaindex url
        :param url: fifaindex player page url
        :return: scraped data in a dictionary
        '''
        url = url.lower()
        if url.find("fifaindex.com") == -1:
            raise Exception(f"{url} is not a FIFAIndex.com url")
        soup = FIFAScraper.get_page_souped(url)
        scraped_data: Dict[str, str] = {}
        try:
            info_card = soup.find('div', class_='col-lg-8').find('div', class_='card mb-5')
        except Exception:
            raise Exception(f"Player ({url}) was not found!")
        scraped_data['overall'] = info_card.find('h5', class_='card-header').find('span', class_='rating').text.strip()
        scraped_data['name'] = info_card.find('h5', class_='card-header').contents[0].lower().strip()

        nation = soup.find('div', class_='pt-3').find('a', class_='link-nation').attrs['title']
        scraped_data['nationality'] = nation.lower().strip()

        team_cards = soup.find('div', class_='col-lg-8').find_all('div', class_='row')[1] \
            .find_all('div', class_='col-12')
        for card in team_cards:
            team_name = card.find('h5', class_='card-header').text.lower().strip()
            if team_name != scraped_data['nationality']:
                scraped_data['team'] = team_name

        info_card_body = info_card.find('div', class_='card-body').find_all('p')
        info_card_items = ['height', 'weight', 'preferred foot', 'age']
        for info in info_card_body:
            info: Tag
            info_text: str = info.text.lower().strip()

            if info_text.startswith('weak foot'):
                scraped_data['weak foot'] = str(5 - len(info.find_all('i', class_='far')))

            if info_text.startswith('preferred positions'):
                positions = []
                for pos in info.find_all('span', class_='position'):
                    positions.append(pos.text.lower())
                scraped_data['preferred positions'] = ", ".join(positions)

            for item in info_card_items:
                if info_text.startswith(item):
                    scraped_data[item] = info_text[len(item):].strip()

        stats_cards = soup.find('div', class_='col-lg-8').find('div', class_='grid').find_all('div', class_='col-12')
        cards_needed = ['ball skills', 'defence', 'mental', 'passing', 'physical', 'shooting', 'goalkeeper']
        for card in stats_cards:
            card: Tag
            card_name = card.find('h5', class_='card-header').text.lower()
            if not card_name in cards_needed:
                continue
            card_stats = card.find('div', class_='card-body').find_all('p')
            for stat in card_stats:
                stat: Tag
                for player_stat in FIFAScraper.PLAYER_STATS:
                    stat_text = stat.text.lower().strip()
                    if stat_text.find(player_stat.lower()) != -1:
                        stat_num = stat_text[len(player_stat):].strip()
                        scraped_data[player_stat] = stat_num

        return scraped_data

    @staticmethod
    def __data_to_player(scraped_data: Dict[str, str]) -> FIFAPlayer:
        '''
        convert extracted data to player object
        :param scraped_data: scraped data gotten from FIFAPlayer.__scrape (Dict[str, str])
        :return: player's object (FIFAPlayer)
        '''
        name = scraped_data['name']
        age = int(scraped_data['age'])
        foot = scraped_data['preferred foot']
        nation = scraped_data['nationality']
        team = scraped_data['team']
        height = int(re.findall('(\d{3})\s*cm', string=scraped_data['height'])[0])
        weight = int(re.findall('(\d{2,3})\s*kg', string=scraped_data['weight'])[0])
        stats = FIFAScraper.__data_to_stats(scraped_data)
        return FIFAPlayer(name, name, age, 0, foot, height, weight, team, nation, stats)

    @staticmethod
    def __data_to_stats(scraped_data: Dict[str, str]) -> FIFAPlayerStats:
        '''
        convert extracted data to player stats
        :param scraped_data: scraped data gotten from FIFAScraper.__scrape (Dict[str, str])
        :return: player's stats (FIFAPlayerStats)
        '''
        overall = int(scraped_data['overall'])
        stats = FIFAPlayerStats(overall)

        # Find Player Position Enum
        preferred_positions = scraped_data['preferred positions'].split(', ')
        for fifpos in FIFAPosition:
            if preferred_positions[0].find(fifpos.name.lower()) != -1:
                stats.position = fifpos
                break
        pref_poses = []
        for pos in preferred_positions[1:]:
            for fifpos in FIFAPosition:
                if pos.find(fifpos.name.lower()) != -1:
                    pref_poses.append(fifpos)
                    break
        stats.preferred_positions = tuple(pref_poses)

        # Assigning Extracted Stats to PlayerStats Object
        for stat in FIFAScraper.PLAYER_STATS:
            stat_pow = int(scraped_data[stat])
            stats.__dict__[stat.lower().replace(' ', '_').replace('.', '')] = stat_pow

        stats.weak_foot = scraped_data['weak foot']
        return stats


if __name__ == '__main__':
    print(FIFAScraper.get_player("messi").stats.__dict__)
