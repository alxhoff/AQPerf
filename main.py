from client import Client
from rankings import Rankings


def main():
    global username, passwd, report_ID

    client = Client(username, passwd, report_ID)

    rankings = Rankings(client)


if __name__ == "__main__":
    main()
