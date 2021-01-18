from v2.client import Client



def main():
    global username, passwd

    client = Client(username, passwd)

    rankings = client.get_rankings()

    print("hello")

if __name__ == "__main__":
    main()
