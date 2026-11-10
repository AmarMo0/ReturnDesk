from typing import get_args

from agent.policy import ReplacementStatus, ReturnStatus
from agent.prompts import DECISION_MEANING


def test_every_policy_result_has_a_meaning():
    statuses = set(get_args(ReplacementStatus)) | set(get_args(ReturnStatus))
    assert statuses <= set(DECISION_MEANING)
