import pdb

from django.db import connection


def login_user(email, senha):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM dashboard_pessoa WHERE email= '{email}'")
        rows = cursor.fetchall()
        if len(rows) == 1:
            columns = [col[0] for col in cursor.description]# monta uma lista com as colunas da tabela do db
            user = [dict(zip(columns, row)) for row in rows][0]  # monta dict para acesso mais facil as informações do select
            #print(user)
            cursor.close()
            if user['senha'] == senha:
                return user['id_pessoa']
        return False
