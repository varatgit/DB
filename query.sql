CREATE TABLE transactions (
    transaction_id VARCHAR(255) PRIMARY KEY,
    transaction_date DATE NOT NULL,
    description TEXT,
    amount DECIMAL(10, 2) NOT NULL,
    type VARCHAR(20) -- 'Revenue' or 'Expense'
);

INSERT INTO transactions (transaction_id, transaction_date, description, amount, type) VALUES
('5a0e14a7-8f5b-4c6e-b8d9-2e1f6e0c4a7f', '2025-07-01', 'Software License Sale', 5000.00, 'Revenue'),
('3c4d7e89-1a2b-3c4d-5e6f-7g8h9i0j1k2l', '2025-07-02', 'Office Supplies', 150.75, 'Expense'),
('f8e7d6c5-4b3a-2d1e-0f9e-8d7c6b5a4f3e', '2025-07-03', 'Consulting Services', 2500.00, 'Revenue'),
('1b2c3d4e-5f6g-7h8i-9j0k-1l2m3n4o5p6q', '2025-07-04', 'Employee Salaries', 3000.00, 'Expense'),
('8g9h0i1j-2k3l-4m5n-6o7p-8q9r0s1t2u3v', '2025-07-05', 'Subscription Fees', 75.50, 'Expense'),
('4a5b6c7d-8e9f-0a1b-2c3d-4e5f6a7b8c9d', '2025-07-06', 'Product Sale', 12000.00, 'Revenue');