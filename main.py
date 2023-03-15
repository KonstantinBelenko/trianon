from completions import Candy
from dotenv import load_dotenv
load_dotenv()

response = Candy \
    .completion("The sky is blue because") \
    .set_max_tokens(64) \
    .append_input() \
    .run()

print(response)