CREATE TABLE players (
    id SERIAL primary key,
    name varchar(80) NOT NULL
);

--  The following two constraints ensures a player does not play themselves and
--  a player only faces an opponent once.

CREATE TABLE matches (
    id SERIAL primary key,
    winner_id integer NOT NULL references players(id),
    loser_id integer NOT NULL references players(id),
    constraint self_cannot_face_self CHECK (winner_id != loser_id)
);
CREATE UNIQUE INDEX match_uniqueness ON matches(least(winner_id,loser_id),greatest(winner_id,loser_id));


--  A view displaying total matches played by a player grouped by a player's ID.

CREATE VIEW completed_matches_by_players_id AS
    select tmp1.player_id, sum(tmp1.match) as matches_played from (
        select winner_id as player_id, 1 as match from matches
                        union all
                        select loser_id as player_id, 1 as match from matches
    ) tmp1 group by tmp1.player_id;


CREATE VIEW matches_won_by_players_id AS
    select winner_id as player_id, count(*) as matches_won from matches group by winner_id;