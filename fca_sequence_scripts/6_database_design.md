# Database Design and Integration

## Overview
This document outlines the database design and integration plan for the FCA Company Categorization API.

## Database Technology
- PostgreSQL for robust relational data management
- SQLAlchemy as ORM
- Alembic for migrations

## Schema Design

### 1. Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    disabled BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### 2. Companies Table
```sql
CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    firm_reference_number CHAR(6) UNIQUE,
    regulatory_status VARCHAR(50),
    assets_under_management DECIMAL,
    annual_revenue DECIMAL,
    employee_count INTEGER,
    date_authorized DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### 3. Permissions Table
```sql
CREATE TABLE permissions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### 4. Company_Permissions Table
```sql
CREATE TABLE company_permissions (
    company_id INTEGER REFERENCES companies(id),
    permission_id INTEGER REFERENCES permissions(id),
    granted_date DATE,
    PRIMARY KEY (company_id, permission_id)
);
```

### 5. Categorizations Table
```sql
CREATE TABLE categorizations (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id),
    smcr_category VARCHAR(50) NOT NULL,
    firm_type VARCHAR(50) NOT NULL,
    size_complexity VARCHAR(50) NOT NULL,
    geographic_reach VARCHAR(50) NOT NULL,
    ownership_structure VARCHAR(50) NOT NULL,
    risk_profile VARCHAR(50) NOT NULL,
    risk_score DECIMAL NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### 6. Regulatory_Implications Table
```sql
CREATE TABLE regulatory_implications (
    id SERIAL PRIMARY KEY,
    categorization_id INTEGER REFERENCES categorizations(id),
    implication TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

## SQLAlchemy Models

### Base Configuration
```python
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()
```

### Model Examples
```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    disabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    firm_reference_number = Column(String, unique=True, index=True)
    permissions = relationship("Permission", secondary="company_permissions")
    categorizations = relationship("Categorization", back_populates="company")
```

## Database Integration Steps

### 1. Setup
1. Install dependencies
   ```bash
   pip install sqlalchemy psycopg2-binary alembic
   ```

2. Configure database URL
   ```python
   DATABASE_URL = "postgresql://user:password@localhost/dbname"
   ```

### 2. Migration Management
1. Initialize Alembic
   ```bash
   alembic init alembic
   ```

2. Create migration script
   ```bash
   alembic revision --autogenerate -m "Initial migration"
   ```

3. Run migrations
   ```bash
   alembic upgrade head
   ```

### 3. Database Session Management
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## API Integration

### 1. Dependency Injection
```python
@app.post("/categorize")
async def categorize_company(
    company_info: FCACompanyInfo,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Database operations
```

### 2. CRUD Operations
```python
def create_company(db: Session, company: CompanyCreate):
    db_company = Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company
```

## Testing Strategy

### 1. Test Database
```python
TEST_DATABASE_URL = "postgresql://test_user:test_pass@localhost/test_db"

@pytest.fixture
def test_db():
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
```

### 2. Database Tests
```python
def test_create_company(test_db):
    company_data = {
        "name": "Test Company",
        "firm_reference_number": "123456"
    }
    company = create_company(test_db, CompanyCreate(**company_data))
    assert company.name == "Test Company"
```

## Performance Considerations

1. Indexing Strategy
   - Primary keys
   - Foreign keys
   - Frequently queried fields

2. Query Optimization
   - Eager loading
   - Query caching
   - Connection pooling

3. Data Management
   - Regular maintenance
   - Backup strategy
   - Data archival

## Security Measures

1. Data Protection
   - Encrypted connections
   - Password hashing
   - Data sanitization

2. Access Control
   - User permissions
   - Row-level security
   - Audit logging

## Monitoring

1. Database Metrics
   - Connection pool status
   - Query performance
   - Resource utilization

2. Error Tracking
   - Failed operations
   - Connection issues
   - Performance bottlenecks

## Next Steps

1. Implementation
   - Set up PostgreSQL
   - Create database models
   - Implement migrations
   - Update API endpoints

2. Testing
   - Unit tests
   - Integration tests
   - Performance testing

3. Documentation
   - API updates
   - Database schema
   - Deployment guide
