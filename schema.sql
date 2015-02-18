drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  task text not null
);
