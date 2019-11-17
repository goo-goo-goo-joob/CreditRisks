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

CREATE OR REPLACE VIEW risks.calcModelsView AS
SELECT calcModels.id                 AS id,
       calcModels.name               AS name,
       calcClasses.name              AS class_name,
       TO_BASE64(calcModels.archive) AS archive
FROM risks.calcModels
         JOIN risks.calcClasses ON calcModels.class_id = calcClasses.id;

show processlist