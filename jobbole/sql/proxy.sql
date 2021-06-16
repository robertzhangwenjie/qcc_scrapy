create table proxy_ip
(
    id         int auto_increment,
    proxy_addr varchar(50) null,
    constraint proxy_ip_id_uindex
        unique (id),
    constraint proxy_ip_proxy_addr_uindex
        unique (proxy_addr)
);

alter table proxy_ip
    add primary key (id);

