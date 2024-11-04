# FCA Company Categorization API Specification

## API Endpoints

### 1. Authentication
```http
POST /token
Content-Type: application/x-www-form-urlencoded

username=user&password=pass
```

### 2. Company Categorization
```http
POST /categorize
Authorization: Bearer <token>
Content-Type: application/json

{
    "name": "Company Name",
    "firm_reference_number": "123456",
    "regulatory_status": "Authorized",
    "permissions": ["investment management", "retail clients"],
    "assets_under_management": 1000000000,
    "employee_count": 250,
    "country_operations": ["UK"]
}
```

## Data Models

### Input Model (FCACompanyInfo)
```python
class FCACompanyInfo(BaseModel):
    name: str
    firm_reference_number: Optional[str]
    regulatory_status: Optional[str]
    permissions: Optional[List[str]]
    assets_under_management: Optional[float]
    employee_count: Optional[int]
    country_operations: Optional[List[str]]
    date_authorized: Optional[date]
```

### Output Model (FCACategorization)
```python
class FCACategorization(BaseModel):
    smcr_category: SMCRCategory
    regulatory_status: RegulatoryStatus
    firm_type: FirmType
    business_activities: List[str]
    client_base: List[ClientType]
    size_and_complexity: SizeComplexity
    geographic_reach: GeographicReach
    ownership_structure: OwnershipStructure
    risk_profile: RiskProfile
    specialization: List[str]
    risk_score: float
    regulatory_implications: List[str]
```

## Business Logic

### 1. Permission Analysis
- Categorizes business activities
- Identifies specializations
- Maps to regulatory requirements

### 2. Risk Assessment
- Calculates risk scores
- Determines risk profile
- Evaluates complexity

### 3. Regulatory Implications
- Determines applicable regulations
- Identifies compliance requirements
- Assesses reporting obligations

## Response Examples

### Successful Categorization
```json
{
    "smcr_category": "Core",
    "regulatory_status": "Authorized",
    "firm_type": "Solo-regulated Firm",
    "business_activities": ["Investment Management"],
    "client_base": ["Retail"],
    "size_and_complexity": "Large",
    "geographic_reach": "Domestic",
    "ownership_structure": "Private",
    "risk_profile": "Medium",
    "specialization": ["Asset Management"],
    "risk_score": 75.5,
    "regulatory_implications": [
        "FCA Principles for Business compliance required",
        "Consumer Duty obligations apply"
    ]
}
```

### Error Response
```json
{
    "detail": "Firm Reference Number must be 6 digits"
}
```

## Validation Rules

1. Firm Reference Number
   - Must be 6 digits
   - Optional field

2. Permissions
   - List of strings
   - Case-insensitive matching
   - Optional field

3. Financial Metrics
   - Non-negative values
   - Optional fields

## Rate Limiting

- 100 requests per minute per authenticated user
- 10 requests per minute for authentication endpoints

## Security

1. Authentication Required
   - JWT token-based
   - 30-minute token expiration

2. Input Validation
   - Pydantic models
   - Custom validators

3. Error Handling
   - Detailed error messages
   - Appropriate status codes

## Future Enhancements

1. Additional Endpoints
   - Batch processing
   - Historical data
   - Analytics

2. Enhanced Features
   - Machine learning integration
   - Real-time updates
   - Advanced analytics

3. Integration Points
   - External data sources
   - Regulatory databases
   - Reporting systems
