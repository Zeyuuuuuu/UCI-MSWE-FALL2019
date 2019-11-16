USE ex;

INSERT INTO members
	VALUES (DEFAULT, 'Tony', 'Stark', '3800 ParkView Ln', 'Irvine', 'CA', '949-111-2222');
INSERT INTO members
	VALUES (DEFAULT, 'Peter', 'Parker', '3900 ParkView Ln', 'Irvine', 'CA', '949-222-3333');

INSERT INTO committees
	VALUES (DEFAULT, 'Avengers');
INSERT INTO committees
	VALUES (DEFAULT, 'Stark Industries');

INSERT INTO members_committees
	VALUES (1, 2);
INSERT INTO members_committees
	VALUES (2, 1);
INSERT INTO members_committees
	VALUES (2, 2);

SELECT c.committee_name, m.last_name, m.first_name
FROM committees c INNER JOIN members_committees mc
    ON c.committee_id = mc.committee_id
  INNER JOIN members m
    ON mc.member_id = m.member_id
ORDER BY c.committee_name, m.last_name, m.first_name;