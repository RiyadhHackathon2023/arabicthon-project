from src.llm_agents.extractors.examples.events_examples import events_examples
from src.llm_agents.extractors.cohere_extractor import cohereExtractor

class cohereEventsExtractor(cohereExtractor):
    def __init__(self):
        super().__init__()
        self.examples = [e[1] for e in events_examples]
        self.example_labels = [e[0] for e in events_examples]
        self.example_prompt = "Extract in Arabic all the names of historical events from the text: "
        self.NO_RESULT = "لا شيء"
    
    def extract(self, example):
        extracted = super().extract(example)
        return extracted.split(',')