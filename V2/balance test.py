with open(r"RPI rewrite 2\current_balance.txt", "r", encoding='utf-8') as balance_file:
    balance_dict = {}
    balance_read = balance_file.read()
    balance_list = balance_read.split(":")
    user_list = []
    values_list = []
    user_number = int((len(balance_list)))
    for a in range(user_number):
        if (a % 2) == 0 or a == 0:
            user_list.append(str(balance_list[a])[1:])
        else:
            values_list.append(int(balance_list[a]))
    user_list.pop(len(user_list) - 1)
    for i in range(len(user_list)):
        balance_dict[user_list[i]] = values_list[i]