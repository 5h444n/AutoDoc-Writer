-- This file contains common injection attack vectors
SELECT * FROM users WHERE username = 'admin' --' AND password = 'password';
DROP TABLE students; --
UNION SELECT credit_card FROM payments;