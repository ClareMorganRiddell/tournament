1234567890123456789012345678901234567890123456789012345678901234567890123456789
#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def conn_and_cursor():
	"""Creates a cursor object"""
	pg = connect()
	return pg, pg.cursor()

def get_last_entry():
    """Returns last entry into Players table"""
    pg, c = conn_and_cursor()
    query_last_entry = """SELECT max(player_id)
                            FROM players"""
    c.execute(query_last_entry)
    new_id = c.fetchone()
    print new_id[0]
    pg.close()
    return int(new_id[0])

def reset_seq():
    """Resets Primary Key sequence during delete of table data"""
    sequence_start = 1
    pg, c = conn_and_cursor()
    update = """ALTER SEQUENCE players_player_id_seq 
                  RESTART WITH %s;"""
    c.execute(update, (sequence_start,))
    pg.commit()
    pg.close()
    return

def deleteStandings():
    """Remove all the entries in standings table."""
    pg, c = conn_and_cursor()
    c.execute("DELETE FROM standings;")
    rows_deleted = c.rowcount
    pg.commit()
    pg.close()
    return rows_deleted

def deleteMatches():
    """Remove all the match records from the database."""
    pg, c = conn_and_cursor()
    zero_matches, zero_wins = 0, 0
    update = """UPDATE standings 
                  SET matches = %s, wins = %s"""
    c.execute(update, (zero_matches, zero_wins))
    rows_deleted = c.rowcount
    pg.commit()
    pg.close()
    return rows_deleted

def deletePlayers():
    """Remove all the player records from the database and reset Primary Key
    sequence.
    """
    pg, c = conn_and_cursor()
    deleteStandings()
    c.execute("DELETE FROM players;")
    reset_seq()
    pg.commit()
    pg.close()
    return 

def countPlayers():
    """Returns the number of players currently registered."""
    pg, c = conn_and_cursor()
    c.execute("SELECT count(player_name) FROM players;")
    tot_count = c.fetchone()
    pg.close
    return int(tot_count[0])
    
def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
    
    Sanitizes input before proceddure is run.
    Creates a new player and registers the player in the standings table.

    Args:
      name: the player's full name (need not be unique).
    """
    clean_name = bleach.clean(name)
    pg, c = conn_and_cursor()
    new_player_name = """INSERT INTO players 
                           VALUES(%s)"""
    c.execute(new_player_name, (clean_name,))
    pg.commit()    
    new_id = get_last_entry()
    zero_wins, zero_matches = 0, 0
    new_standings = """INSERT INTO standings
                        VALUES(%s,%s,%s)"""
    c.execute(new_standings, (new_id, zero_wins, zero_matches))
    pg.commit()
    pg.close()
    return

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    pg, c = conn_and_cursor()
    c.execute("SELECT * FROM  view_standings")
    rows = c.fetchall()
    return rows

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.
    
    Sanitizes input before proceddure is run.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    clean_winner = bleach.clean(winner)
    clean_loser = bleach.clean(loser)
    pg, c = conn_and_cursor()
    add_win, add_match = 1, 1
    winner_update = """UPDATE standings 
    					SET wins = wins + %s, matches = matches + %s
    					WHERE player_id = %s"""
    loser_update = """UPDATE standings 
    					SET matches = matches + %s
    					WHERE player_id = %s"""
    c.execute(winner_update, (add_win, add_match,clean_winner))
    c.execute(loser_update, (add_match,clean_loser))
    pg.commit()
    pg.close()
    return playerStandings()
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player 
    adjacent to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    even_number = 2
    is_even_number = 0
    next_place = 1
    pg, c = conn_and_cursor()
    query_players = ("""SELECT DISTINCT ON (a.player_id, b.player_id) 
                        a.player_id, a.player_name,
                        b.player_id, b.player_name
                         FROM ordered_standings AS a
                           JOIN ordered_standings AS b
                           ON a.matches = b.matches
                           AND MOD(b.place, %s) = %s
                           AND b.place = (a.place +%s)""")
    c.execute(query_players, (even_number, is_even_number, next_place))
    sorted_list = c.fetchall()
    pg.close()
    return sorted_list