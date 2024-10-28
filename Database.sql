SELECT * FROM room;
SELECT * FROM booking;
SELECT * FROM rating;
SELECT * FROM users;
INSERT INTO room (room_id, room_type, price, is_available, status) 
VALUES (6, 'Single', 1000, TRUE, 'available');

INSERT INTO room (room_id, room_type, price, is_available, status) 
VALUES (7, 'Double', 1500, TRUE, 'available');

INSERT INTO room (room_id, room_type, price, is_available, status) 
VALUES (8, 'Suite', 3000, TRUE, 'available');

INSERT INTO room (room_id, room_type, price, is_available, status) 
VALUES (9, 'Deluxe', 2500, TRUE, 'available');

INSERT INTO room (room_id, room_type, price, is_available, status) 
VALUES (10, 'Single', 1000, TRUE, 'available');

UPDATE room
SET price = 4000
WHERE room_id = 4;

CREATE TABLE Customer (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15) UNIQUE NOT NULL
);

CREATE TABLE Room (
    room_id SERIAL PRIMARY KEY,
    room_type VARCHAR(50),
    price NUMERIC(10, 2),
    is_available BOOLEAN DEFAULT TRUE
);

CREATE TABLE Booking (
    booking_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES Customer(customer_id),
    room_id INT REFERENCES Room(room_id),
    booking_date DATE DEFAULT CURRENT_DATE,
    check_in_date DATE,
    check_out_date DATE,
    status VARCHAR(50) DEFAULT 'Booked'
    is_completed BOOLEAN DEFAULT FALSE;

);


CREATE TABLE Rating (
    rating_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES Customer(customer_id),
    rating INT CHECK (rating >= 1 AND rating <= 5),
    feedback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



