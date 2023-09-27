<div align="center">

![banner]

</div>

# Untitled

# **Galo Índio - V1.1**

## **Visão Geral**

O Galo Índio é um interpretador simples da linguagem de programação "Rinha". Este projeto foi desenvolvido como parte de um experimento de construção de um interpretador onde registro cada etapa do processo.

## **Uso Rápido**

Para começar, siga os passos abaixo:

### **1. Clone o Repositório**

Primeiro, clone o repositório do GitHub para obter o código-fonte do projeto:

```bash
git clone https://github.com/olordecoelho/rinha-de-compiladores
cd rinha-de-compiladores
```

### **2. Builde a Imagem Docker**

Em seguida, execute o seguinte comando para construir a imagem Docker:

```bash
docker build -t galo-indio .
```

### **3. Execute a Imagem Docker**

Rode a imagem Docker com a seguinte linha de comando:

```bash
docker run -e TERM=xterm galo-indio
```

### **Executando Programa Sem Docker**

Para executar programas Rinha a partir de arquivos JSON, utilize o seguinte comando:

```bash
python indio.py -r caminho-do-arquivo.rinha.json
```

> By Daniel Coelho - 2023 - olordecoelho@proton.me
>

[banner]: ./img/banner.png