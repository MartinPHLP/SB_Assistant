import openai
from .keys_and_paths import OAI_ORGANIZATION_ID, OAI_SECRET_KEY_ACCESS


####### Setup #######


openai.organization = OAI_ORGANIZATION_ID
openai.api_key = OAI_SECRET_KEY_ACCESS

chat_memory = [{"role": "system", "content": "Tu es un assistant vocal. Tu t'exprimes dans un language naturel. Pas plus de 5 phrases."}]


####### AI processing #######


def chat_completion(input):
	"""
	This function declare the chat completion model for the conversation.

	Args:
		input (str): text from the conversion

	Returns:
		str: answer of the AI model
	"""

	completion = openai.ChatCompletion.create(
		model="gpt-3.5-turbo",
		messages=chat_memory,
		max_tokens=200,
		temperature=0.9
	)
	return completion['choices'][0]['message']['content']


def chat_resume(chat):
	"""
	This function summarize the conversation.

	Args:
		chat (str):conversation

	Returns:
		str: summarized conversation
	"""

	completion = openai.ChatCompletion.create(
		model="gpt-3.5-turbo",
		messages=[
			{"role": "system", "content": "you're a tool to summarize a conversation, sentences with max 5 words in french."},
			{"role": "user", "content": f"summarize it: {str(chat[1:])}"}
		],
		max_tokens=100,
		temperature=0.9
	)
	return completion['choices'][0]['message']['content']


def get_ia_response(input):
	"""
	This function use OpenAI API to treat the converted-to-text audio.

	Args:
		input (str): text from the conversion

	Returns:
		str: final result
	"""

	chat_memory.append({"role": "user", "content": f"{input}"})
	result = chat_completion(input)
	chat_memory.append({"role": "assistant", "content": f"{result}"})

	return result
