CREATE TABLE user (
    id BIGSERIAL PRIMARY KEY,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE user_info(
    user_info_id BIGSERIAL PRIMARY KEY,
    id BIGINT NOT NULL,
    age INT,
    gender VARCHAR(10),
    FOREIGN KEY (id) REFERENCES user(id) ON DELETE CASCADE
);

CREATE TABLE tablename (
    
);

CREATE TABLE tablename (

);

--log daily food intake to track symptom reactions related to food
CREATE TABLE tablename (

);

CREATE TABLE tablename (

);
