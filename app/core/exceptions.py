class TravelPlannerException(Exception):
    """Base exception for travel planner."""
    pass


class ResourceNotFound(TravelPlannerException):
    """Resource not found."""
    pass


class BusinessRuleViolation(TravelPlannerException):
    """Business rule violation."""
    pass


class ExternalAPIError(TravelPlannerException):
    """External API error."""
    pass
