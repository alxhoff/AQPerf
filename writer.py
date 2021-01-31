import csv


def write_rankings(rankings, split, filename):

    with open(filename + ".csv", "w", newline="") as f:

        writer = csv.writer(f)
        writer.writerow(
            [
                "Player",
                "Role",
                "Buffs",
                "Visc Weps",
                "Visc Oils",
                "Visc NPP",
                "Visc Absorbed",
                "Huhu NPP",
                "Huhu Absorbed",
                "Overall Parse",
                "Parse Multiplier",
                "Fine Multiplier",
                "Gold Fine",
                "Split",
                "Bonuses",
                "Total",
                "Recv",
            ]
        )

        for player in rankings.roster.players.values():
            writer.writerow(
                [
                    player.name,
                    player.type,
                    player.buffs.buff_count,
                    player.visc_weps,
                    player.visc_oils,
                    player.visc_GNPP,
                    player.visc_absorbed,
                    player.princess_GNPP,
                    player.princess_absorbed,
                    player.parses.total_parse,
                    player.parse_multiplier,
                    player.fine_percent,
                    player.gold_fine,
                    "=FLOOR({}*{}*{}-{})".format(
                        split,
                        player.parse_multiplier,
                        player.fine_percent,
                        player.gold_fine,
                    ),
                ]
            )
