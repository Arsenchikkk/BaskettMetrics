import psycopg2
import pandas as pd

# Конфигурация подключения к базе данных
DB_HOST = "localhost"
DB_NAME = "nba db"  # Замените на имя вашей БД
DB_USER = "postgres"   # Замените на ваше имя пользователя
DB_PASS = "0000"         # Замените на ваш пароль

def run_query(query, save_to_csv=None):
    """
    Выполняет SQL-запрос и выводит результат в терминал.
    При необходимости сохраняет результат в CSV.
    """
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
    # Запрос из п. 4b
    query_top_scorers = """
    SELECT
        p."PLAYER_NAME",
        SUM(COALESCE(gd."PTS", 0)) AS total_points
    FROM
        games_details gd
    JOIN
        players p ON gd."PLAYER_ID" = p."PLAYER_ID"
    GROUP BY
        p."PLAYER_NAME"
    ORDER BY
        total_points DESC
    LIMIT 10;
    """
    run_query(query_top_scorers)

    # Пример запроса из п. 4c, с сохранением в файл
    query_top_teams = """
    SELECT
        t."NICKNAME",
        r."W"
    FROM
        ranking r
    JOIN
        teams t ON r."TEAM_ID" = t."TEAM_ID"
    WHERE
        r."SEASON_ID" = (SELECT MAX("SEASON_ID") FROM ranking)
    ORDER BY
        r."W" DESC
    LIMIT 10;
    """
    run_query(query_top_teams, save_to_csv='top_teams.csv')