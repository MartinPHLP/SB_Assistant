####### Text to ask a demand #######


ask_1 = "Ouai gros ?"
ask_2 = "Tu veux quoi mon sauce ?"
ask_3 = "Ouai le zingue ?"
ask_4 = "Ouai ouai ouai ?"


ask_name = [var_name for var_name in dir() if var_name.startswith("ask")]
ask = []
for var_name in ask_name:
	ask.append(globals()[var_name])


####### Text for an unclear input #######


unclear_1 = "Deso frero j'ai rien capté."
unclear_2 = "Man, je comprends rien a ce que tu racontes."
unclear_3 = "Frandjo tu racontes quoi ? Je pige pas."

unclear_name = [var_name for var_name in dir() if var_name.startswith("unclear")]
unclear = []
for var_name in unclear_name:
	unclear.append(globals()[var_name])
