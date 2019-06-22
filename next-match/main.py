import csv
import sys
import os
import random
import copy


class Participant:
    def __init__(self, id, row):
        self.id = id
        self.name = row[0]
        self.year = int(row[1][1:])  # int
        self.grade = float(row[2])  # float
        self.active = row[1][0] == "A"  # boolean
        self.win_point = self.make_win_point(row)  # win(O) is 1, draw(-) is 0.5
        self.played_players_name = self.make_played_player_name_list(row)
        self.opponent = None  # Participant object
        self.position = -1
        self.row = row
        self.rest_count = 0

    def make_played_player_name_list(self, row):
        played_player_list = []
        for i in range(1, len(row) // 3):
            opponent_name = row[i*3+0]
            if opponent_name == "休み":
                self.rest_count += 1
            else:
                played_player_list.append(opponent_name)
        return played_player_list

    @staticmethod
    def make_win_point(row):
        # O is 1, - is 0.5 point
        win_point = 0
        for i in range(1, len(row)//3):
            win_char = row[i*3+2]
            if win_char == 'O':
                win_point += 1
            elif win_char == "-":
                win_point += 0.5
        return win_point

    def decide_opponent(self, ob_list):
        # close win point, grade, older
        # return opponent, if cannot decide None
        if self.active:
            sorted_obs = sorted(ob_list, key=lambda p: abs(p.win_point-self.win_point)*1000+abs(p.grade-self.grade)*100+p.year)
        else:
            sorted_obs = sorted(ob_list, key=lambda p: abs(p.win_point - self.win_point) * 1000 + abs(p.grade - self.grade) * 100 + abs(p.year-self.year))
        for ob in sorted_obs:
            if ob.name not in self.played_players_name:
                return ob
        return None

    def get_table_row(self):
        # add opponent name, position, space
        row = self.row
        if self.opponent.id == self.id:
            row.append("休み")
            row.append("")
        else:
            row.append(self.opponent.name)
            row.append(str(self.position))
        row.append("")
        return row

    def set_position(self, position_n):
        if self.position != -1:
            # already decided
            return position_n
        if self.opponent.id == self.id:
            # rest
            self.position = 0
            # not increment
            return position_n
        else:
            self.position = position_n
            # the opponent must be same position
            self.opponent.position = position_n
            return position_n + 1


def make_participants_list(file_name):
    active_participants = []
    ob_participants = []
    all_participant_list = []
    next_round_number = 0
    participants_name_list = []
    header = ""
    # read file
    # TODO if you want to use shift_jis, change here
    # with open(file_name, 'r', encoding='shift_jis') as f:
    with open(file_name, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        next_round_number = len(header) // 3
        participant_id = 0
        try:
            for row in reader:
                participant = Participant(participant_id, row)
                participant_id += 1
                if participant.active:
                    active_participants.append(participant)
                    all_participant_list.append(participant)
                else:
                    ob_participants.append(participant)
                    all_participant_list.append(participant)
                if row[0] in participants_name_list:
                    print("同じ名前が二つあります．" + row[0])
                    exit()
                participants_name_list.append(row[0])
        except:
            print("入力ファイルに誤りがあります")

    # TODO remove
    # # make to play list of each participants
    # for participant in participant_list:
    #     participant.make_to_play_participants(participant_list)

    return all_participant_list, active_participants, ob_participants, next_round_number, header


def make_file_name():
    file_name = "participants.csv"
    if len(sys.argv) >= 3:
        file_name = sys.argv[2]
    if not os.path.exists(file_name):
        print(file_name + " というファイルは存在しません．")
        exit()
    return file_name


def save_to_file(participant_list, header):
    round_number = len(header) // 3
    save_file = "participants{0}.csv".format(round_number)
    header.append(str(round_number) + "回戦")
    header.append("場所")
    header.append("勝敗")
    comp_tables =[header]
    for p in participant_list:
        comp_tables.append(p.get_table_row())
    # TODO if you want to use shift_jis, change here
    # with open(save_file, 'w', encoding='shift_jis') as f:
    with open(save_file, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, lineterminator='\n')  # 改行コード（\n）を指定しておく
        writer.writerows(comp_tables)  # 2次元配列も書き込める


def decide_active_opponent(active_participants, ob_participants):
    # decide active participant opponent
    # return remain obs
    remain_obs = ob_participants
    for active in active_participants:
        opponent = active.decide_opponent(remain_obs)
        if opponent is None:
            print("Cannot decide opponent")
            exit()
        opponent.opponent = active
        active.opponent = opponent
        remain_obs.remove(opponent)
    return remain_obs


def decide_ob_opponent(ob_participants):
    # return boolean, no remain ob or not
    if len(ob_participants) == 0:
        return True
    if len(ob_participants) % 2 == 1:
        print("Error cannot decide opponent because the number is odd")
        exit()
    # the order is win_point grade
    random.shuffle(ob_participants)
    sorted_obs = sorted(ob_participants, key=lambda p: (p.win_point+p.grade) * -1)
    target_obs = sorted_obs.pop(0)
    # close win point, grade, year
    sorted_obs = sorted(sorted_obs, key=lambda p: abs(p.win_point-target_obs.win_point)*1000+abs(p.grade-target_obs.grade)*100+abs(p.year-target_obs.year))
    for ob in sorted_obs:
        if ob.name not in target_obs.played_players_name:
            obs_list = []  # this doesn't have ob
            for o in sorted_obs:
                if o.name != ob.name:
                    obs_list.append(o)
            if decide_ob_opponent(obs_list):
                # all obs decide opponent
                ob.opponent = target_obs
                target_obs.opponent = ob
                return True
            # cannot decide
    return False


if __name__ == '__main__':
    participants_file_name = make_file_name()
    all_participants, active_participants_list, ob_participants_list, next_round, head = make_participants_list(participants_file_name)
    # sort active participants, win point, random
    random.shuffle(active_participants_list)
    # if the number is odd, decide rest one
    if (len(active_participants_list) + len(ob_participants_list)) % 2 == 1:
        active_participants_list = sorted(active_participants_list, key=lambda p: p.rest_count * -1)
        rest_active = active_participants_list.pop(0)
        rest_active.opponent = rest_active
    active_participants_list = sorted(active_participants_list, key=lambda p: p.win_point*-1)
    # decide active opponent
    remain_ob_list = decide_active_opponent(active_participants_list, ob_participants_list)
    if remain_ob_list is None:
        print("cannot decide next opponent")
        exit()
    # decide ob opponent
    if not decide_ob_opponent(remain_ob_list):
        print("cannot decide ob next opponent")
        exit()
    # decide position
    # order is year
    position_number = 1
    for participant in sorted(all_participants, key=lambda p: p.grade+100*p.year):
        position_number = participant.set_position(position_number)
    # save
    save_to_file(all_participants, head)
