
import unittest
from decimal import Decimal

from models import InsurancePolicy
from policy_manager import PolicyManager
from priority_queue import ReviewPriorityQueue


def sample_policy(policy_id="POL1001"):
    return InsurancePolicy(
        policy_id=policy_id,
        customer_name="Test Customer",
        coverage_type="General Liability",
        premium=Decimal("1500.00"),
    )


class TestPolicyManager(unittest.TestCase):

    def setUp(self):
        self.manager = PolicyManager()

    def test_add_and_lookup(self):
        self.manager.add_policy(sample_policy())
        policy = self.manager.get_policy("POL1001")
        self.assertEqual(policy.customer_name, "Test Customer")

    def test_duplicate_policy(self):
        self.manager.add_policy(sample_policy())
        with self.assertRaises(ValueError):
            self.manager.add_policy(sample_policy())

    def test_missing_policy(self):
        self.assertIsNone(self.manager.get_policy("UNKNOWN"))

    def test_update_policy(self):
        self.manager.add_policy(sample_policy())
        updated = self.manager.update_policy(
            "POL1001",
            premium=Decimal("1750.00"),
        )
        self.assertEqual(updated.premium, Decimal("1750.00"))

    def test_delete_policy(self):
        self.manager.add_policy(sample_policy())
        self.assertTrue(self.manager.delete_policy("POL1001"))
        self.assertIsNone(self.manager.get_policy("POL1001"))

    def test_review_priority(self):
        self.manager.add_policy(sample_policy("POL1001"))
        self.manager.add_policy(sample_policy("POL1002"))

        self.manager.schedule_review("POL1001", 3)
        self.manager.schedule_review("POL1002", 1)

        policy, priority = self.manager.process_next_review()
        self.assertEqual(policy.policy_id, "POL1002")
        self.assertEqual(priority, 1)

    def test_equal_priority_fifo(self):
        queue = ReviewPriorityQueue()
        queue.add_review("POL1001", 2)
        queue.add_review("POL1002", 2)

        self.assertEqual(queue.pop_next(), ("POL1001", 2))
        self.assertEqual(queue.pop_next(), ("POL1002", 2))

    def test_empty_review_queue(self):
        self.assertIsNone(self.manager.process_next_review())

    def test_deleted_policy_review(self):
        self.manager.add_policy(sample_policy())
        self.manager.schedule_review("POL1001", 1)
        self.manager.delete_policy("POL1001")
        self.assertIsNone(self.manager.process_next_review())

    def test_invalid_premium(self):
        with self.assertRaises(ValueError):
            InsurancePolicy(
                policy_id="POL1001",
                customer_name="Test Customer",
                coverage_type="General Liability",
                premium=Decimal("-50.00"),
            )

    def test_invalid_priority(self):
        queue = ReviewPriorityQueue()
        with self.assertRaises(ValueError):
            queue.add_review("POL1001", 0)

    def test_invalid_update(self):
        self.manager.add_policy(sample_policy())
        with self.assertRaises(ValueError):
            self.manager.update_policy("POL1001", policy_id="NEW")

    def test_missing_review_policy(self):
        with self.assertRaises(KeyError):
            self.manager.schedule_review("UNKNOWN", 1)

    def test_cancelled_policy_review(self):
        policy = sample_policy()
        policy.status = "Cancelled"
        self.manager.add_policy(policy)
        self.manager.schedule_review("POL1001", 1)
        self.assertIsNone(self.manager.process_next_review())


if __name__ == "__main__":
    unittest.main(verbosity=2)
