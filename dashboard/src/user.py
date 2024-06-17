import pdb
from django.db import connection

def exec_query(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]# monta uma lista com as colunas da tabela do db
        cursor.close()
        return [dict(zip(columns, row)) for row in rows]


def todos_ativos(user_id): #todo entender e quebrar a função em menores
    carteiras_id = exec_query(query=f"SELECT id_carteira FROM dashboard_carteira where id_pessoa_id={user_id};")[0]
    carteiras_id = carteiras_id['id_carteira']

    operacao_id = exec_query(query=f"SELECT * FROM dashboard_carteiraoperacao where id_carteira_id = {carteiras_id};")
    ids_operacoes = [str(d['id_operacao_id']) for d in operacao_id]
    ids_operacoes = ','.join(ids_operacoes)

    operacoes = exec_query(query=f"SELECT * FROM dashboard_operacao where id_operacao in ({ids_operacoes});")
    #print(operacoes)
    tickets_id = [str(d['id_operacao']) for d in operacoes]

    ids_tickets = ','.join(tickets_id)

    ativos = exec_query(query=f"SELECT * FROM dashboard_ativo where ticker in ({ids_tickets});")
    #print(ativos)

    #calcula o valor total de operações pra cara ticket
    result_operacoes = {}

    for op in operacoes:
        if not result_operacoes.get(op['ticker_id']):
            result_operacoes[op['ticker_id']] = 0
        total = op['qtd_operacao'] * op['valor_un_operacao']
        total = total if op['tipo_operacao'] == 'Compra' else -total
        result_operacoes[op['ticker_id']] += float(total)

    id_news_ids = set()
    for item in ativos:
        id_news_ids.add(str(item['id_news_id']))
    id_news_ids_lista = list(id_news_ids)
    id_news_ids_lista = ','.join(id_news_ids_lista)

    noticias = exec_query(query=f"SELECT * FROM dashboard_news where id_news in ({id_news_ids_lista});")

    return {
        'total_por_ticker': result_operacoes,
        'noticias': noticias
    }

