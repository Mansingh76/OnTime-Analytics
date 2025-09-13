CREATE TABLE IF NOT EXISTS stops (
    stop_id INT PRIMARY KEY,
    name VARCHAR(100),
    lat FLOAT,
    lon FLOAT
);

CREATE TABLE IF NOT EXISTS routes (
    route_id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS arrivals (
    route_id INT,
    stop_id INT,
    scheduled_time TIMESTAMP,
    actual_time TIMESTAMP,
    delay_minutes FLOAT
);
