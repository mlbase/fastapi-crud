create table api_user(
    id INTEGER primary key auto_increment,
    full_name varchar(100),
    email text,
    hashed_password text,
    is_active boolean,
    is_superuser boolean default=FALSE
)

create table item(
    id INTEGER primary key ,
    title VARCHAR(100),
    description text,
    owner_id INTEGER
);
alter table item
add foreign key (owner_id) references api_user(id)