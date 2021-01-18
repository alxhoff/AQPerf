from requests import Session
from urllib import parse


class Player:
    def __init__(self, player):
        self.name = player.get("name")
        self.id = player.get("id")
        self.guid = player.get("guid")
        self.type = player.get("type")

    def print(self):

        print("{} - {}".format(self.name, self.type))


class Boss:
    def __init__(self, name, id):

        self.name = name
        self.id = id


class Encounter:
    def __init__(self, fight):

        self.boss_ascii = fight.get("name")
        self.boss_id = fight.get("boss")
        self.start_time = fight.get("start_time")
        self.end_time = fight.get("end_time")
        self.raider_count = fight.get("size")
        self.fight_id = fight.get("id")
        self.kill = fight.get("kill")


class Raid:
    def __init__(self, api_key, encounter_id):

        self.client = AQPerfClient(api_key, encounter_id)

        fights = self.client.get_fights()
        self.first_fight = None
        if fights:
            self.first_fight = fights[0]
        self.boss_fights = self.client.get_boss_fights()

        for boss in self.boss_fights:
            print("{} - {} -> {}".format(boss.boss_ascii, boss.start_time, boss.end_time))


        summary = self.client.get_summary(self.first_fight)
        composition = summary.get("composition")
        self.player_count = len(composition)
        self.players = []
        for player in composition:
            self.players.append(Player(player))

        self.print_summary()

    def print_summary(self):

        print("{} Raiders".format(self.player_count))
        for player in self.players:
            player.print()


class AQPerfClient:
    HOST = "https://classic.warcraftlogs.com/v1/"

    def __init__(self, api_key, encounter_id):

        self.api_key = api_key
        self.encounter_id = encounter_id
        self.session = Session()

        self._get()

    def _api_get(self, path, **kwargs):
        params = {"api_key": self.api_key}
        params.update(kwargs)

        url = parse.urljoin(self.HOST, path)

        data = self.session.get(url, params=params)
        return data.json()

    def _get(self):
        url = "https://classic.warcraftlogs.com/reports/C1dRfApW8Prm7kGX#boss=-2&difficulty=0&wipes=2&playermetriccompare=rankings"

        data = self.session.get(url)

        data = data.json()

        print("hello")

    def get_zones(self):
        return self._api_get("zones")

    def get_zone(self, zone):
        ret = [z for z in self.get_zones() if z["name"] == zone]
        return ret

    def get_boss_fights(self):
        data = self._api_get("report/fights/{}".format(self.encounter_id))
        return [Encounter(fight) for fight in data["fights"] if fight["boss"] != 0]

    def get_fights(self):
        data = self._api_get("report/fights/{}".format(self.encounter_id))
        return [Encounter(fight) for fight in data["fights"]]

    def get_event(self, event):
        return self._api_get("report/events/{}/{}".format(event, self.encounter_id))

    def _get_report_table(self, table, fight):
        args = {"start": fight.start_time, "end": fight.end_time, "wipes": 0}
        path = "report/tables/{}/{}".format(table, self.encounter_id)
        return self._api_get(path, **args)

    def get_damage_done(self, fight):
        return self._get_report_table("damage-done", fight)

    def get_summary(self, fight):
        return self._get_report_table("summary", fight)

    def get_dispels(self):
        return self._get_event("dispels")
