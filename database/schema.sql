CREATE TABLE countries (
    iso3 TEXT PRIMARY KEY,
    country TEXT,
    continent TEXT,
    population_count BIGINT,
    iso2 TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    country_flag TEXT
);

CREATE TABLE covid_cases (
    iso3 TEXT,
    date DATE NOT NULL,
    one_case_per_people BIGINT,
    one_death_per_people BIGINT,
    one_test_per_people BIGINT,
    active_per_one_million DOUBLE PRECISION,
    recovered_per_one_million DOUBLE PRECISION,
    critical_per_one_million DOUBLE PRECISION,
    cases BIGINT,
    today_cases BIGINT,
    deaths BIGINT,
    today_deaths BIGINT,
    recovered BIGINT,
    today_recovered BIGINT, 
    active_people BIGINT,
    critical BIGINT,
    cases_per_one_million BIGINT,
    deaths_per_one_million BIGINT,
    tests BIGINT,
    tests_per_one_million BIGINT,
    PRIMARY KEY (iso3, date),
    FOREIGN KEY (iso3) REFERENCES countries(iso3)
);

