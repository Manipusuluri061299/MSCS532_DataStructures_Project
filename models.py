
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class InsurancePolicy:
    """Represents a fictional insurance policy."""

    policy_id: str
    customer_name: str
    coverage_type: str
    premium: Decimal
    status: str = "Active"

    def __post_init__(self):
        if not self.policy_id.strip():
            raise ValueError("Policy ID cannot be empty")

        if not self.customer_name.strip():
            raise ValueError("Customer name cannot be empty")

        if not self.coverage_type.strip():
            raise ValueError("Coverage type cannot be empty")

        if not isinstance(self.premium, Decimal):
            raise TypeError("Premium must be a Decimal")

        if not self.premium.is_finite() or self.premium < 0:
            raise ValueError(
                "Premium must be a finite non-negative amount"
            )

        if self.status not in {"Active", "Pending", "Cancelled"}:
            raise ValueError("Invalid policy status")
