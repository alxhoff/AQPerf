#!/usr/bin/env python

from client import Client
from rankings import Rankings
from writer import write_rankings
import argparse


def main():

    try:
        f = open("auth.txt")
        auth_id = f.readline().rstrip()
        auth_secret = f.readline().rstrip()
    except IOError:
        print(
            "auth.txt doesn't exist. Please place client ID and secret into a file named 'auth.txt' with the ID on the first line and the secret on the second."
        )
    finally:
        f.close()

    filename = "results"

    parser = argparse.ArgumentParser(
        description="Basic AQ parse performance for GDKP splits"
    )
    parser.add_argument(
        "-r",
        "--report",
        required=True,
        type=str,
        help="Warcraftlogs report ID to be analyzed",
    )
    parser.add_argument(
        "-f",
        "--filename",
        required=False,
        type=str,
        help="Filename in which the results should be stored",
    )
    parser.add_argument(
        "-s", "--split", required=True, type=int, help="100% split value"
    )
    parser.add_argument(
        "-b",
        "--brackets",
        action="append",
        help="Three integers specifying the dps parse " "brackets",
    )
    parser.add_argument("-he", "--healers", type=int, help="Healer bracket cutoff")
    parser.add_argument("-v", "--verbose", required=False, action="store_true")
    parser.add_argument("-vi", "--visc", required=False, action="store_true")
    args = parser.parse_args()

    client = Client(auth_id, auth_secret, args.report)
    if args.filename:
        filename = args.filename

    rankings = Rankings(client, args.verbose, args.brackets, args.healers, args.visc)

    write_rankings(rankings, args.split, filename)


if __name__ == "__main__":
    main()
