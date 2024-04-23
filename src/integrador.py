import requests
import firebirdsql
## REQUESTS
class JSONRequester:
    def __init__(self):
        pass

    def request_json(self, uri):
        try:
            response = requests.get(uri)
            response.raise_for_status()  # Lança uma exceção para erros de HTTP
            return response.json()  # Retorna o JSON da resposta
        except requests.exceptions.RequestException as e:
            print("Erro ao fazer a requisição:", e)
            return None
## CONEXÃO
class FirebirdDBConnector:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        try:
            self.connection = firebirdsql.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            print("Conexão bem-sucedida com o banco de dados Firebird.")
        except Exception as e:
            print("Erro ao conectar ao banco de dados Firebird:", e)

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Conexão com o banco de dados Firebird fechada.")

    def insert_data(self, data):
        try:
            nome = data["pessoa"]["nome"]
            estado = data["pessoa"]["Estado"]
            cidade = data["pessoa"]["cidade"]
            pais = data["pessoa"]["pais"]     
            sql_command = f"INSERT INTO USUARIO (NOME, CIDADE, ESTADO, PAIS) VALUES(\'{nome}\', \'{estado}\', \'{cidade}\', \'{pais}\')"
            cursor = self.connection.cursor()
            cursor.execute(sql_command)
            self.connection.commit()
            print("Dados inseridos com sucesso.")
        except Exception as e:
            print("Erro ao inserir dados:", e)


# Entry Points
if __name__ == "__main__":
    requester = JSONRequester()
    uri = "https://gist.githubusercontent.com/BoscoBecker/b343b480631ca61b0b06f4dca6b23139/raw/440f560f86627871789eabdc4c86b4e819ddc9b1/data.json"
    json_data = requester.request_json(uri)
    persist = FirebirdDBConnector("localhost","D:\Projetos\Python\Integrador\src\Data\DADOS.FDB","SYSDBA", "masterkey")
    persist.connect()
    persist.insert_data(json_data)
    persist.disconnect()

