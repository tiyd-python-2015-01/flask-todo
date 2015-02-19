drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  todo text not null
);
