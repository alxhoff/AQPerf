import csv


def write_rankings(rankings, filename):

    with open(filename + ".csv", "w", newline="") as f:

        writer = csv.writer(f)
        writer.writerow(
            [
                "Player",
                "Role",
                "Buffs",
                "Overall Parse",
                "Visc Weps",
                "Visc Oils",
                "Visc NPP",
                "Huhu NPP",
                "% fine",
                "gold fine",
            ]
        )
