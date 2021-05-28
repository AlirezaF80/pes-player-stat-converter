from Scrapers.fifaScraper import FIFAScraper
from fifaPlayer import FIFAPlayer, FIFAPlayerStats, FIFAPosition
from pesPlayer import PESPlayer, PESPlayerStats, PESPosition


class FIFAToPESConverter:
    @staticmethod
    def convert_player(fifa_player: FIFAPlayer) -> PESPlayer:
        '''
        convert fifa player data to pes
        :param fifa_player: fifa player object
        :return: pes player object (PESPlayer)
        '''
        converted_stats = FIFAToPESConverter.__convert_stats(fifa_player.stats)
        pes_player = PESPlayer(fifa_player.name, fifa_player.full_name, fifa_player.age, fifa_player.ID,
                               fifa_player.foot, fifa_player.height, fifa_player.weight, fifa_player.team,
                               fifa_player.nationality, converted_stats)
        return pes_player

    FIFA_POS_PES_EQUIV = {FIFAPosition.GK: PESPosition.GK, FIFAPosition.LB: PESPosition.LB,
                          FIFAPosition.LCB: PESPosition.CB, FIFAPosition.CB: PESPosition.CB,
                          FIFAPosition.RCB: PESPosition.CB, FIFAPosition.RB: PESPosition.RB,
                          FIFAPosition.LWB: PESPosition.LB, FIFAPosition.LDM: PESPosition.DMF,
                          FIFAPosition.CDM: PESPosition.DMF, FIFAPosition.RDM: PESPosition.DMF,
                          FIFAPosition.RWB: PESPosition.RB, FIFAPosition.LM: PESPosition.LMF,
                          FIFAPosition.LCM: PESPosition.CMF, FIFAPosition.CMF: PESPosition.CMF,
                          FIFAPosition.RCM: PESPosition.CMF, FIFAPosition.RM: PESPosition.RMF,
                          FIFAPosition.LAM: PESPosition.AMF, FIFAPosition.CAM: PESPosition.AMF,
                          FIFAPosition.RAM: PESPosition.AMF, FIFAPosition.LW: PESPosition.LWF,
                          FIFAPosition.LF: PESPosition.SS, FIFAPosition.CF: PESPosition.SS,
                          FIFAPosition.RF: PESPosition.SS, FIFAPosition.RW: PESPosition.RWF,
                          FIFAPosition.LS: PESPosition.CF, FIFAPosition.ST: PESPosition.CF,
                          FIFAPosition.RS: PESPosition.CF}
    PES_FIFA_STAT_DICT = {"ball_control": "ball_control", "dribbling": "dribbling", "tight_possession": "agility",
                          "low_pass": "short_pass", "finishing": "finishing", "heading": "heading", "jump": "jumping",
                          "curl": "curve", "speed": "sprint_speed", "acceleration": "acceleration",
                          "stamina": "stamina", "kicking_power": "shot_power", "balance": "balance",
                          "aggression": "aggression", "gk_catching": "gk_handling", "gk_reflexes": "gk_reflexes",
                          "weak_foot_usage": "weak_foot", "weak_foot_acc": "weak_foot", "physical_contact": "strength"}
    PES_FIFA_STAT_MIX_DICT = {"lofted_pass": ["long_pass", "crossing"], "defensive_awareness": ["marking", "reactions"],
                              "ball_winning": ["slide_tackle", "stand_tackle", "interceptions"],
                              "gk_awareness": ["gk_positioning", "gk_reflexes"],
                              "place_kicking": ["fk_acc", "penalties"], "gk_reach": ["gk_positioning", "gk_diving"],
                              "offensive_awareness": ["att_position", "vision"]}
    PES_FIFA_GK_DICT = {"lofted_pass": ["gk_kicking", "long_pass"], "kicking_power": ["shot_power", "gk_kicking"]}

    @staticmethod
    def __convert_stats(fifa_player_stats: FIFAPlayerStats) -> PESPlayerStats:
        '''
        convert fifa player stats to pes
        :param fifa_player_stats: fifa player stats object
        :return: pes player stats object (PESPlayerStats)
        '''
        pes_player_stat = PESPlayerStats(fifa_player_stats.overall)
        # Positions
        pes_player_stat.position = FIFAToPESConverter.FIFA_POS_PES_EQUIV[fifa_player_stats.position]
        other_pos = []
        for pref_pos in fifa_player_stats.preferred_positions:
            other_pos.append(FIFAToPESConverter.FIFA_POS_PES_EQUIV[pref_pos])
        pes_player_stat.other_positions = tuple(other_pos)
        # Abilities with Equivalent Factors
        for pes_stat, fifa_stat in FIFAToPESConverter.PES_FIFA_STAT_DICT.items():
            pes_player_stat.__dict__[pes_stat] = fifa_player_stats.__dict__[fifa_stat]

        # Abilities with Multiple factors
        for pes_stat, fifa_stats in FIFAToPESConverter.PES_FIFA_STAT_MIX_DICT.items():
            stats_sum = 0
            for fifa_stat in fifa_stats:
                stats_sum += fifa_player_stats.__dict__[fifa_stat]
            pes_player_stat.__dict__[pes_stat] = stats_sum // len(fifa_stats)

        # If player is GK
        if fifa_player_stats.position == FIFAPosition.GK:
            for pes_stat, fifa_stats in FIFAToPESConverter.PES_FIFA_GK_DICT.items():
                stats_sum = 0
                for fifa_stat in fifa_stats:
                    stats_sum += fifa_player_stats.__dict__[fifa_stat]
                pes_player_stat.__dict__[pes_stat] = stats_sum // len(fifa_stats)

        # Setting abilities minimum to 40
        for stat, pow in pes_player_stat.__dict__.items():
            if type(pow) == int:
                pes_player_stat.__dict__[stat] = max(pes_player_stat.__dict__[stat], 40)
        return pes_player_stat


if __name__ == '__main__':
    print(FIFAToPESConverter.convert_player(FIFAScraper.get_player('messi')).stats.__dict__)
