import requests
import requests
import mysql.connector

def consultar_cep(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)

    if response.status_code != 200:
        print("Erro ao consultar API.")
        return None
    
    dados = response.json()

    if "erro" in dados:
        print("CEP não encontrado.")
        return None

    return {
        "cep": dados["cep"].replace("-", ""),
        "logradouro": dados.get("logradouro", ""),
        "complemento": dados.get("complemento", ""),
        "bairro": dados.get("bairro", ""),
        "localidade": dados.get("localidade", ""),
        "uf": dados.get("uf", "")
    }


def inserir_no_mysql(dados):
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="senha123",
            database="banco123"
        )

        cursor = conexao.cursor()

        sql = """
        INSERT INTO ceps (cep, logradouro, complemento, bairro, localidade, uf)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        valores = (
            dados["cep"],
            dados["logradouro"],
            dados["complemento"],
            dados["bairro"],
            dados["localidade"],
            dados["uf"]
        )

        cursor.execute(sql, valores)
        conexao.commit()

        print("CEP inserido com sucesso!")

    except mysql.connector.Error as erro:
        print("Erro ao inserir no MySQL:", erro)

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

cep_input = input("Digite o CEP (somente números): ")

dados_cep = consultar_cep(cep_input)

if dados_cep:
    inserir_no_mysql(dados_cep)
