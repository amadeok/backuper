


label = "name,duration,dontblend,substract,pre_attack_t,long_range,fast_attack,standingattack,useattack,DelayBeforeIdle,DistanceLevel,CombosInto,FeintsInto,nbDamagePhases,range,ComboStartPos,"

attack_names = "D,D2,DoubleRR,L,L2,L3,LD,p_D,p_DoubleRL,p_L,p_LD,p_LU,p_R,p_RD,p_RD2,p_RLow,p_RU,R,RD,RD2,RU,Thrust,Thrust2"
file = "C:\\Users\\amade\\Documents\\Unreal Projects\\third_person_426\\Source\\AnimTimingsCSV_m.csv"
new_file = "C:\\Users\\amade\\Documents\\Unreal Projects\\third_person_426\\Source\\AnimTimingsCSV_m.csv"
column_remove = 11
row_max = 24
with open(file) as inp_:
    new_data = []
    data = inp_.read().splitlines()
    data_arr = [[]]
    row_nb = 0
    while row_nb < row_max:
        line = data[row_nb]
        new_line = line.split(',')
        new_line.pop(column_remove)
        new_data.append(new_line)
        row_nb+=1
        
        print(line)
with open(new_file, 'w+') as out:
    for line in new_data:
        str_line = ""
        for entry in line:
            str_line += entry + ","
        out.write(str_line + "\n")
