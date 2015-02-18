drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  id todo text not null
);
