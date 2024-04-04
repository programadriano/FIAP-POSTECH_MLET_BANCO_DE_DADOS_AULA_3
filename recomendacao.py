from neo4j import GraphDatabase

class MovieRecommender:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def recommend_movies(self, user_name):
        with self.driver.session() as session:
            result = session.execute_read(self._find_recommendations, user_name)
            return result

    @staticmethod
    def _find_recommendations(tx, user_name):
        query = (
            """
            MATCH (targetUser:User {name: $user_name})-[:LIKES]->(movie)<-[:LIKES]-(otherUser)
            WITH targetUser, otherUser
            MATCH (otherUser)-[:LIKES]->(recommendation)
            WHERE NOT EXISTS ((targetUser)-[:LIKES]->(recommendation))
            WITH recommendation, COUNT(DISTINCT otherUser) AS Score
            RETURN recommendation.name AS MovieName, Score
            ORDER BY Score DESC LIMIT 1
            """
        )
        print(user_name);
        result = tx.run(query, user_name=user_name)
        return [record["MovieName"] for record in result]

# Substitua 'neo4j://localhost:7687', 'neo4j', 'password' com as suas credenciais de conexão
recommender = MovieRecommender("neo4j://localhost:7687", "neo4j", "Adriano543520$")
recommended_movies = recommender.recommend_movies("Thiago")

print("Movies recommended for Thiago:")
for movie in recommended_movies:
    print(movie)
