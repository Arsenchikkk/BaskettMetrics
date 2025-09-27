import psycopg2
import pandas as pd
import re

# Конфигурация подключения к базе данных
DB_HOST = "localhost"
DB_NAME = "nba db"  
DB_USER = "postgres" 
DB_PASS = "0000" 

def run_query(query, save_to_csv=None):
    """
    Выполняет SQL-запрос и выводит результат в терминал.
    При необходимости сохраняет результат в CSV.
    """
    conn = None  # Инициализируем conn, чтобы избежать второй ошибки
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = conn.cursor()
        print(f"Выполнение запроса:\n{query}\n")
        cur.execute(query)
        results = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        df = pd.DataFrame(results, columns=columns)
        print(df)
        
        if save_to_csv:
            df.to_csv(save_to_csv, index=False)
            print(f"\nРезультаты сохранены в файл: {save_to_csv}")
            
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Ошибка при выполнении запроса: {error}")
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    # Путь к файлу с SQL-запросами
    queries_file = "queries.sql"

    try:
        # Читаем файл с явным указанием кодировки UTF-8 с BOM
        with open(queries_file, 'r', encoding='utf-8-sig') as f:
            content = f.read()

        # Разделяем содержимое на отдельные запросы
        queries = [q.strip() for q in content.split(';') if q.strip()]

        # Выполняем каждый запрос из файла
        for i, query in enumerate(queries):
            print("-" * 50)
            print(f"Выполняется Запрос #{i + 1}")
            run_query(query)
            
    except FileNotFoundError:
        print(f"Ошибка: Файл '{queries_file}' не найден.")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")