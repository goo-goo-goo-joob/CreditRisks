CREATE DATABASE IF NOT EXISTS risks;
CREATE TABLE IF NOT EXISTS risks.companies
(
    inn    BIGINT PRIMARY KEY,
    name   varchar(100) not null,
    okpo   BIGINT       not null,
    okopf  BIGINT       not null,
    okfs   BIGINT       not null,
    okved  char(10)     not null,
    region TINYINT      not null

) ENGINE = INNODB;