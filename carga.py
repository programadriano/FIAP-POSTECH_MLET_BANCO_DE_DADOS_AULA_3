from neo4j import GraphDatabase

class DataLoader:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def load_data(self):
        with self.driver.session() as session:
            session.write_transaction(self._create_users)
            session.write_transaction(self._create_movies)
            session.write_transaction(self._create_likes)

    @staticmethod
    def _create_users(tx):
        query = """
            UNWIND ['Thiago', 'Juliana', 'Agnes','Manuela'] AS userName
            MERGE (u:User {name: userName})
            """
        tx.run(query)

    @staticmethod
    def _create_movies(tx):
        # Atualize esta parte para incluir um dicionário com os nomes dos filmes e seus respectivos rótulos
        movies_data = [
            ("Pixels", "Comédia"),
            ("Titanic", "Drama"),
            ("The Chosen", "Drama"),
            ("Detona Ralph", "Animação"),
            ("Barbie", "Animação"),
        ]
        query = """
            UNWIND $moviesData AS movie
            MERGE (m:Movie {name: movie[0]})
            SET m.label = movie[1] 
            """
        tx.run(query, moviesData=movies_data)

    @staticmethod
    def _create_likes(tx):
        likes_data = [
            ("Thiago", "Pixels"),
            ("Thiago", "Detona Ralph"),
            ("Juliana", "Titanic"),
            ("Juliana", "The Chosen"),
            ("Juliana", "Pixels"),
            ("Juliana", "Detona Ralph"),
            ("Agnes", "Barbie"),
            ("Agnes", "Detona Ralph"),
            ("Manuela", "Barbie"),
        ]
        query = """
            UNWIND $likesData AS pair
            MATCH (u:User {name: pair[0]})
            MATCH (m:Movie {name: pair[1]})
            MERGE (u)-[:LIKES]->(m)
            """
        tx.run(query, likesData=likes_data)

# Substitua 'neo4j://localhost:7687', 'neo4j', 'password' com as suas credenciais de conexão
data_loader = DataLoader("neo4j://localhost:7687", "neo4j", "Adriano543520$")
data_loader.load_data()
data_loader.close()
