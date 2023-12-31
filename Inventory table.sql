-- Create INVENTORY schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS INVENTORY;

-- Switch to the INVENTORY schema
USE INVENTORY;

-- Create Inventory table
CREATE TABLE IF NOT EXISTS Inventory (
    ProductID INT AUTO_INCREMENT PRIMARY KEY,
    ProductName VARCHAR(255) NOT NULL,
    QuantityInStock INT NOT NULL,
    UnitPrice DECIMAL(10, 2) NOT NULL
);

-- Insert initial rows into the Inventory table
INSERT INTO Inventory (ProductName, QuantityInStock, UnitPrice)
VALUES 
    ('Product A', 100, 19.99),
    ('Product B', 150, 29.99),
    ('Product C', 75, 14.99),
    ('Product D', 120, 24.99),
    ('Product E', 200, 9.99),
    ('Product F', 50, 34.99);
