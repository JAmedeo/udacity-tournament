#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    try:
        conn = psycopg2.connect("dbname={}".format(database_name))
        cursor = conn.cursor()
        return conn, cursor
    except:
        print("<error message>")


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn, cursor = connect()

    query = "INSERT INTO players (name) VALUES (%s);"
    parameter = (name,)
    cursor.execute(query, parameter)

    conn.commit()
    conn.close()


def deleteMatches():
    """Remove all the match records from the database."""
    conn, cursor = connect()
    cursor.execute(" TRUNCATE matches;")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn, cursor = connect()
    cursor.execute("TRUNCATE players CASCADE;")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn, cursor = connect()
    cursor.execute("SELECT count(*) FROM players;")
    result = cursor.fetchone()[0]
    conn.close()
    return result


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
    conn, cursor = connect()
    cursor.execute("""SELECT players.id as id,
                             players.name as name,
                             case when tmp.matches_won is null then 0 else tmp.matches_won end as wins,  # NOQA
                             case when tmp.matches_played is null then 0 else tmp.matches_played end as matches  # NOQA
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
    conn, cursor = connect()
    query = "INSERT INTO matches (winner_id, loser_id) values ('%s', '%s')"
    parameter = (winner, loser,)
    cursor.execute(query, parameter)
    conn.commit()
    conn.close()


def swissPairings():
    # retrieves player standings i.e. id, player, wins, matches ordered by wins
    standings = playerStandings()
    # pairs for next round are stored in this array.
    next_round = []

    # iterates on the standings results. As the results are already in
    # descending order, the pairs can be made using adjacent players, hence the
    # loop is set to interval of 2 to skip to player for next pair
    # in every iteration.
    for i in range(0, len(standings), 2):
        # each iteration picks player attributes (id, name) of current row
        # and next row and adds in the next_round array.
        next_round.append((standings[i][0], standings[i][1], standings[i + 1][0], standings[i + 1][1]))  # NOQA
    # pairs for next round are returned from here.
    return next_round
