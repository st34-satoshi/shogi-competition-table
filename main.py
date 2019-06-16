import csv
import sys
import os


class Participant:
    def __init__(self, id, name, year, grade, active):
        self.id = id
        self.name = name
        self.year = year  # int
        self.grade = grade  # float
        self.active = active  # boolean
        self.to_play_participants = []
        self.opponents = []

    def make_to_play_participants(self, participant_list):
        # grade_diff * 100 + year_diff
        sorted_participants = sorted(participant_list, key=lambda p: abs(p.grade - self.grade)*100+abs(p.year - self.year))
        for participant in sorted_participants:
            if self.active:
                # active
                if not participant.active:
                    self.to_play_participants.append(participant)
            else:
                # ob
                if participant.id != self.id:
                    self.to_play_participants.append(participant)

    def len_to_play(self):
        return len(self.to_play_participants)

    def set_opponent(self, opponent):
        if opponent is not None:
            self.to_play_participants.remove(opponent)
            self.opponents.append(opponent)
        else:
            self.opponents.append(self)

    def get_table_row(self):
        row = [self.name]
        for opponent in self.opponents:
            if opponent.id == self.id:
                row.append("休み")
            else:
                row.append(opponent.name)
        return row


def decide_player_to_play(participants_list, decided_id_dictionary):
    # return decided_participant_id_dictionary or None
    # dictionary key and item are participant id
    for i, target_participant in enumerate(participants_list):
        # decide target
        if target_participant.id not in decided_id_dictionary:
            for to_player in target_participant.to_play_participants:
                if to_player.id not in decided_id_dictionary:
                    # find opponent
                    decided_id_dictionary[target_participant.id] = to_player.id
                    decided_id_dictionary[to_player.id] = target_participant.id
                    # decide opponent of other participants
                    decided_ids = decide_player_to_play(participants_list[i+1:], decided_id_dictionary)
                    if decided_ids is None:
                        # find opponent again
                        remove = decided_id_dictionary.pop(to_player.id)
                        remove = decided_id_dictionary.pop(target_participant.id)
                    else:
                        return decided_ids
            # the target doesn't have opponent
            return None
    # all participants in decided_id_dictionary
    return decided_id_dictionary


def next_match_list(participant_list):
    # return the tuple list. tuple is player id.
    # TODO you can change here to change the result
    sorted_participants = sorted(participant_list, key=lambda p: p.len_to_play())
    # TODO you can change the rest participant
    if len(sorted_participants) % 2 == 1:
        rest_participant = sorted_participants.pop(0)
    return decide_player_to_play(sorted_participants, {})


def make_participants_table(file_name):
    participant_list = []
    # read file
    # TODO if you want to use shift_jis, change here
    # with open(file_name, 'r', encoding='shift_jis') as f:
    with open(file_name, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # ヘッダーを読み飛ばす
        participant_id = 0
        try:
            for row in reader:
                participant = Participant(participant_id, row[0], int(row[1][1:]), float(row[2]), row[1][0] == "A")
                participant_id += 1
                participant_list.append(participant)
        except:
            print("入力ファイルに誤りがあります")

    # make to play list of each participants
    for participant in participant_list:
        participant.make_to_play_participants(participant_list)

    return participant_list


def make_file_name():
    file_name = "participants.csv"
    if len(sys.argv) >= 3:
        file_name = sys.argv[2]
    if not os.path.exists(file_name):
        print(file_name + " というファイルは存在しません．")
        exit()
    return file_name


def play_times():
    if len(sys.argv) < 2:
        print("対局回数を指定してください．")
        exit()
    try:
        times = int(sys.argv[1])
        return times
    except:
        print("対局回数を正しく入力してください．")
        exit()


def save_to_file(participant_list, play_times):
    save_file = "competition-table.csv"
    header = ["氏名"]
    for r in range(play_times):
        header.append(str(r+1) + "回戦")
    comp_tables =[header]
    for participant in participant_list:
        comp_tables.append(participant.get_table_row())
    # TODO if you want to use shift_jis, change here
    # with open(save_file, 'w', encoding='shift_jis') as f:
    with open(save_file, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, lineterminator='\n')  # 改行コード（\n）を指定しておく
        writer.writerows(comp_tables)  # 2次元配列も書き込める


if __name__ == '__main__':
    play_time = play_times()
    print(play_time)
    participants_file_name = make_file_name()
    participants = make_participants_table(participants_file_name)
    decided_times = 0
    for r in range(play_time):
        player_ids = next_match_list(participants)
        if player_ids is None:
            print("cannot decide next opponent")
            break
        for participant in participants:
            if participant.id in player_ids:
                opponent_id = player_ids[participant.id]
                participant.set_opponent(participants[opponent_id])
            else:
                # rest
                participant.set_opponent(None)
        decided_times += 1
    # save
    save_to_file(participants, decided_times)
