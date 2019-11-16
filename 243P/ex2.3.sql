-- 1
INSERT INTO terms
	(terms_id,terms_description,terms_due_days)
VALUES
	(6,'Net due 120 days', 120);
-- 2
UPDATE terms
SET	terms_description = 'Net due 125 days', terms_due_days = 125
WHERE terms_id = 6;
-- 3
DELETE from terms
WHERE terms_id = 6;
-- 4
INSERT INTO invoices
VALUES (DEFAULT,32,'AX-014-027', '2018-08-01', 434.58, 0, 0, 2, '2018-08-31', NULL);
-- 5
SELECT *
FROM invoices
WHERE invoice_id = 115;
-- 6
INSERT INTO invoice_line_items 
VALUES
    (115, 1, 160, 180.23, 'Hard drive'),
    (115, 2, 527, 254.35, 'Exchange Server update');
-- 7
UPDATE invoices
SET credit_total = invoice_total * 0.1,
    payment_total = invoice_total - credit_total
WHERE invoice_id = 115;
-- 8
UPDATE Vendors
SET default_account_number = 403
WHERE vendor_id = 44;
-- 9
UPDATE Invoices
SET terms_id = 2
WHERE vendor_id IN
    (SELECT vendor_id
     FROM Vendors
     WHERE default_terms_id = 2);
     
DELETE FROM invoice_line_items
WHERE invoice_id = 115;

DELETE FROM invoices
WHERE invoice_id = 115;


