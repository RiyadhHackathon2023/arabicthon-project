from src.llm_agents.scrapers.playwright_sync import get_paragraphs
from src.llm_agents.sources.wikipedia import WikipediaSource
from src.llm_agents.extractors.cohere_definition_extractor import cohereDefinitionExtractor
from src.neo4j_db.neo4j_connection import Neo4jConnection
from src.llm_agents.classifiers.classify_definition import classify_definition


def generate_definitions(worker_id="",
                         domain="",
                         sources=[{
                             "type": "",
                             "content": ""
                         }],
                         words=[]):
    for source in sources:
        print(source["type"])
        if source["type"] == "Url":
            input_paragraphs = get_paragraphs(source["content"])
        elif source["type"] == "Wikipedia":
            wiki = WikipediaSource(domain=domain, n_docs=1)
            input_paragraphs = wiki.get_content()
        elif source["type"] == "File":
            input_paragraphs = source["content"]

        extractor = cohereDefinitionExtractor()

        conn = Neo4jConnection(
            uri='neo4j+s://5e2c94ef.databases.neo4j.io',
            user='neo4j',
            pwd='E53hCDHJjVnO8aTLMejfxtmz1G7q9LplVVO6K5L6drg')
        print('Scraping...')
        for paragraph in input_paragraphs:
            print("\nPARAGRAPH", paragraph)
            for word in words:
                if word in paragraph:
                    print("\nWORD", word)
                    paragraph = paragraph.replace('\'', '')
                    paragraph = paragraph.replace('\"', '')
                    print("REPLACED", paragraph)
                    if classify_definition(paragraph):
                        print("\nDEF FOUND")
                        extracted_text = extractor.extract(paragraph, word)
                        conn.add_definition(worker_id, word, extracted_text,
                                            domain)

        conn.close()
    return "OK"
