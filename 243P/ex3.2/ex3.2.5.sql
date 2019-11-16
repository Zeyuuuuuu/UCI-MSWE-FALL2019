ALTER TABLE Committees
MODIFY committee_name VARCHAR(50) NOT NULL UNIQUE;


INSERT INTO Committees
VALUES (DEFAULT, 'Avengers');