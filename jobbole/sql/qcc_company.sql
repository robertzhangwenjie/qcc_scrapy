create table qcc_company
(
    id               int auto_increment,
    name             varchar(50)  not null,
    leader           varchar(50)  null,
    phone            varchar(100) null,
    addr             tinytext     null,
    registry_date    varchar(50)  null,
    registry_capital varchar(50)  null,
    scope            longtext     null,
    ip               varchar(100) null,
    industry         varchar(200) null,
    constraint qcc_company_id_uindex
        unique (id),
    constraint qcc_company_name_uindex
        unique (name)
);

alter table qcc_company
    add primary key (id);

