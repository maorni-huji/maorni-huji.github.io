from Server import server_control
from Client import compete


def main():
    # server_control.server_control()
    compete.upload_opponent_file()
    server_control.server_auto_control()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
