import copy
from pathlib import Path

import pytest
import yaml

from v2x_msg_validator.validator import V2XMessageValidator


@pytest.fixture
def validator():
    return V2XMessageValidator(revision="j2735_202409")

@pytest.fixture
def fixtures_dir():
    return Path(__file__).parent / "fixtures"