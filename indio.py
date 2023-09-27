import argparse
import os
import sys
import ujson as json
from src.interpreter import Interpreter, RinhaError


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
    parser = argparse.ArgumentParser(description='Galo Índio da linguagem (Rinha)')
    parser.add_argument('-v', '--version', action='store_true', help='Versao do interpretador')
    parser.add_argument('-r', '--run', metavar='filename', type=str, help='Apenas arquivos .json')

    args = parser.parse_args()

    if args.run:
        filename = args.run
        if not filename.endswith('.json'):
            raise RinhaError("Error: O arquivo deve ser .json")
        
        data = load_json_file(filename)
        program_node = data.get("expression")
        if program_node is None:
            raise RinhaError("Error: Expressao nao encontrada.")
        
        print(Interpreter(program_node).run())
    else:
        default_file_path = os.path.join(os.path.dirname(__file__), 'var/rinha/source.rinha.json')
        try:
            data = load_json_file(default_file_path)
            program_node = data.get("expression")
            if program_node is None:
                raise RinhaError("Error: Expressao nao encontrada.")
            
            print(Interpreter(program_node).run())
        except RinhaError as e:
            print(e, file=sys.stderr)
            sys.exit(1)
else:
    print("Leia a Documentação em https://github.com/olordecoelho/rinha-de-compiladores")
