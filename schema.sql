-- ====================================================
-- DATABASE SCHEMA: PAINT HOUSE MANAGEMENT SYSTEM
-- ====================================================

-- 1. USERS TABLE
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT 0,
    upi_id VARCHAR(100) DEFAULT 'paint.house@upi',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. COLOR ITEMS & PRICING TABLE
CREATE TABLE IF NOT EXISTS color_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL,
    hex_code VARCHAR(10) NOT NULL,
    category VARCHAR(20) DEFAULT 'WHEEL',
    price_per_room DECIMAL(10,2) DEFAULT 499.00
);

-- 3. BOOKINGS TABLE
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    id_proof VARCHAR(50) DEFAULT 'Not Provided',
    color VARCHAR(50) NOT NULL,
    design_style VARCHAR(50) NOT NULL,
    booking_date DATE NOT NULL,
    booking_time TIME NOT NULL,
    rooms INTEGER DEFAULT 1,
    notes TEXT,
    amount DECIMAL(10,2) DEFAULT 499.00,
    payment_mode VARCHAR(20) DEFAULT 'COD',
    payment_status VARCHAR(20) DEFAULT 'PENDING',
    payment_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 4. REVIEWS TABLE
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    rating INTEGER NOT NULL,
    comment TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);