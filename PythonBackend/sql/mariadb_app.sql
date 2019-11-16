CREATE TABLE risks.calcClasses
(
    id   SERIAL PRIMARY KEY,
    name VARCHAR(20) UNIQUE NOT NULL
) ENGINE = INNODB;
CREATE TABLE risks.calcModels
(
    id       SERIAL PRIMARY KEY,
    name     VARCHAR(100)    NOT NULL,
    class_id BIGINT UNSIGNED NOT NULL,
    archive  LONGBLOB        NOT NULL,
    CONSTRAINT class_id_fkey FOREIGN KEY (class_id) REFERENCES risks.calcClasses (id)
) ENGINE = INNODB;
