SELECT * FROM games LIMIT 10;
---------------------------
SELECT "PLAYER_NAME", "PTS"
FROM games_details
WHERE "PTS" >= 50
ORDER BY "PTS" DESC;
---------------------------
SELECT
    "TEAM_ID",
    COUNT("GAME_ID") AS total_games,
    AVG("PTS") AS avg_points,
    MIN("PTS") AS min_points,
    MAX("PTS") AS max_points
FROM
    games_details
GROUP BY
    "TEAM_ID"
ORDER BY
    avg_points DESC;
----------------------------
SELECT
    p."PLAYER_NAME",
    SUM(gd."PTS") AS total_points
FROM
    games_details gd
JOIN
    players p ON gd."PLAYER_ID" = p."PLAYER_ID"
GROUP BY
    p."PLAYER_NAME"
ORDER BY
    total_points DESC
LIMIT 10;

-- Считает среднее количество очков, набранных домашней и гостевой командами за все матчи.
SELECT
    AVG("PTS_home") AS avg_home_pts,
    AVG("PTS_away") AS avg_away_pts
FROM
    games;

-- Находит 10 команд с наибольшим количеством побед в последнем сезоне.
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

-- Находит топ-5 игроков с максимальным количеством передач (AST) в одной игре.
SELECT
    p."PLAYER_NAME",
    gd."AST",
    gd."GAME_ID"
FROM
    games_details gd
JOIN
    players p ON gd."PLAYER_ID" = p."PLAYER_ID"
ORDER BY
    gd."AST" DESC
LIMIT 5;

-- Рассчитывает средний процент побед (W_PCT) для каждой конференции.
SELECT
    "CONFERENCE",
    AVG("W_PCT") AS avg_win_percentage
FROM
    ranking
WHERE
    "SEASON_ID" = (SELECT MAX("SEASON_ID") FROM ranking)
GROUP BY
    "CONFERENCE";

-- Считает общее количество игр, в которых участвовал каждый игрок.
SELECT
    p."PLAYER_NAME",
    COUNT(DISTINCT gd."GAME_ID") AS games_played
FROM
    games_details gd
JOIN
    players p ON gd."PLAYER_ID" = p."PLAYER_ID"
GROUP BY
    p."PLAYER_NAME"
ORDER BY
    games_played DESC
LIMIT 10;

-- Находит игры, где было набрано наибольшее суммарное количество очков обеими командами.
SELECT
    "GAME_ID",
    "PTS_home" + "PTS_away" AS total_points
FROM
    games
ORDER BY
    total_points DESC
LIMIT 10;

-- Считает общее количество игр, выигранных домашней командой.
SELECT
    SUM("HOME_TEAM_WINS") AS home_wins_count
FROM
    games;

-- Рассчитывает среднее количество подборов для каждой команды за все игры.
SELECT
    t."NICKNAME",
    AVG(gd."REB") AS avg_rebounds
FROM
    games_details gd
JOIN
    teams t ON gd."TEAM_ID" = t."TEAM_ID"
GROUP BY
    t."NICKNAME"
ORDER BY
    avg_rebounds DESC
LIMIT 10;

-- Находит игроков с лучшим процентом трехочковых (FG3_PCT) при условии, что они сделали не менее 100 бросков.
SELECT
    p."PLAYER_NAME",
    SUM(gd."FG3M") * 100.0 / SUM(gd."FG3A") AS three_point_pct
FROM
    games_details gd
JOIN
    players p ON gd."PLAYER_ID" = p."PLAYER_ID"
GROUP BY
    p."PLAYER_NAME"
HAVING
    SUM(gd."FG3A") >= 100
ORDER BY
    three_point_pct DESC
LIMIT 10;

-- Определяет города, в которых базируется наибольшее количество команд.
SELECT
    "CITY",
    COUNT("TEAM_ID") AS team_count
FROM
    teams
GROUP BY
    "CITY"
ORDER BY
    team_count DESC;