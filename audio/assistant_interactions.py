####### Text to ask a demand #######


ask_1 = "Oui, comment puis-je vous aider ?"
ask_2 = "Oui, je vous écoute !"
ask_3 = "De quoi avez-vous besoin ?"
ask_4 = "Que puis-je faire pour vous ?"
ask_5 = "De quoi avez-vous besoin ?"
ask_6 = "Quelle est votre question ?"



ask_name = [var_name for var_name in dir() if var_name.startswith("ask")]
ask = []
for var_name in ask_name:
	ask.append(globals()[var_name])


####### Text for an unclear input #######


unclear_1 = "Désolé, je n'ai pas compris."
unclear_2 = "Je n'ai pas compris ce que vous avez dit, pouvez-vous répéter ?"

unclear_name = [var_name for var_name in dir() if var_name.startswith("unclear")]
unclear = []
for var_name in unclear_name:
	unclear.append(globals()[var_name])
