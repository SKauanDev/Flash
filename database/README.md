# Banco de dados

O Flash usa MySQL 8.4+ e, no Windows, pode usar o MySQL do XAMPP.

## XAMPP

1. Abra o XAMPP Control Panel.
2. Inicie MySQL.
3. Deixe a porta em 3306.
4. Se o root tiver senha, ajuste scripts/setup_database.py.

## Criar o banco

Na raiz do projeto:

    python scripts/setup_database.py

Alternativamente, abra database/001_create_schema.sql no phpMyAdmin e execute-o.

O script cria o banco flash, o usuário flash e as tabelas users, messages, memories e tasks.

A aplicação usa:

    mysql+pymysql://flash:flash@127.0.0.1:3306/flash?charset=utf8mb4
