import requests
from django.shortcuts import get_object_or_404
from dashboard.models import Pessoa
from django.db import connection


def exec_query(query):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]  # monta uma lista com as colunas da tabela do db
            cursor.close()
            return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        print(e)

def get_noticias(user_id):
    carteira = exec_query(query=f"SELECT * FROM dashboard_carteira where id_pessoa_id={user_id};")[0]
    carteiras_id = carteira['id_carteira']
    carteiras_valor = float(carteira['valor_total_carteira'])

    if carteiras_valor == 0:
        return []

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
                dca.nome_categoria_ativo AS ativo_nome,
                SUM(dco.valor_total_ativo) AS valor_total_somado
            FROM
                dashboard_carteiraoperacao dco
                LEFT JOIN
                dashboard_carteira dc ON dc.id_carteira = dco.id_carteira_id
                LEFT JOIN
                dashboard_operacao do ON dco.id_operacao_id = do.id_operacao
                LEFT JOIN
                dashboard_ativo da ON do.ticker_id = da.ticker
                LEFT JOIN
                dashboard_categoriaativo dca ON da.id_categoria_ativo_id = dca.id_categoria_ativo
                LEFT JOIN
                dashboard_pessoa dp ON dc.id_pessoa_id = dp.id_pessoa
            WHERE
                dp.id_pessoa = {user_id}
            GROUP BY
                dca.nome_categoria_ativo;
                """)
    result = {i["ativo_nome"]: float(i["valor_total_somado"]) for i in result_operacoes}

    return result

def get_total_por_carteira(user_id):
    result_operacoes = exec_query(query=f"""
                            SELECT
                                dc.valor_total_carteira
                            FROM
                                dashboard_carteira dc
                                    LEFT JOIN
                                dashboard_pessoa dp ON dc.id_pessoa_id = dp.id_pessoa
                            WHERE
                                dp.id_pessoa = {user_id};
                            """)[0]
    print(result_operacoes)
    result = float(result_operacoes['valor_total_carteira'])

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