USE `nasa_judge`;
CREATE TABLE wireguard_profiles (
    profile_id SERIAL PRIMARY KEY,
    valid BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
