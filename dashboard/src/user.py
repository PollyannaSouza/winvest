import requests
from django.shortcuts import get_object_or_404
from dashboard.models import Pessoa
from django.db import connection


def exec_query(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]  # monta uma lista com as colunas da tabela do db
        cursor.close()
        return [dict(zip(columns, row)) for row in rows]


def get_noticias(user_id):
    carteiras_id = exec_query(query=f"SELECT id_carteira FROM dashboard_carteira where id_pessoa_id={user_id};")[0]
    carteiras_id = carteiras_id['id_carteira']

    operacao_id = exec_query(query=f"SELECT * FROM dashboard_carteiraoperacao where id_carteira_id = {carteiras_id};")
    ids_operacoes = [str(d['id_operacao_id']) for d in operacao_id]
    ids_operacoes = ','.join(ids_operacoes)

    operacoes = exec_query(query=f"SELECT * FROM dashboard_operacao where id_operacao in ({ids_operacoes});")
    tickets_id = [str(d['id_operacao']) for d in operacoes]

    ids_tickets = ','.join(tickets_id)

    ativos = exec_query(query=f"SELECT * FROM dashboard_ativo where ticker in ({ids_tickets});")

    id_news_ids = set()
    for item in ativos:
        id_news_ids.add(str(item['id_news_id']))
    id_news_ids_lista = list(id_news_ids)
    id_news_ids_lista = ','.join(id_news_ids_lista)

    noticias = exec_query(query=f"SELECT * FROM dashboard_news where id_news in ({id_news_ids_lista});")

    return noticias


def get_total_por_ticker(user_id):
    result_operacoes = exec_query(query=f"""
                              SELECT
                                    dc.valor_total_carteira,
                                    dca.nome_categoria_ativo AS ativo_nome
                                FROM
                                    dashboard_carteira dc
                                LEFT JOIN
                                    dashboard_carteiraoperacao dco ON dc.id_carteira = dco.id_carteira_id
                                LEFT JOIN
                                    dashboard_operacao do ON dco.id_operacao_id = do.id_operacao
                                LEFT JOIN
                                    dashboard_ativo da ON do.ticker_id = da.ticker
                                LEFT JOIN
                                    dashboard_categoriaativo dca ON da.id_categoria_ativo_id = dca.id_categoria_ativo
                                LEFT JOIN
                                    dashboard_pessoa dp ON dc.id_pessoa_id = dp.id_pessoa
                                WHERE
                                    dp.id_pessoa = {user_id};
                              """)
    result = {i["ativo_nome"]: float(i["valor_total_carteira"]) for i in result_operacoes}

    print(f"RESULT_OPERACOES: {result}")
    return result


def nome_user(user_id):
    pessoa = get_object_or_404(Pessoa, id_pessoa=user_id)
    partes_nome = pessoa.nome.split()
    primeiro_nome = partes_nome[0] if partes_nome else ''
    return primeiro_nome


def get_dados_grafico(total_por_ticker):
    labels = [i for i in total_por_ticker.keys()]
    values = [i for i in total_por_ticker.values()]

    return labels, values


def get_cotacoes(tickers):
    token = '12wokeQFxmxvd2kExnMYjJ'

    result = []
    for ticker in tickers:
        try:
            url = rf'https://brapi.dev/api/quote/{ticker}?token={token}'
            res = requests.get(url=url)
            res = res.json()['results'][0]
            info_dict = {
                'longName': res['longName'],
                'regularMarketChange': res['regularMarketChange'],
                'regularMarketChangePercent': res['regularMarketChangePercent'],
                'regularMarketPrice': res['regularMarketPrice'],
                'symbol': res['symbol']
            }
            result.append(info_dict)
        except:
            print(f'Ticket {ticker} não existe na API')

    return result