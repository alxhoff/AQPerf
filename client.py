from transport import v2_oauth_transport


class Client:
    def __init__(self, client_id, client_secret, report_ID):

        self.transport = v2_oauth_transport(client_id, client_secret)
        self.report_ID = report_ID

    def _get_report_field_query(self, field):
        return 'query{{reportData{{report(code:"{}") {{ {} }} }} }}'.format(
            self.report_ID, field
        )

    def _get_report_table_query(self, field):
        log_duration = self._get_duration()
        return 'query{{reportData{{report(code:"{}") {{ table(endTime: {}, {}) }} }} }}'.format(
            self.report_ID, log_duration, field
        )

    def _get_report_table_fight(self, fight):
        query = self._get_report_table_query("fightIDs: [{}]".format(fight))
        ret = self.transport.query(query)["reportData"]["report"]["table"]["data"]
        return ret

    def _get_start_time(self):
        query = self._get_report_field_query("startTime")
        ret = self.transport.query(query)
        return ret["reportData"]["report"]["startTime"]

    def _get_end_time(self):
        query = self._get_report_field_query("endTime")
        ret = self.transport.query(query)
        return ret["reportData"]["report"]["endTime"]

    def _get_duration(self):
        st = self._get_start_time()
        et = self._get_end_time()
        return et - st

    def get_raid_composition(self, fight):
        return self._get_report_table_fight(fight)["composition"]

    def get_raid_combatant_info(self, fight):
        pd = self._get_report_table_fight(fight)["playerDetails"]
        return pd["tanks"] + pd["dps"] + pd["healers"]

    def get_combatant_fight_data(self, fight_id):
        log_duration = self._get_duration()
        query = self._get_report_field_query(
            'events(fightIDs: [{}], endTime: {}, filterExpression: "type = \\"combatantinfo\\""){{data}}'.format(
                fight_id, log_duration
            )
        )
        ret = self.transport.query(query)["reportData"]["report"]["events"]["data"]
        return ret

    def get_ranked_characters(self):
        query = self._get_report_field_query("rankedCharacters")
        ret = self.transport.query(query)
        return ret

    def get_rankings(self):
        query = self._get_report_field_query("rankings")
        return self.transport.query(query)["reportData"]["report"]["rankings"]["data"]
