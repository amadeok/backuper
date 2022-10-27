file = "C:\\Users\\amade\\Documents\\Unreal Projects\\third_person_426\\Source\\AnimTimingsCSV.csv"

class attack_data:
    def __init__(self, name, r_start, r_end) -> None:
        self.name = name
        self.r_start = r_start
        self.r_end = r_end
        self.distance_array = []

attack_list = []
attack_names = []
with open(file, "r") as inp:

    text = inp.read()
    text = text.split("#END")[0]
    text_splitted  = text.splitlines()

    lis = []
    for line in text_splitted:
        lis.append([entry for entry in line.split(",")])


    labels = lis[0]
    lis.pop(0)
    for attack_ in lis:
        ranges = attack_[12].split("-")
        attack_list.append(attack_data(attack_[0], ranges[0], ranges[1]))


lvl = 0
for attack in attack_list:
    

print(attack_list)
    
