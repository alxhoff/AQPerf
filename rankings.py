# -*- coding: utf-8 -*-

from enum import Enum, auto


class FightParse:
    def __init__(self, fight_id, boss_id, boss_name, parse):

        self.fight_id = fight_id
        self.boss_id = boss_id
        self.boss_name = boss_name
        self.parse = parse

    def set_parse(self, parse):

        if parse > self.parse:
            self.parse = parse

    def __str__(self):
        return "{}:{}".format(self.boss_name, self.parse)


class ParseTable:
    def __init__(self):

        self.parses = {}

    def add_parse(self, fight_id, boss_id, boss_name, parse):

        # Visc parse is not counted!
        if boss_id == 713:
            return

        if str(boss_id) not in self.parses:
            self.parses[str(boss_id)] = FightParse(fight_id, boss_id, boss_name, parse)
        else:
            self.parses[str(boss_id)].set_parse(parse)

    def get_parse(self, boss_id):
        self.parses.get(str(boss_id), 0)

    def get_overall_parse(self):
        from math import floor

        tparse = 0
        nparse = 0
        for key, parse in self.parses.items():
            tparse += parse.parse
            nparse += 1

        try:
            return floor(tparse / nparse)
        except Exception:
            return 0

    def __str__(self):
        ret = "[ "
        for key, parse in self.parses.items():
            ret += str(parse) + ", "
        ret += ": {}]".format(self.get_overall_parse())
        return ret


class Buffs:
    def __init__(self):

        self.DMT = False
        self.ZG = False
        self.HOR = False
        self.SF = False
        self.DS = False
        self.DMF = False
        self.buff_count = 0

    def __str__(self):
        return str(self.buff_count)

    def get_buff_count(self):

        buffs = 0
        if self.DMT:
            buffs += 1
        if self.ZG:
            buffs += 1
        if self.HOR:
            buffs += 1
        if self.SF:
            buffs += 1
        if self.DS:
            buffs += 1
        if self.DMF:
            buffs += 1
        self.buff_count = buffs

    def set_buffs(self, artifacts):
        for buff in artifacts:
            guid = buff["guid"]
            if guid == 22817:
                self.DMT = True
            elif guid == 22818:
                self.DMT = True
            elif guid == 22820:
                self.DMT = True
            elif guid == 16609:
                self.HOR = True
            elif guid == 23768:
                self.DMF = True
            elif guid == 23766:
                self.DMF = True
            elif guid == 23737:
                self.DMF = True
            elif guid == 23769:
                self.DMF = True
            elif guid == 23736:
                self.DMF = True
            elif guid == 23738:
                self.DMF = True
            elif guid == 15366:
                self.SF = True
            elif guid == 24425:
                self.ZG = True
            elif guid == 22888:
                self.DS = True
            else:
                print("Unknown BUFF!")
        pass


class ParseType(Enum):
    UNKNOWN = auto()
    HEALS = auto()
    TANK = auto()
    DPS = auto()


class Player:
    def __init__(self, composition):

        try:
            self.name = composition["name"]
        except Exception:
            return None
        self.id = composition["id"]
        self.guid = composition["guid"]
        self.type = composition["type"]
        self.buffs = Buffs()
        self.parses = ParseTable()
        self.parse_type = ParseType.UNKNOWN
        self.visc_weps = True
        self.visc_oils = True
        self.visc_GNPP = False
        self.visc_absorbed = 0
        self.princess_GNPP = False
        self.princess_absorbed = 0
        self.fine_percent = 0
        self.gold_fine = 0

    def add_combatant_info(self, ci):
        if "combatantInfo" in ci:
            if ci["combatantInfo"]:
                if "artifact" in ci["combatantInfo"]:
                    if ci["combatantInfo"]["artifact"]:
                        self.buffs.set_buffs(ci["combatantInfo"]["artifact"])
                        self.buffs.get_buff_count()

    def __str__(self):
        ret = "{} - {} - Buffs: {}, Parses {}, Weps {}, Oils {}, Visc GNPP: {}, Huhu GNPP: {}, Fine %: {}, Fine Gold: {}".format(
            self.name,
            self.type,
            str(self.buffs),
            str(self.parses),
            self.visc_weps,
            self.visc_oils,
            self.visc_GNPP,
            self.princess_GNPP,
            self.fine_percent,
            self.gold_fine,
        )
        return ret


class Roster:
    """
    Describes a raid roster for a given period, eg. fight, raid, first pull etc.
    """

    def __init__(self, composition):

        self.players = {}
        for player in composition:
            if "name" in player:
                self.players[player["name"]] = Player(player)

    def get_name_from_id(self, id):
        for player in self.players.values():
            if player.id == id:
                return player.name
        return None

    def __str__(self):
        ret = "{} raiders\n".format(len(self.players))
        for key, player in self.players.items():
            ret += "{}\n".format(str(player))
        return ret

    def calculate_fines(self):
        for player in self.players.values():

            # Buffs
            if player.buffs.buff_count == 0:
                player.fine_percent = 20
            elif player.buffs.buff_count == 1:
                player.fine_percent = 10

            # Weps
            if not player.visc_weps:
                player.gold_fine += 50
            if not player.visc_oils:
                player.gold_fine += 50

            # NPPs
            if not player.visc_GNPP:
                player.gold_fine += 50
            if not player.princess_GNPP:
                player.gold_fine += 50


class Fight:
    """
    Stores the encounter and boss ids required to pull fight data
    """

    def __init__(self, eid, bid, name, data):

        self.boss_id = bid
        self.encounter_id = eid
        self.name = name
        self.data = data


class Rankings:
    def __init__(self, client, verbose):

        self.client = client
        self.rankings = client.get_rankings()
        self.boss_fights = self.get_boss_fights()

        # Fight zero represents all trash fights and is such used for checking WBs as the first pull is trash, this is
        # the moment where WBs are snapshotted
        self.roster = Roster(self.client.get_raid_composition(0))

        # add parse types
        for player in self.roster.players.values():
            if player.name in [
                n["name"] for n in self.rankings[-1]["roles"]["tanks"]["characters"]
            ]:
                player.parse_type = ParseType.TANK
            elif player.name in [
                n["name"] for n in self.rankings[-1]["roles"]["healers"]["characters"]
            ]:
                player.parse_type = ParseType.HEALS
            elif player.name in [
                n["name"] for n in self.rankings[-1]["roles"]["dps"]["characters"]
            ]:
                player.parse_type = ParseType.DPS

        ci = self.client.get_raid_combatant_info(0)
        for combatant in ci:
            self.roster.players[combatant["name"]].add_combatant_info(combatant)

        for rank in self.rankings:
            fight_id = rank["fightID"]
            boss_id = rank["encounter"]["id"]
            boss_name = rank["encounter"]["name"]
            players = (
                rank["roles"]["tanks"]["characters"]
                + rank["roles"]["healers"]["characters"]
                + rank["roles"]["dps"]["characters"]
            )
            for player in players:
                self.roster.players[player["name"]].parses.add_parse(
                    fight_id, boss_id, boss_name, player["rankPercent"]
                )

        # Fight analytics
        for fight in self.boss_fights:
            if fight.boss_id == 713:  # Visc
                frost_mele_weps = [10761, 19099, 810, 14487, 13984, 5756]
                frost_wands = [13534, 19108, 9489, 19130, 18483, 10704, 16789]
                for combatant in fight.data:
                    name = self.roster.get_name_from_id(combatant["sourceID"])
                    player = self.roster.players[name]

                    if player.parse_type in [ParseType.HEALS, ParseType.TANK]:
                        player.visc_weps = True
                        player.visc_oils = True
                    else:
                        if player.type in ["Rogue", "Warrior", "Hunter"]:
                            mainhand = combatant["gear"][15]["id"]
                            offhand = combatant["gear"][16]["id"]
                            if (not mainhand in frost_mele_weps) or (
                                not offhand in frost_mele_weps
                            ):
                                player.visc_weps = False

                            if (not "temporaryEnchant" in combatant["gear"][15]) or (
                                not "temporaryEnchant" in combatant["gear"][16]
                            ):
                                player.visc_oils = False
                            else:
                                mh_oil = combatant["gear"][15]["temporaryEnchant"]
                                oh_oil = combatant["gear"][16]["temporaryEnchant"]
                                if mh_oil != 26 or oh_oil != 26:
                                    player.visc_oils = False

                        elif player.type in ["Warlock"]:
                            wand = combatant["gear"][17]["id"]

                            if not wand in frost_wands:
                                player.visc_weps = False

                        elif player.type in ["Shaman", "Druid"]:
                            mainhand = combatant["gear"][15]["id"]
                            mh_oil = combatant["gear"][15]["temporaryEnchant"]
                            if not mainhand in frost_mele_weps:
                                player.visc_weps = False
                            if mh_oil != 26:
                                player.visc_oils = False

                    healing_done = self.client.get_healing_done(
                        fight_id=fight.encounter_id, combatant_id=player.id
                    )

                    GNPP_healing = sum(
                        [
                            skill["total"]
                            for skill in healing_done
                            if skill["guid"] in [17546, 7254]
                        ]
                    )

                    if GNPP_healing > 1800:
                        player.visc_absorbed = GNPP_healing
                        player.visc_GNPP = True

            if fight.boss_id == 714:  # Huhuran
                for combatant in fight.data:
                    name = self.roster.get_name_from_id(combatant["sourceID"])
                    player = self.roster.players[name]
                    healing_done = self.client.get_healing_done(
                        fight_id=fight.encounter_id, combatant_id=player.id
                    )
                    GNPP_healing = sum(
                        [
                            skill["total"]
                            for skill in healing_done
                            if skill["guid"] in [17546, 7254]
                        ]
                    )
                    if player.parse_type in [ParseType.HEALS, ParseType.TANK]:
                        player.princess_GNPP = True
                    else:
                        if player.type in ["Rogue", "Warrior"]:
                            if GNPP_healing > 1800:
                                player.visc_GNPP = True
                                player.princess_absorbed = GNPP_healing
                        elif player.type in [
                            "Warlock",
                            "Mage",
                            "Priest",
                            "Shaman",
                            "Druid",
                            "Hunter",
                        ]:
                            player.princess_GNPP = True
        # Fines
        self.roster.calculate_fines()

        if verbose:
            print(self.roster)

    def get_boss_fights(self):
        return [
            Fight(
                fight["fightID"],
                fight["encounter"]["id"],
                fight["encounter"]["name"],
                self.client.get_combatant_fight_data(fight["fightID"]),
            )
            for fight in self.rankings
        ]
