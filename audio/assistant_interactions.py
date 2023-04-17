####### Text to ask a demand #######


ask_1 = "Ouai gros ?"
ask_2 = "Tu veux quoi mon sauce ?"
ask_3 = "Ouai le zingue ?"
ask_4 = "Ouai ouai ouai ?"
ask_5 = "Wesh frero tu veux quoi ?"
ask_6 = "Tu veux quoi tete de zeub ?"
ask_7 = "Oh pélo il t'arrive quoi ?"


ask_name = [var_name for var_name in dir() if var_name.startswith("ask")]
ask = []
for var_name in ask_name:
	ask.append(globals()[var_name])


####### Text for an unclear input #######


unclear_1 = "Deso frero j'ai rien capté."
unclear_2 = "Man, je comprends rien a ce que tu racontes."
unclear_3 = "Pélo tu racontes quoi ? Je pige pas."

unclear_name = [var_name for var_name in dir() if var_name.startswith("unclear")]
unclear = []
for var_name in unclear_name:
	unclear.append(globals()[var_name])
