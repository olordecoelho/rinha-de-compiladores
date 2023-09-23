import argparse
from src.interpreter import *
import ujson as json


def load_json_file(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        raise RinhaError(f"Erro ao carregar o arquivo JSON '{filename}': {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Interpretador Galo Índio da linguagem Rinha')
    parser.add_argument('-v', '--version', action='store_true', help='Mostra a versão do interpretador')
    parser.add_argument('-r', '--run', metavar='filename', type=str, help='Rodar a partir de um Arquivo .json')

    args = parser.parse_args()

    if args.run:
        try:
            filename = args.run

            if not filename.endswith('.json'):
                raise RinhaError("O arquivo deve ter a extensão .json")
        except Exception as e:
            print(f"Erro: {e}")
        else:
            data = load_json_file(filename)
            program_node = data["expression"]
            output = interpret(program_node, {})
            print(output)
    else:
        print("Use 'indio -h' or 'indio --help' to get help.")
