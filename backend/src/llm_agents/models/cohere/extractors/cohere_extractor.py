import cohere
from src.llm_agents.constants import COHERE_API_KEY
import time


class cohereExtractor():

    def __init__(self):
        self.api_key = COHERE_API_KEY
        self.co = cohere.Client(self.api_key)
        self.labels = []
        self.examples = []
        self.example_labels = []
        self.example_prompt = ""
        self.task_desciption = ""

    def make_prompt(self, example):
        examples = self.examples + [example]
        labels = self.example_labels + [""]
        return (self.task_desciption + "\n---\n".join([
            examples[i] + "\n" + self.example_prompt + labels[i]
            for i in range(len(examples))
        ]))

    def extract(self, example):
        while True:
            try:
                extraction = self.co.generate(prompt=self.make_prompt(example),
                                            temperature=0.1,
                                            stop_sequences=["\n"])
                return (extraction.generations[0].text)
            except cohere.error.CohereAPIError as e:
                    time.sleep(2)
