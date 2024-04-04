from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)
        
    def close(self):
        if self.__driver is not None:
            self.__driver.close()
        
    def run_query(self, query):
        if self.__driver is not None:
            with self.__driver.session() as session:
                result = session.run(query)
                return [record for record in result]
        else:
            return None

def find_common_friends(conn):
    query = """
    MATCH (p1:Person)-[:AMIGO_DE]->(friend)<-[:AMIGO_DE]-(p2:Person)
    WHERE p1.name = 'Alice' AND p2.name = 'Bob'
    RETURN friend.name AS FriendName
    """
    return conn.run_query(query)

if __name__ == "__main__":
    uri = "neo4j://localhost:7687"  # Substitua pelo seu URI
    user = "neo4j"                  # Substitua pelo seu usuário
    password = "Adriano543520$"           # Substitua pela sua senha
    
    # Estabelece conexão com o banco de dados
    conn = Neo4jConnection(uri, user, password)
    
    # Encontra amigos em comum
    common_friends = find_common_friends(conn)
    for friend in common_friends:
        print(f"Amigo em Comum: {friend['FriendName']}")
    
    # Fecha a conexão com o banco de dados
    conn.close()
