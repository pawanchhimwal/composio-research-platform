"""Constants and Validation Enums for the Research Platform."""
from enum import Enum

class AuthMethod(str, Enum):
    OAUTH2 = "OAuth2"
    API_KEY = "API Key"
    BASIC_AUTH = "Basic Auth"
    BEARER_TOKEN = "Bearer Token"
    JWT = "JWT"
    SESSION = "Session"
    UNKNOWN = "Unknown"

class ApiType(str, Enum):
    REST = "REST"
    GRAPHQL = "GraphQL"
    SOAP = "SOAP"
    WEBHOOKS = "Webhooks"
    NONE = "None"
    UNKNOWN = "Unknown"

class Buildability(str, Enum):
    READY = "Ready Today"
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"
    IMPOSSIBLE = "Impossible"
    UNKNOWN = "Unknown"

class VerificationState(str, Enum):
    PENDING = "Pending"
    VERIFIED = "Verified"
    HUMAN_REVIEWED = "Human Reviewed"
    FAILED = "Failed"

class SelfServeStatus(str, Enum):
    FREE_TRIAL = "Free/Trial"
    PAID_PLAN = "Paid Plan"
    ADMIN_APPROVAL = "Admin Approval"
    SALES_GATED = "Partner/Sales Gated"
    UNKNOWN = "Unknown"
