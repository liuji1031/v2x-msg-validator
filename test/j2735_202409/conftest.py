import copy
from pathlib import Path

import pytest
import yaml

from v2x_msg_validator.validator import V2XMessageValidator

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def validator():
    return V2XMessageValidator(revision="j2735_202409")


@pytest.fixture
def map_full_data():
    with open(FIXTURES_DIR / "MAP_full.yaml", "r") as f:
        data = yaml.safe_load(f)
    return data


@pytest.fixture
def map_full_inner(map_full_data):
    """Return the inner MapData dict (inside value.MapData) as a deep copy."""
    return copy.deepcopy(map_full_data)
