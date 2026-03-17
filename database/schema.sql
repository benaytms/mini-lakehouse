CREATE TABLE countries (
    iso3 TEXT PRIMARY KEY,
    country TEXT,
    continent TEXT,
    populationCount BIGINT,
    iso2 TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    countryFlag TEXT
);

CREATE TABLE covid_cases (
    iso3 TEXT,
    date DATE NOT NULL,
    oneCasePerPeople BIGINT,
    oneDeathPerPeople BIGINT,
    oneTestPerPeople BIGINT,
    activePerOneMillion DOUBLE PRECISION,
    recoveredPerOneMillion DOUBLE PRECISION,
    criticalPerOneMillion DOUBLE PRECISION,
    cases BIGINT,
    todayCases BIGINT,
    deaths BIGINT,
    todayDeaths BIGINT,
    recovered BIGINT,
    todayRecovered BIGINT, 
    activePeople BIGINT,
    critical BIGINT,
    casesPerOneMillion BIGINT,
    deathsPerOneMillion BIGINT,
    tests BIGINT,
    testsPerOneMillion BIGINT,
    PRIMARY KEY (iso3, date),
    FOREIGN KEY (iso3) REFERENCES countries(iso3)
);