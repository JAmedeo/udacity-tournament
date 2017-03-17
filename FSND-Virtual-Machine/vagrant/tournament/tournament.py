#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM matches")
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM players")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM players")
    result = cursor.fetchone()[0]
    conn.close()
    return result


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO players (name) values (%s)", (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""SELECT players.id as id,
                             players.name as name,
                             case when tmp.matches_won is null then 0 else tmp.matches_won end as wins,
                             case when tmp.matches_played is null then 0 else tmp.matches_played end as matches
                       FROM players
                       LEFT JOIN (
                            SELECT t.player_id,
                                   case when s.matches_won is null then 0
                                        else s.matches_won
                                   end as matches_won,
                                   t.matches_played
                            FROM completed_matches_by_players_id t
                            LEFT JOIN matches_won_by_players_id s
                            ON t.player_id = s.player_id
                            ) tmp on players.id = tmp.player_id
                       order by tmp.matches_won desc
                """)
    result = cursor.fetchall()
    conn.close()
    return result

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO matches (winner_id, loser_id) values ('%s', '%s')", (winner,loser,))
    conn.commit()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    cursor = conn.cursor()

    pairings = []
    cursor.execute("""SELECT * FROM matches LIMIT 1 """)
    if not cursor.fetchone():
        cursor.execute("""SELECT id, name FROM players""")
        temp = ()
        for row in cursor.fetchall():
            temp += (row[0], row[1])
            if len(temp) == 4:
                pairings.append(temp)
                temp = ()
    else:
        cursor.execute("select winner_id, loser_id from matches")
        existing_matches = []
        player_list = []
        for row in cursor.fetchall():
            existing_matches.append((row[0], row[1]))
            existing_matches.append((row[1], row[0]))
        future_matches = playerStandings()
        for player1 in future_matches:
            for player2 in future_matches:
                if player1[0] != player2[0]:
                    if ((player1[0], player2[0]) not in existing_matches and
                        player1[0] not in player_list and
                        player2[0] not in player_list):
                        pairings.append((player1[0], player1[1], player2[0], player2[1]))
                        player_list.append(player1[0])
                        player_list.append(player2[0])
                        break
    conn.close()
    return pairings

'''


reportMatch(1,2)
reportMatch(4,3)
reportMatch(1,3)
reportMatch(1,4)
reportMatch(2,3)
reportMatch(2,4)


'''

deleteMatches()
deletePlayers()
