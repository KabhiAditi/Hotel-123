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

