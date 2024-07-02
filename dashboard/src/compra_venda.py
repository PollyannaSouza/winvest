import datetime
from pprint import pprint
import pandas as pd

from django.db import connection


def exec_select(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]  # monta uma lista com as colunas da tabela do db
        cursor.close()
        return pd.DataFrame([dict(zip(columns, row)) for row in rows])


def exec_query(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        cursor.close()


def compra(codigo_ativo, descricao_ativo, classe_risco, setor, descricao_setor, data_operacao, valor_unitario,
           quantidade_total, user_id):
    try:
        select_categoria_ativo = exec_select(f"SELECT * FROM dashboard_categoriaativo WHERE nome_categoria_ativo = '{codigo_ativo}'")

        if select_categoria_ativo.empty:
            exec_query(f"INSERT INTO dashboard_setor (nome_setor, descricao_setor) VALUES ('{setor}','{descricao_setor}')")
            exec_query(f"INSERT INTO dashboard_categoriaativo (nome_categoria_ativo, descricao_categoria_ativo, classe_risco) VALUES ('{codigo_ativo}','{descricao_ativo}', '{classe_risco}')")
            id_setor = exec_select(f"SELECT id_setor FROM dashboard_setor WHERE nome_setor = '{setor}'")['id_setor'].values[0]
            id_categoria_ativo = exec_select(
                f"SELECT id_categoria_ativo FROM dashboard_categoriaativo WHERE nome_categoria_ativo = '{codigo_ativo}'")['id_categoria_ativo'].values[0]
            exec_query(f"INSERT INTO dashboard_ativo (id_categoria_ativo_id, id_news_id, id_setor_id) VALUES ({id_categoria_ativo},13, {id_setor})")
            print('entrou')
        id_categoria_ativo = exec_select(
            f"SELECT * FROM dashboard_categoriaativo WHERE nome_categoria_ativo = '{codigo_ativo}'")[
            'id_categoria_ativo'].values[0]
        exec_query(f""
                   f"INSERT INTO dashboard_operacao "
                   f"(data_operacao, valor_un_operacao, qnd_operacao, tipo_operacao, ticker_id) "
                   f"VALUES ({data_operacao},{valor_unitario}, {quantidade_total}, 'COMPRA', {id_categoria_ativo})"
                   )
        id_operacao = exec_select('SELECT id_operacao FROM winvest.dashboard_operacao order by id_operacao desc limit 1;')['id_operacao'].values[0]
        exec_query(f"INSERT INTO dashboard_categoriaoperacao (data_insercao, valor_total_ativo, valor_medio_ativo, id_carteira_id, id_operacao_id) VALUES ('{datetime.date.today()}',{valor_unitario*quantidade_total}, 0, {user_id}, {id_operacao})")
        carteira_atual = exec_select(f'SELECT * FROM winvest.dashboard_carteira WHERE id_pessoa_id = {user_id};')
        exec_query(f"UPDATE winvest.dashboard_carteira SET valor_total_carteira = {carteira_atual['valor_total_carteira'].values[0]+(valor_unitario*quantidade_total)} WHERE ")

        return {'message': 'Adicionado com sucesso'}
    except Exception as e:
        pprint(f'EXCEÇÃO: {e}')

def venda(select_codigo, data_operacao, valor_unitario, quantidade_total, user_id):
    ...
