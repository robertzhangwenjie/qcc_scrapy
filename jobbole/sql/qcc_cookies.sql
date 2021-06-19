create table qcc_cookies
(
    id     int auto_increment,
    cookie longtext    not null,
    phone  varchar(30) not null,
    constraint qcc_cookies_id_uindex
        unique (id)
);

alter table qcc_cookies
    add primary key (id);

