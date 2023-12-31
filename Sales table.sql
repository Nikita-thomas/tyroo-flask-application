-- Create Sales table
CREATE TABLE IF NOT EXISTS Sales (
    SaleID INT AUTO_INCREMENT PRIMARY KEY,
    ProductID INT NOT NULL,
    QuantitySold INT NOT NULL,
    SaleDate DATE NOT NULL
);

-- Insert initial rows into the Sales table
INSERT INTO Sales (ProductID, QuantitySold, SaleDate)
VALUES 
    (1, 15, '2023-01-03'),
    (2, 12, '2023-01-05'),
    (3, 8, '2023-01-04'),
    (4, 18, '2023-01-06');
