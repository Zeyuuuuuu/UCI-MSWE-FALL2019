ALTER TABLE Members
ADD annual_dues   DECIMAL(5,2)    DEFAULT 52.50;
ALTER TABLE Members
ADD payment_date  DATE;