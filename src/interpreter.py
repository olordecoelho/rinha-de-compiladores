import json
import os

# Caminho do JSON
json_file_path = os.path.join("src", "files", "hello.rinha.json")

try:
    # Lê o JSON do arquivo e carrega em json_data
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)

    # Função para analisar e executar o JSON
    def execute_json(json_data):
        if "expression" in json_data and "kind" in json_data["expression"]:
            if json_data["expression"]["kind"] == "Print":
                message = json_data["expression"]["value"]["value"]
                print(message)
            else:
                print("Erro: Comando desconhecido.")
        else:
            print("Erro: Formato JSON inválido.")
        

    # Chamada da função para executar o JSON
    execute_json(json_data)

except FileNotFoundError:
    print(f"Erro: Arquivo JSON não encontrado em '{json_file_path}'.")

except json.JSONDecodeError:
    print(f"Erro: Falha na decodificação do JSON em '{json_file_path}'.")

except Exception as e:
    print(f"Erro desconhecido: {str(e)}")
