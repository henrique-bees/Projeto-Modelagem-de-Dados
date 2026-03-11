# Twitter Scraper - Perfil Apple

Script para coletar tweets do perfil @Apple no Twitter/X.

## Instalação

```bash
pip install -r requirements.txt
```

## Uso

```bash
python twitter_scraper.py
```

## Dados Coletados

- Autor (username)
- Nome completo
- Descrição (texto do tweet)
- Data de publicação
- Likes
- Retweets
- Respostas
- Views
- URL do tweet
- Idioma
- Hashtags
- Menções

## Configuração

Edite as variáveis no script:
- `USERNAME`: usuário do Twitter (padrão: "Apple")
- `MAX_TWEETS`: número máximo de tweets (padrão: 500)
