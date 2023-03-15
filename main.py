# Before running this file, make sure you have installed the required packages
# and have set up the environment variables: NOUGAT_DB and OPENAI_API_KEY
# 
# To install the required packages, run the following command:
# pip install -r requirements.txt
#
# To set up the environment variables, create a .env file in the same directory
# as this file and add the following lines:
# NOUGAT_DB=<path to nougat.db>
# OPENAI_API_KEY=<your openai api key>
#
# To run this file, run the following command:
# python main.py

from candy import Candy
from nougat import Nougat
from dotenv import load_dotenv
load_dotenv()

nougat = Nougat()

query = input("> ")
similar_results = nougat.find_similar_concepts(query=query, entity="Hasp")
if not similar_results:
    print("No similar results found")
    exit()

final_prompt = Candy.prepare_similar_query(query, similar_results)
response = Candy.completion() \
    .set_prompt(final_prompt) \
    .set_temperature(0.7) \
    .set_max_tokens(64) \
    .set_stop(["stop"]) \
    .run() \
    .strip()

print(response)