from client import Raid

key = "32f59249f7b1ef3e5c67bb064e03bbfc"
fid = "C1dRfApW8Prm7kGX"


def main():
    global key, fid
    API_key = key
    encounter_ID = fid
    # API_key = input("Warcraft logs API key: ")
    # encounter_ID = input("Encounter ID: ")

    client = Raid(api_key=API_key, encounter_id=encounter_ID)

    print("hello")


if __name__ == "__main__":
    main()
