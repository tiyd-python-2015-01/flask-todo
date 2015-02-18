drop table if exists users;
drop table if exists list;

create table users (
  username text primary key not null,
  password text not null
);

create table list (
  id integer primary key autoincrement,
  owner text not null,
  task text not null
);

create table done (
    id integer primary key autoincrement,
    owner text not null,
    task text not null
);
