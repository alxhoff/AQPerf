from v2.client import Client
from v2.rankings import Rankings


def main():
    global username, passwd, report_ID

    client = Client(username, passwd, report_ID)

    duration = client._get_duration()

    rankings = Rankings(client)


if __name__ == "__main__":
    main()
