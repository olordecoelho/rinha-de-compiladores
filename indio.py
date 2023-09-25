import argparse
import os
import ujson as json
import sys

from src.interpreter import interpret

class RinhaError(Exception):
    pass

def load_json_file(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        raise RinhaError(f"Error: Arquivo JSON '{filename}' nao encontrado.")
    except json.JSONDecodeError as e:
        raise RinhaError(f"Erro ao carregar o arquivo JSON '{filename}': {e}")

if __name__ == "__main__":
    os.system("clear")
    parser = argparse.ArgumentParser(description='Galo Índio da linguagem (Rinha)')
    parser.add_argument('-v', '--version', action='store_true', help='Versao do interpretador')
    parser.add_argument('-r', '--run', metavar='filename', type=str, help='Apenas arquivos .json')

    args = parser.parse_args()

    if args.run:
        try:
            filename = args.run
            if not filename.endswith('.json'):
                raise RinhaError("Error: O arquivo deve ter extenssao .json")
            
            data = load_json_file(filename)
            program_node = data.get("expression")
            if program_node is None:
                raise RinhaError("Error: Expressao nao encontrada.")
            
            output = interpret(program_node, {})  # Replace 'interpret' with your actual interpreter function
            print(output)
        except RinhaError as e:
            print(e, file=sys.stderr)
            sys.exit(1)
    else:
        print("Use 'indio -h' or 'indio --help' to get help.")
