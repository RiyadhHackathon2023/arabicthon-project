from src.llm_agents.extractors.examples.definitions_examples import definitions_examples, input_words
from src.llm_agents.extractors.cohere_extractor import cohereExtractor
import cohere
import time

class cohereDefinitionExtractor(cohereExtractor):
    def __init__(self):
        super().__init__()
        self.examples = [e[1] for e in definitions_examples]
        self.example_labels = [e[0] for e in definitions_examples]
        self.example_prompt = ""
        self.input_words = input_words + ['']
        self.no_result = 'منعدم'
    
    def extract(self, example, input_word):
        self.input_words[len(self.input_words)-1] = input_word
        while True:
            try:
                extraction = self.co.generate(
                prompt=self.make_prompt(example),
                temperature=0,
                stop_sequences=["\n"])
                break
            except cohere.error.CohereAPIError as e:
                time.sleep(10)
        return(extraction.generations[0].text)
    
    def create_prompt(self, input_word):
        return "Extract only in Arabic the definition of '{}' from the text: ".format(input_word)
    
    def make_prompt(self, example):
        examples = self.examples + [example]
        labels = self.example_labels + [""]
        return (self.task_desciption +
                "\n---\n".join( [examples[i] + "\n" +
                                self.create_prompt(self.input_words[i]) + 
                                 labels[i] for i in range(len(examples))]))