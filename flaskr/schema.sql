DROP TABLE IF EXISTS _case;
DROP TABLE IF EXISTS _project;
DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
    
);


CREATE TABLE _project(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT UNIQUE NOT NULL
   
    
);

CREATE TABLE _case (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    _description TEXT UNIQUE NOT NULL,
    _project_id INTEGER NOT NULL,
    parent_id INTEGER,
    child_id INTEGER,
    
    FOREIGN KEY (_project_id) REFERENCES _project(id),
    
    FOREIGN KEY (parent_id) REFERENCES _case(id),
    FOREIGN KEY (child_id) REFERENCES _case(id),
    
);