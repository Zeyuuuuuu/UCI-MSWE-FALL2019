-- 1
SELECT *
FROM vendors INNER JOIN invoices
    ON vendors.vendor_id = invoices.vendor_id;
-- 2  
SELECT vendor_name, invoice_number, invoice_date,invoice_total-payment_total-credit_total AS balance_due
FROM vendors v INNER JOIN invoices i
  ON v.vendor_id = i.vendor_id
WHERE invoice_total-payment_total-credit_total <> 0
ORDER BY vendor_name;
-- 3
SELECT vendor_name, default_account_number AS default_account, account_description AS description
FROM vendors INNER JOIN general_ledger_accounts
  ON vendors.default_account_number = general_ledger_accounts.account_number
ORDER BY account_description, vendor_name;
-- 4
SELECT vendor_name, invoice_date, invoice_number, invoice_sequence AS li_sequence,line_item_amount AS li_amount
FROM vendors v INNER JOIN invoices i
  ON v.vendor_id = i.vendor_id
 INNER JOIN invoice_line_items li
   ON i.invoice_id = li.invoice_id
ORDER BY vendor_name, invoice_date, invoice_number, invoice_sequence;
-- 5
SELECT v1.vendor_id,v1.vendor_name,CONCAT(v1.vendor_contact_first_name,' ',v1.vendor_contact_last_name) AS contact_name
FROM Vendors v1 JOIN Vendors v2
	ON v1.vendor_id <> v2.vendor_id and v1.vendor_contact_last_name = v2.vendor_contact_last_name
ORDER BY v1.vendor_contact_last_name;
-- 6
SELECT g.account_number, g.account_description
FROM General_Ledger_Accounts g LEFT JOIN Invoice_Line_Items i
	ON g.account_number = i.account_number
WHERE i.invoice_id is NULL
Order by g.account_number;
-- 7
SELECT vendor_name,'CA'
	FROM vendors
	WHERE vendor_state = 'CA'
UNION
	SELECT vendor_name, 'Outside CA'
	FROM vendors
	WHERE vendor_state <> 'CA'
ORDER BY vendor_name
