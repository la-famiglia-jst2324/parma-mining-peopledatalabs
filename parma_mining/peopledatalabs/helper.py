"""Helper functions."""

from parma_mining.mining_common.exceptions import BaseError
from parma_mining.peopledatalabs.model import ErrorInfoModel


def collect_errors(company_id: str, errors: dict, e: BaseError):
    """Collect errors in required dict format."""
    errors[company_id] = ErrorInfoModel(
        error_type=e.__class__.__name__, error_description=e.message
    )
