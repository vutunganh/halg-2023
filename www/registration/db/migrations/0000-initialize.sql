CREATE TABLE participant (
  id              SERIAL    PRIMARY KEY,
  name            TEXT      NOT NULL,
  surname         TEXT,
  email           TEXT      NOT NULL UNIQUE,
  affiliation     TEXT,
  address         TEXT      NOT NULL,
  city            TEXT      NOT NULL,
  country         TEXT      NOT NULL,
  zip_code        TEXT,
  vat_tax_no      TEXT,
  is_student      BOOLEAN   DEFAULT FALSE,
  date_registered TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
