# PDF Table Extraction & Search API

## Overview

PDF Table Extraction & Search API is a backend service built with FastAPI that enables users to upload PDF documents, automatically extract tabular data, store the extracted records in MongoDB, and perform powerful searches on the extracted data.

The system is designed for organizations and individuals who frequently work with large PDF reports containing structured tables and need a fast way to convert them into searchable datasets.

---

## Problem Statement

Many organizations receive reports in PDF format that contain thousands of rows of tabular data.

Common challenges include:

* Manual data entry into spreadsheets
* Difficulty searching specific records inside PDFs
* Large PDF files taking significant time to process
* Lack of real-time feedback during extraction
* Poor scalability when handling multiple documents

This project solves these problems by automatically extracting tables, storing them in a database, and providing flexible search capabilities.

---

## Features

### Authentication & User Management

* User registration
* User login/logout
* JWT authentication
* Password reset
* Protected routes

### PDF Processing

* Upload PDF documents
* Extract tabular data from multi-page PDFs
* Support for files containing hundreds of pages
* Optional header detection
* Real-time extraction progress tracking using WebSockets

### Data Storage

* Store extracted records in MongoDB
* Store document metadata in PostgreSQL
* Maintain ownership of uploaded documents

### Search Engine

Search by:

* Exact match (=)
* Contains
* Starts with
* Ends with
* Greater than (>)
* Less than (<)
* Greater than or equal (>=)
* Less than or equal (<=)

Pagination support included.

### Document Management

* View uploaded documents
* Retrieve document metadata
* Delete documents
* Remove associated MongoDB collections

### Exporting

* Save extracted data to Excel
* Save extracted data to MongoDB

### Real-Time Updates

WebSocket support provides:

* Current page being processed
* Total pages
* Processing percentage
* Completion notifications
* Error notifications

---

## Technology Stack

### Backend

* FastAPI
* Python 3.12+

### Databases

* PostgreSQL
* MongoDB

### ORM

* SQLAlchemy

### Authentication

* JWT
* Argon2 Password Hashing

### PDF Processing

* pdfplumber
* pandas

### Realtime Communication

* WebSockets

### Email Services

* SMTP
* FastAPI Background Tasks

---

## Project Architecture

```text
Client
   |
   v
FastAPI
   |
   +---- Authentication
   |
   +---- PDF Extraction
   |
   +---- Search Engine
   |
   +---- WebSocket Progress Tracking
   |
   +---- PostgreSQL (Users, Metadata)
   |
   +---- MongoDB (Extracted Records)
```

## Why MongoDB?

PDF tables often have varying structures.

MongoDB allows:

* Dynamic schemas
* Fast document retrieval
* Flexible querying
* Easier storage of extracted records

while PostgreSQL handles relational data such as users, payments, subscriptions, and uploaded document metadata.

---

## API Modules

### User Routes

```text
/api/v1/user
```

### PDF Routes

```text
/api/v1/pdf
```

### Document Routes

```text
/api/v1/documents
```

### Payment Routes

```text
/api/v1/payments
```

---

## Future Improvements

* OCR support for scanned PDFs
* AI-powered table detection
* CSV export
* Role-based access control
* Document sharing
* Search analytics
* Background job queues using Celery

---

## Author

Built as a scalable PDF extraction and search platform using FastAPI, PostgreSQL, MongoDB, and WebSockets.
