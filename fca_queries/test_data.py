from datetime import date

# Full test case
FULL_TEST_COMPANY = {
    "name": "Example Financial Services Ltd",
    "firm_reference_number": "123456",
    "regulatory_status": "Authorized",
    "permissions": [
        "Retail Investment Management",
        "Insurance Distribution",
        "Electronic Money Institution",
        "Professional Trading Services"
    ],
    "appointed_representatives": ["AR Firm 1", "AR Firm 2"],
    "approved_individuals": ["John Doe - CEO", "Jane Smith - Compliance Officer"],
    "assets_under_management": 500000000,  # £500M
    "annual_revenue": 50000000,  # £50M
    "employee_count": 150,
    "country_operations": ["UK", "France", "Germany"],
    "date_authorized": date(2020, 1, 1)
}

# Minimal test case
MINIMAL_TEST_COMPANY = {
    "name": "Minimal Financial Ltd",
    "regulatory_status": "Registered",
    "permissions": ["Basic Investment Advice"]
}

# Invalid test case (should fail validation)
INVALID_TEST_COMPANY = {
    "firm_reference_number": "12345",  # Invalid format
    "regulatory_status": "Unknown"
    # Missing required name field
}
