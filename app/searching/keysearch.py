import cohere
co = cohere.Client('pyEdHfWeakU2lnu05xtTtX8Pnxh73Dhw3EoeJIpb')
from searching.input import get_input

user_input =  get_input()

def keysearch():
    user_input = get_input()

    response = co.generate(
        prompt='translate to English and propose intention to query of' + user_input,
    )

    # Translate the user input to English
    translated_input = response.generations[0].text
    response2 = co.generate(
        prompt='Based on the web search results from https://thegioididong.com and https://anphatpc.com.vn, Only give concise keywords about model, specifications of cheap laptop in Vietnamese Dong related to the following sentence ' + translated_input + 'only from from https://thegioididong.com and https://anphatpc.com.vn. Response have only concise specifications, no other question',
    )
    return response2.generations[0].text