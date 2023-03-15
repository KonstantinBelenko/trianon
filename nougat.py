# This file contains classes and functions to interact with SQLight database
# and query the database for similar concepts based on the provided query.
import os 
import sqlite3

class SimilarConcept:

    def __init__(self, concept: str, description: str, entity: str) -> None:
        self.concept = concept
        self.description = description
        self.entity = entity

    def __str__(self) -> str:
        return f"{self.concept} - {self.description}"
    
    def __repr__(self) -> str:
        return f"{self.entity} | {self.concept}: {self.description}"
    
class Nougat:

    def __init__(self) -> None:

        self.punctuation_marks = ".,?!:;"

        self.db = sqlite3.connect(os.getenv("NOUGAT_DB"))
        self.cursor = self.db.cursor()

        self.init_tables()

    def init_tables(self) -> None:
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS concepts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                concept TEXT NOT NULL,
                description TEXT NOT NULL,
                entity TEXT NOT NULL
            )
        """)
        self.db.commit()

    def add_concept(self, concept: SimilarConcept) -> None:
        self.cursor.execute("""
            INSERT INTO concepts (concept, description, entity) VALUES (?, ?, ?)
        """, (concept.concept, concept.description, concept.entity))
        self.db.commit()

    def remove_concept(self, concept: SimilarConcept) -> None:
        self.cursor.execute("""
            DELETE FROM concepts WHERE concept = ? AND description = ? AND entity = ?
        """, (concept.concept, concept.description, concept.entity))
        self.db.commit()

    def list_entities(self) -> list[str]:
        self.cursor.execute("""
            SELECT DISTINCT entity FROM concepts
        """)
        return self.cursor.fetchall()
    
    def find_similar_concepts(self, query: str, entity: str) -> list[SimilarConcept]:
        # Remove marks and punctuations from the query
        query = query.translate(str.maketrans('', '', self.punctuation_marks))

        # Find similar concepts based on the words in the query
        results = []
        for word in query.split():
            self.cursor.execute("""
                SELECT concept, description, entity FROM concepts WHERE concept LIKE ? AND entity = ?
            """, (f"%{word}%", entity))
            result = self.cursor.fetchall()
            if result:
                for individual in result:
                    results.append(
                        SimilarConcept(
                            concept=individual[0],
                            description=individual[1],
                            entity=individual[2]
                        )
                    )

        # Flatten the list and remove the duplicates
        return list(set(results))