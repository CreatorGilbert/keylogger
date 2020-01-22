/* 
 * Code for this file taken and adapted from:
 * http://flask.pocoo.org/docs/1.0/tutorial/database/
 */
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS trojan;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE trojan (
  id INTEGER UNIQUE PRIMARY KEY,
  last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  status BOOL NOT NULL DEFAULT 0,
  ip TEXT NOT NULL,
  port INTEGER NOT NULL default 50000,
  logged_text TEXT NOT NULL DEFAULT 'No logged text.'
);
