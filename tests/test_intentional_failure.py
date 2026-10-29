import os
import pytest


def test_controlled_intentional_release_barrier():
    """
    Demonstrates that a failing test assertion stops the release pipeline.
    Triggered when BLOCK_RELEASE=true is set.
    """
    should_fail = os.getenv("BLOCK_RELEASE", "false").lower() == "true"
    if should_fail:
        pytest.fail("VERIFIED SAFETY GATE: Intentional test failure halted deployment pipeline.")
    assert True