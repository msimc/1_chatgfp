from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Literal
from enum import Enum
from datetime import date

app = FastAPI(
    title="FCA Company Categorization API",
    description="API for categorizing FCA registered companies across multiple dimensions",
    version="1.0.0"
)

# Enums for fixed categories
class SMCRCategory(str, Enum):
    ENHANCED = "Enhanced"
    CORE = "Core"
    LIMITED_SCOPE = "Limited Scope"
    UNKNOWN = "Unknown"

class RegulatoryStatus(str, Enum):
    AUTHORIZED = "Authorized"
    REGISTERED = "Registered"
    APPOINTED_REPRESENTATIVE = "Appointed Representative"
    UNKNOWN = "Unknown"

class FirmType(str, Enum):
    SMCR_BANKING = "SMCR Banking Firm"
    SMCR_INSURANCE = "SMCR Insurance Firm"
    SOLO_REGULATED = "Solo-regulated Firm"
    UNKNOWN = "Unknown"

class ClientType(str, Enum):
    RETAIL = "Retail"
    PROFESSIONAL = "Professional"
    ELIGIBLE_COUNTERPARTIES = "Eligible Counterparties"

class SizeComplexity(str, Enum):
    SMALL = "Small"
    MEDIUM = "Medium"
    LARGE = "Large"
    UNKNOWN = "Unknown"

class GeographicReach(str, Enum):
    DOMESTIC = "Domestic"
    INTERNATIONAL = "International"
    UNKNOWN = "Unknown"

class OwnershipStructure(str, Enum):
    PUBLIC = "Public"
    PRIVATE = "Private"
    MUTUAL = "Mutual"
    UNKNOWN = "Unknown"

class RiskProfile(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    UNKNOWN = "Unknown"

# Input Models
class FCACompanyInfo(BaseModel):
    name: str
    firm_reference_number: Optional[str] = None
    regulatory_status: Optional[str] = None
    permissions: Optional[List[str]] = []
    appointed_representatives: Optional[List[str]] = []
    approved_individuals: Optional[List[str]] = []
    assets_under_management: Optional[float] = None
    annual_revenue: Optional[float] = None
    employee_count: Optional[int] = None
    country_operations: Optional[List[str]] = []
    date_authorized: Optional[date] = None

    @validator('firm_reference_number')
    def validate_frn(cls, v):
        if v and not (v.isdigit() and len(v) == 6):
            raise ValueError('Firm Reference Number must be 6 digits')
        return v

# Output Models
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
    risk_score: float = Field(..., ge=0, le=100)
    regulatory_implications: List[str]

# Business Logic
def analyze_permissions(permissions: List[str]) -> tuple[List[str], List[str]]:
    activities = []
    specializations = []
    
    permission_mappings = {
        'investment': {
            'activity': 'Investment Management',
            'specializations': ['Asset Management', 'Portfolio Management']
        },
        'insurance': {
            'activity': 'Insurance Services',
            'specializations': ['Insurance Distribution', 'Insurance Underwriting']
        },
        'mortgage': {
            'activity': 'Mortgage Services',
            'specializations': ['Mortgage Lending', 'Mortgage Administration']
        },
        'banking': {
            'activity': 'Banking Services',
            'specializations': ['Retail Banking', 'Commercial Banking']
        },
        'payment': {
            'activity': 'Payment Services',
            'specializations': ['Payment Processing', 'E-money Institution']
        },
        'crypto': {
            'activity': 'Crypto-Asset Services',
            'specializations': ['Crypto Trading', 'Digital Asset Custody']
        }
    }

    for permission in permissions:
        permission_lower = permission.lower()
        for key, value in permission_mappings.items():
            if key in permission_lower:
                activities.append(value['activity'])
                for spec in value['specializations']:
                    if spec.lower() in permission_lower:
                        specializations.append(spec)

    return list(set(activities)), list(set(specializations))

def calculate_risk_metrics(company_info: FCACompanyInfo, size: SizeComplexity, 
                         activities: List[str], client_base: List[ClientType]) -> tuple[float, RiskProfile]:
    risk_score = 50  # Base score

    # Client base risk
    if ClientType.RETAIL in client_base:
        risk_score += 15
    if ClientType.PROFESSIONAL in client_base:
        risk_score += 10

    # Activity risk
    if 'Investment Management' in activities:
        risk_score += 10
    if 'Banking Services' in activities:
        risk_score += 15

    # Size risk
    if size == SizeComplexity.LARGE:
        risk_score += 15
    elif size == SizeComplexity.MEDIUM:
        risk_score += 10

    risk_score = min(risk_score, 100)

    # Risk profile determination
    if risk_score >= 70:
        risk_profile = RiskProfile.HIGH
    elif risk_score >= 40:
        risk_profile = RiskProfile.MEDIUM
    else:
        risk_profile = RiskProfile.LOW

    return risk_score, risk_profile

def determine_regulatory_implications(categorization: dict) -> List[str]:
    implications = ["FCA Principles for Business compliance required"]
    
    if categorization['size_and_complexity'] == SizeComplexity.LARGE:
        implications.extend([
            "Enhanced prudential requirements apply",
            "Additional reporting requirements"
        ])

    if ClientType.RETAIL in categorization['client_base']:
        implications.extend([
            "Consumer Duty obligations apply",
            "Retail client protection measures required"
        ])

    if categorization['risk_profile'] == RiskProfile.HIGH:
        implications.extend([
            "Enhanced risk management framework required",
            "More frequent supervisory interactions expected"
        ])

    return implications

# API Endpoints
@app.post("/categorize", response_model=FCACategorization)
async def categorize_company(company_info: FCACompanyInfo):
    try:
        # Analyze permissions
        activities, specializations = analyze_permissions(company_info.permissions or [])

        # Determine client base
        client_base = []
        permissions_str = " ".join(company_info.permissions or []).lower()
        if any(term in permissions_str for term in ['retail', 'consumer']):
            client_base.append(ClientType.RETAIL)
        if any(term in permissions_str for term in ['professional', 'institutional']):
            client_base.append(ClientType.PROFESSIONAL)
        if any(term in permissions_str for term in ['eligible counterparties', 'market counterparties']):
            client_base.append(ClientType.ELIGIBLE_COUNTERPARTIES)
        if not client_base:
            client_base = [ClientType.RETAIL]  # Default

        # Determine size
        size = SizeComplexity.UNKNOWN
        if company_info.assets_under_management or company_info.annual_revenue or company_info.employee_count:
            points = 0
            if company_info.assets_under_management:
                if company_info.assets_under_management >= 1_000_000_000:
                    points += 2
                elif company_info.assets_under_management >= 100_000_000:
                    points += 1
            if company_info.annual_revenue:
                if company_info.annual_revenue >= 100_000_000:
                    points += 2
                elif company_info.annual_revenue >= 10_000_000:
                    points += 1
            if company_info.employee_count:
                if company_info.employee_count >= 250:
                    points += 2
                elif company_info.employee_count >= 50:
                    points += 1
            
            if points >= 4:
                size = SizeComplexity.LARGE
            elif points >= 2:
                size = SizeComplexity.MEDIUM
            elif points >= 1:
                size = SizeComplexity.SMALL

        # Calculate risk metrics
        risk_score, risk_profile = calculate_risk_metrics(
            company_info, size, activities, client_base
        )

        # Create categorization
        categorization = {
            "smcr_category": SMCRCategory.CORE,  # Default
            "regulatory_status": RegulatoryStatus.AUTHORIZED if company_info.regulatory_status and 'authorized' in company_info.regulatory_status.lower() else RegulatoryStatus.UNKNOWN,
            "firm_type": FirmType.SOLO_REGULATED,  # Default
            "business_activities": activities,
            "client_base": client_base,
            "size_and_complexity": size,
            "geographic_reach": GeographicReach.INTERNATIONAL if len(company_info.country_operations or []) > 1 else GeographicReach.DOMESTIC,
            "ownership_structure": OwnershipStructure.UNKNOWN,  # Would need additional data
            "risk_profile": risk_profile,
            "specialization": specializations,
            "risk_score": risk_score,
            "regulatory_implications": []
        }

        # Add regulatory implications
        categorization["regulatory_implications"] = determine_regulatory_implications(categorization)

        return FCACategorization(**categorization)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
async def root():
    return {
        "message": "FCA Company Categorization API",
        "version": "1.0.0",
        "endpoints": {
            "/categorize": "POST - Categorize an FCA company",
            "/docs": "GET - API documentation"
        }
    }
