
from dataclasses import replace

from models import InsurancePolicy
from priority_queue import ReviewPriorityQueue


class PolicyManager:
    """Manage policies and their review requests."""

    def __init__(self):
        self._policies = {}
        self._reviews = ReviewPriorityQueue()

    def add_policy(self, policy):
        if not isinstance(policy, InsurancePolicy):
            raise TypeError("Expected an InsurancePolicy object")

        if policy.policy_id in self._policies:
            raise ValueError("Policy ID already exists")

        self._policies[policy.policy_id] = replace(policy)

    def get_policy(self, policy_id):
        policy = self._policies.get(policy_id)
        return replace(policy) if policy is not None else None
    
    def update_policy(self, policy_id, /, **changes):
        if policy_id not in self._policies:
            raise KeyError("Policy not found")

        allowed_fields = {
            "customer_name",
            "coverage_type",
            "premium",
            "status",
        }

        if not changes or not set(changes).issubset(allowed_fields):
            raise ValueError("Invalid update fields")

        updated = replace(self._policies[policy_id], **changes)
        self._policies[policy_id] = updated
        return replace(updated)

    def delete_policy(self, policy_id):
        return self._policies.pop(policy_id, None) is not None

    def schedule_review(self, policy_id, priority):
        if policy_id not in self._policies:
            raise KeyError("Cannot review a missing policy")

        self._reviews.add_review(policy_id, priority)

    def process_next_review(self):
        while len(self._reviews) > 0:
            review = self._reviews.pop_next()
            policy_id, priority = review

            policy = self._policies.get(policy_id)

            if policy is not None and policy.status != "Cancelled":
                return policy, priority

        return None

    def policy_count(self):
        return len(self._policies)


if __name__ == "__main__":
    from decimal import Decimal

    manager = PolicyManager()

    manager.add_policy(
        InsurancePolicy(
            policy_id="POL1001",
            customer_name="Customer A",
            coverage_type="General Liability",
            premium=Decimal("1250.00"),
        )
    )

    manager.add_policy(
        InsurancePolicy(
            policy_id="POL1002",
            customer_name="Customer B",
            coverage_type="Commercial Auto",
            premium=Decimal("2100.00"),
        )
    )

    manager.schedule_review("POL1001", priority=2)
    manager.schedule_review("POL1002", priority=1)

    print("Total policies:", manager.policy_count())
    print("Policy lookup:", manager.get_policy("POL1001"))
    print("Next review:", manager.process_next_review())
