CREATE TABLE players (id serial primary key not null, username text unique not null, password text not null, firstname text, lastname text, grade_level integer);
CREATE TABLE gamestates (id serial primary key not null, player_id int not null references players(id), gamestate json not null, environment json not null);
CREATE TABLE sessions (id serial primary key not null, player_id int not null references players(id), session_token text not null, session_started timestamptz not null, last_used timestamptz not null);
