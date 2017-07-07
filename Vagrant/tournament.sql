
CREATE TABLE players( player_name TEXT,
					  player_id SERIAL PRIMARY KEY);

CREATE TABLE standings(	player_id INTEGER REFERENCES players,
						wins INTEGER,
						matches INTEGER);

CREATE VIEW view_standings AS
	SELECT standings.player_id, players.player_name, standings.wins, 
			standings.matches
		FROM standings,  players
			WHERE standings.player_id = players.player_id;

CREATE VIEW ordered_standings AS
	SELECT standings.player_id, players.player_name, standings.wins, 
			standings.matches, 
			row_number() over (ORDER BY standings.wins) AS place
		FROM standings,  players
			WHERE standings.player_id = players.player_id;

