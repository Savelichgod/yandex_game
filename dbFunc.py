import sqlite3

db = sqlite3.connect('statistics.db')
cur = db.cursor()


def add_player(player_name, password):
    """Добавляет пользователя в базу"""
    query = f'INSERT INTO players(name, password) VALUES ("{player_name}", "{password}");'
    res = cur.execute(query)
    db.commit()
    return res


def get_players():
    """Получает список пользователей из базы"""
    players = cur.execute('SELECT name FROM players').fetchall()
    players_names = [player[0] for player in players]
    return players_names

def login(name, password):
    """Получает id пользователя, если он есть в базе"""
    id = cur.execute(f'SELECT id FROM players where name = "{name}" AND password = "{password}"').fetchone()
    if id:
        return id[0]
    return False

def write_game_result(player_id, status):
    cur.execute(f'INSERT INTO results (player_id, status) VALUES ({player_id},"{status}")')
    db.commit()

def get_statistics():
    """Топ 10 игроков"""
    query = """select name, status from results
                join players
                on players.id = results.player_id"""
    statistics = dict()
    res = cur.execute(query).fetchall()
    for record in res:
        name, staus = record
        if name not in statistics:
            statistics[name ] = {'won' : 0, 'lose':0, 'draw':0}
        statistics[name][staus] += 1
    summary_statistics = []
    for user in statistics:
        total_count = statistics[user]['won'] + statistics[user]['lose']
        wins = statistics[user]['won']
        rate = wins / total_count * 100
        summary_statistics.append((user, round(rate, 2)))
    summary_statistics.sort(key=lambda x: -x[1])

    return summary_statistics[:10]


def clear_players():
    """Удаляем всех пользователей из базы"""
    cur.execute('DELETE FROM players;')
    db.commit()


