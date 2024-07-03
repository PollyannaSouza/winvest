import datetime
from pprint import pprint

import pandas as pd
from django.db import connection


def exec_select(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        cursor.close()
        return pd.DataFrame([dict(zip(columns, row)) for row in rows])


def exec_query(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        cursor.close()


def compra(codigo_ativo, descricao_ativo, classe_risco, setor, descricao_setor, data_operacao, valor_unitario,
           quantidade_total, user_id):
    try:
        select_categoria_ativo = exec_select(
            f"SELECT * FROM dashboard_categoriaativo WHERE nome_categoria_ativo = '{codigo_ativo}'")
        print('Executou select_categoria_ativo:', select_categoria_ativo)

        if select_categoria_ativo.empty:
            exec_query(
                f"INSERT INTO dashboard_setor (nome_setor, descricao_setor) VALUES ('{setor}','{descricao_setor}')")
            print('Executou INSERT INTO dashboard_setor')

            exec_query(
                f"INSERT INTO dashboard_categoriaativo (nome_categoria_ativo, descricao_categoria_ativo, classe_risco) VALUES ('{codigo_ativo}','{descricao_ativo}', '{classe_risco}')")
            print('Executou INSERT INTO dashboard_categoriaativo')

            id_setor = \
            exec_select(f"SELECT id_setor FROM dashboard_setor WHERE nome_setor = '{setor}'")['id_setor'].values[0]
            print('Executou select id_setor:', id_setor)

            id_categoria_ativo = exec_select(
                f"SELECT id_categoria_ativo FROM dashboard_categoriaativo WHERE nome_categoria_ativo = '{codigo_ativo}'")[
                'id_categoria_ativo'].values[0]
            print('Executou select id_categoria_ativo:', id_categoria_ativo)

            exec_query(
                f"INSERT INTO dashboard_ativo (id_categoria_ativo_id, id_news_id, id_setor_id) VALUES ({id_categoria_ativo},13, {id_setor})")
            print('Executou INSERT INTO dashboard_ativo')

            print('entrou')

        id_categoria_ativo = exec_select(
            f"SELECT * FROM dashboard_categoriaativo WHERE nome_categoria_ativo = '{codigo_ativo}'")[
                                 'id_categoria_ativo'].values[0]
        print('Executou select id_categoria_ativo (de novo):', id_categoria_ativo)

        id_ativo = exec_select(f"SELECT * FROM dashboard_ativo WHERE id_categoria_ativo_id = {id_categoria_ativo}")['ticker'].values[0]

        query_operacao = f"""
        INSERT INTO dashboard_operacao (data_operacao, valor_un_operacao, qtd_operacao, tipo_operacao, ticker_id) 
        VALUES ('{data_operacao}',{float(valor_unitario)}, {quantidade_total}, 'Compra', {id_ativo})
        """
        print('query_operacao:', query_operacao)

        exec_query(query_operacao)
        print('Executou INSERT INTO dashboard_operacao')

        id_operacao = \
        exec_select('SELECT id_operacao FROM winvest.dashboard_operacao order by id_operacao desc limit 1;')[
            'id_operacao'].values[0]
        print('Executou select id_operacao:', id_operacao)

        qnt_total = float(valor_unitario) * int(quantidade_total)
        print('Calculou qnt_total:', qnt_total)

        query_carteira_operacao = f"INSERT INTO dashboard_carteiraoperacao (data_insercao, valor_total_ativo, valor_medio_ativo, id_carteira_id, id_operacao_id) VALUES ('{datetime.date.today()}',{qnt_total}, 0, {user_id}, {id_operacao})"
        print('query_carteira_operacao:', query_carteira_operacao)

        exec_query(query_carteira_operacao)
        print('Executou INSERT INTO dashboard_carteiraoperacao')

        carteira_atual = exec_select(f'SELECT * FROM winvest.dashboard_carteira WHERE id_pessoa_id = {user_id};')
        print('Executou select carteira_atual:', carteira_atual)

        novo_valor_total = float(carteira_atual['valor_total_carteira'].values[0]) + float(
            float(valor_unitario) * int(quantidade_total))
        print('Calculou novo_valor_total:', novo_valor_total)

        query_update = f"UPDATE winvest.dashboard_carteira SET valor_total_carteira = {novo_valor_total} WHERE id_carteira={user_id}"
        print('query_update:', query_update)

        exec_query(query_update)
        print('Executou UPDATE dashboard_carteira')

        return {'message': 'Adicionado com sucesso'}
    except Exception as e:
        pprint(f'EXCEÇÃO: {e}')


def venda(select_codigo, data_operacao, valor_unitario, quantidade_total, user_id):
    try:
        nome_ticket = select_codigo.split("'")[1]

        id_categoria_ativo = exec_select(
            f"SELECT * FROM dashboard_categoriaativo WHERE nome_categoria_ativo = '{nome_ticket}'")[
                'id_categoria_ativo'].values[0]
        print('Id categoria ativo: ', id_categoria_ativo)

        id_ativo = exec_select(f"SELECT * FROM dashboard_ativo WHERE id_categoria_ativo_id = {id_categoria_ativo}")[
            'ticker'].values[0]

        query_operacao = f"""
                INSERT INTO dashboard_operacao (data_operacao, valor_un_operacao, qtd_operacao, tipo_operacao, ticker_id) 
                VALUES ('{data_operacao}',{float(valor_unitario)}, {quantidade_total}, 'Venda', {id_ativo})
                    """
        # pprint(query_operacao)
        exec_query(query_operacao)
        id_operacao = exec_select('SELECT id_operacao FROM winvest.dashboard_operacao order by id_operacao desc limit 1;')[
            'id_operacao'].values[0]
        qnt_total = float(valor_unitario) * int(quantidade_total)
        query_carteira_operacao = f"INSERT INTO dashboard_carteiraoperacao (data_insercao, valor_total_ativo, valor_medio_ativo, id_carteira_id, id_operacao_id) VALUES ('{datetime.date.today()}',{-qnt_total}, 0, {user_id}, {id_operacao})"
        # print('QUERY CARTEIRA_OP', query_carteira_operacao)
        exec_query(query_carteira_operacao)

        carteira_atual = exec_select(f'SELECT * FROM winvest.dashboard_carteira WHERE id_pessoa_id = {user_id};')
        print(carteira_atual)
        novo_valor_total = float(carteira_atual['valor_total_carteira'].values[0]) - float(
            float(valor_unitario) * int(quantidade_total))
        print(novo_valor_total)
        query_update = f"UPDATE winvest.dashboard_carteira SET valor_total_carteira = {novo_valor_total} WHERE id_carteira={user_id}"
        print('query_update', query_update)
        exec_query(query_update)

        return {'message': 'Adicionado com sucesso'}
    except Exception as e:
        pprint(f'EXCEÇÃO: {e}')