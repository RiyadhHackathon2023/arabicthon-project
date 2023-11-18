import cohere
from src.llm_agents.extractors.examples.translation_examples import translations_examples
import time

# Paste your API key here. Remember to not share publicly
api_key = 'p9jFscVEhxLVDMI8sqCU4JX2STAVMAFUUja2SgXg'

# Create and retrieve a Cohere API key from os.cohere.ai
co = cohere.Client(api_key) 

class CohereTranslator():
    def __init__(self, arabic_to_english=True):
        self.labels = []
        self.task_desciption = ""
        if arabic_to_english:
            self.example_prompt = "Translate the text to English: "
            self.examples = [e[1] for e in translations_examples]
            self.example_labels = [e[0] for e in translations_examples]
        else:
            self.example_prompt = "Translate the text to Arabic: "
            self.examples = [e[0] for e in translations_examples]
            self.example_labels = [e[1] for e in translations_examples]
        

    def make_prompt(self, example):
        examples = self.examples + [example]
        labels = self.example_labels + [""]
        return (self.task_desciption +
                "\n---\n".join( [examples[i] + "\n" +
                                self.example_prompt + 
                                 labels[i] for i in range(len(examples))]))

    def extract(self, example):
        while True:
            try:
                extraction = co.generate(
                    prompt=self.make_prompt(example),
                    max_tokens=100,
                    temperature=0.1,
                    stop_sequences=["\n"])
                break
            except cohere.error.CohereAPIError as e:
                time.sleep(10)
        return(extraction.generations[0].text)