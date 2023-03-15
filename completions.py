import openai
import os

class Runner:

    def __init__(self) -> None:
        self.prompt = ""
        self.tokens = 128
        self.temperature = 0.7
        self.engine = 'text-davinci-003'
        self.append_prompt = False
        self.separator = ""

        self.openai = openai
        self.openai.api_key = os.getenv("OPENAI_API_KEY")

    def set_prompt(self, prompt: str):
        self.prompt = prompt
        return self

    def set_max_tokens(self, tokens: int):
        self.tokens = tokens
        return self
    
    def append_input(self, separator: str = ""):
        self.append_prompt = True
        self.separator = separator
        return self

class CompletionRunner(Runner):

    def __init__(self) -> None:
        super().__init__()

    def run(self):
        result = openai.Completion.create(
            engine=self.engine,
            prompt=self.prompt,
            temperature=self.temperature,
            max_tokens=self.tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["\n"]
        )

        text = result.choices[0].text
        if self.append_prompt:
            text = self.prompt + self.separator + text

        return text

class ChatRunner(Runner):

    def __init__(self) -> None:
        super().__init__()
        self.message_log = []
        self.engine = 'gpt-3.5-turbo'

    def set_prompt(self, prompt: str):
        self.message_log.append(prompt)
        self.prompt = prompt
        return self

    def run(self) -> str:
        response = openai.ChatCompletion.create(
            model=self.engine,
            messages=self.message_log
        )

        result = ''
        for choice in response.choices:
            result += choice.message.content

        self.message_log.append(result)

        return result



class Candy:

    def __init__(self) -> None:
        pass        

    @staticmethod
    def completion(prompt: str):
        r = CompletionRunner()
        return r.set_prompt(prompt)
    
    @staticmethod
    def chat(prompt: str):
        r = ChatRunner()
        return r.set_prompt(prompt)