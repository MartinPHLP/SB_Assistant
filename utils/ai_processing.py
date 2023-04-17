import openai
from .keys_and_paths import OAI_ORGANIZATION_ID, OAI_SECRET_KEY_ACCESS


####### Setup #######


openai.organization = OAI_ORGANIZATION_ID
openai.api_key = OAI_SECRET_KEY_ACCESS


####### AI processing #######


def result_of_ai(input):
	"""
	This function use OpenAI API to treat the converted-to-text audio.

	Args:
		input (str): text from the conversion

	Returns:
		str: answer of the AI model
	"""

	completion = openai.ChatCompletion.create(
		model="gpt-3.5-turbo",
		messages=[
			{"role": "system", "content": "Tu es un assistant vocal. Tu te comportes comme un jeune" \
											"de cite de 20 ans extremement vulgaire et agressif"},
			{"role": "user", "content": f"{input}"}
		],
		max_tokens=200,
		temperature=0.9
	)
	return (completion['choices'][0]['message']['content'])
