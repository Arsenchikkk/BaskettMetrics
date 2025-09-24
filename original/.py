import pandas as pd

# Загружаем файл
df = pd.read_csv('ranking.csv')

# Удаляем дубликаты, оставляя только одну запись для каждой комбинации TEAM_ID и SEASON_ID
# Порядок сортировки (например, по дате) может быть важен, если есть несколько записей
df_unique = df.drop_duplicates(subset=['TEAM_ID', 'SEASON_ID'], keep='first')

# Сохраняем очищенный файл
df_unique.to_csv('ranking_clean.csv', index=False)