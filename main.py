import csv
import sys
import os


def competition_table(participants_table):
    pass


def read_participants_table(file_name):
    pass


def make_file_name():
    file_name = "participants.csv"
    if len(sys.argv) >= 2:
        file_name = sys.argv[1]
    if not os.path.exists(file_name):
        print(file_name + " というファイルは存在しません．")
        exit()
    return file_name


if __name__ == '__main__':
    participants_file_name = make_file_name()
    print(file_name)
    # participants_table = read_prticipants_table()