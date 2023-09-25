<div align="center">

![banner]

</div>

# O Galo mais brabo da [rinha-de-compiler](https://github.com/aripiprazole/rinha-de-compiler) - V1.0

### É um interpretador simples da linguagem 'Rinha' de programação, funciona, mas é lento. Registrei cada passo da construção do interpretador e vou publicar minha experiência em breve.

# Vamos rodar:

## Primeiramente builde a imagem:

```bash
docker build -t galo-indio .
```

## Segundamente rode a imagem:

```bash
docker run galo-indio
```
## Agora escreva assim para usar outros arquivos rinha em JSON:

```bash
python indio.py -r caminho-do-arquivo.rinha.json
```

## Enjoy

### Não, não é o galo mais brabo, mas eu tentei...

[banner]: ./img/banner.png