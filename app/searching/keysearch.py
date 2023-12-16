import cohere

co = cohere.Client('ZdmchLQ5VOe6SOLqVR5JJcqOGCyq2KzBWC4f6bOK')

user_input = input("What is your prompt? ")

response = co.generate(
    prompt='translate to English and propose intention to query of' + user_input,
)

# Translate the user input to English
translated_input = response.generations[0].text
response2 = co.generate(
    prompt='Based on the web search results from https://thegioididong.com and https://anphatpc.com.vn, Only give concise keywords about model, specifications of cheap laptop in Vietnamese Dong related to the following sentence ' + translated_input + 'only from from https://thegioididong.com and https://anphatpc.com.vn',
)
print(response2.generations[0].text)


def keysearch():
    return response2.generations[0].text