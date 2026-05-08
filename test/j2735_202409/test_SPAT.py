import copy

import pytest
import yaml
from pycrate_asn1rt.err import ASN1ObjValErr


@pytest.fixture
def spat_full_data(fixtures_dir):
    with open(fixtures_dir / "SPAT.yaml", "r") as f:
        data = yaml.safe_load(f)
    return data


class TestValidFullMessage:
    def test_valid_full_message(self, validator, spat_full_data):
        errors = validator.validate(spat_full_data)
        assert errors == [], f"Expected no errors but got: {errors}"


class TestMissingRequiredKeys:
    """Each test removes one required key and asserts MISSING_MANDATORY_KEY error."""

    @pytest.fixture
    def data(self, spat_full_data):
        return copy.deepcopy(spat_full_data)

    def _inner(self, data):
        return data["value"]["SPAT"]

    def test_missing_intersections(self, validator, data):
        del self._inner(data)["intersections"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY
            and "intersections" in e.msg
            for e in errors
        )

    def test_missing_intersectionState_id(self, validator, data):
        del self._inner(data)["intersections"][0]["id"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "id" in e.msg
            for e in errors
        )

    def test_missing_intersectionState_revision(self, validator, data):
        del self._inner(data)["intersections"][0]["revision"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "revision" in e.msg
            for e in errors
        )

    def test_missing_intersectionState_status(self, validator, data):
        del self._inner(data)["intersections"][0]["status"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "status" in e.msg
            for e in errors
        )

    def test_missing_intersectionState_states(self, validator, data):
        del self._inner(data)["intersections"][0]["states"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "states" in e.msg
            for e in errors
        )

    def test_missing_intersectionReferenceID_id(self, validator, data):
        del self._inner(data)["intersections"][0]["id"]["id"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "id" in e.msg
            for e in errors
        )

    def test_missing_movementState_signalGroup(self, validator, data):
        del self._inner(data)["intersections"][0]["states"][0]["signalGroup"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "signalGroup" in e.msg
            for e in errors
        )

    def test_missing_movementState_stateTimeSpeed(self, validator, data):
        del self._inner(data)["intersections"][0]["states"][0]["state-time-speed"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY
            and "state-time-speed" in e.msg
            for e in errors
        )

    def test_missing_movementEvent_eventState(self, validator, data):
        del self._inner(data)["intersections"][0]["states"][0]["state-time-speed"][0][
            "eventState"
        ]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "eventState" in e.msg
            for e in errors
        )

    def test_missing_timeChangeDetails_minEndTime(self, validator, data):
        del self._inner(data)["intersections"][0]["states"][0]["state-time-speed"][0][
            "timing"
        ]["minEndTime"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "minEndTime" in e.msg
            for e in errors
        )

    def test_missing_advisorySpeed_type(self, validator, data):
        del self._inner(data)["intersections"][0]["states"][0]["state-time-speed"][0][
            "speeds"
        ][0]["type"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "type" in e.msg
            for e in errors
        )

    def test_missing_connectionManeuverAssist_connectionID(self, validator, data):
        del self._inner(data)["intersections"][0]["maneuverAssistList"][0][
            "connectionID"
        ]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY
            and "connectionID" in e.msg
            for e in errors
        )


class TestInvalidValues:
    """Mutate all required fields to invalid values and check all are reported."""

    def test_invalid_values_all_required_fields(self, validator, spat_full_data):
        data = copy.deepcopy(spat_full_data)
        inner = data["value"]["SPAT"]

        inner["intersections"][0]["id"]["id"] = "bad"
        inner["intersections"][0]["revision"] = "bad"
        inner["intersections"][0]["status"] = 12345
        inner["intersections"][0]["states"][0]["signalGroup"] = "bad"
        inner["intersections"][0]["states"][0]["state-time-speed"][0][
            "eventState"
        ] = "nonExistentState"
        inner["intersections"][0]["states"][0]["state-time-speed"][0]["timing"][
            "minEndTime"
        ] = "bad"
        inner["intersections"][0]["states"][0]["state-time-speed"][0]["speeds"][0][
            "type"
        ] = "nonExistentType"
        inner["intersections"][0]["maneuverAssistList"][0]["connectionID"] = "bad"

        errors = validator.validate(data)

        expected_keys = [
            "SPAT.intersections[0].id.id",
            "SPAT.intersections[0].revision",
            "SPAT.intersections[0].status",
            "SPAT.intersections[0].states[0].signalGroup",
            "SPAT.intersections[0].states[0].state-time-speed[0].eventState",
            "SPAT.intersections[0].states[0].state-time-speed[0].timing.minEndTime",
            "SPAT.intersections[0].states[0].state-time-speed[0].speeds[0].type",
            "SPAT.intersections[0].maneuverAssistList[0].connectionID",
        ]
        for expected_key in expected_keys:
            assert any(
                e.code == ASN1ObjValErr.INVALID_VALUE and e.key == expected_key
                for e in errors
            ), f"Expected INVALID_VALUE error for key '{expected_key}'"


class TestInvalidKeys:
    """Insert 10 bogus keys at random levels and assert all are detected."""

    def test_invalid_keys_at_random_levels(self, validator, spat_full_data):
        data = copy.deepcopy(spat_full_data)
        inner = data["value"]["SPAT"]

        targets = [
            inner,
            inner["intersections"][0],
            inner["intersections"][0]["id"],
            inner["intersections"][0]["states"][0],
            inner["intersections"][0]["states"][0]["state-time-speed"][0],
            inner["intersections"][0]["states"][0]["state-time-speed"][0]["timing"],
            inner["intersections"][0]["states"][0]["state-time-speed"][0]["speeds"][0],
            inner["intersections"][0]["maneuverAssistList"][0],
            inner["intersections"][0]["states"][0]["maneuverAssistList"][0],
            inner,
        ]

        bogus_keys = [f"bogus_key_{i}" for i in range(10)]
        for i, key in enumerate(bogus_keys):
            targets[i][key] = "invalid_value"

        errors = validator.validate(data)

        invalid_key_errors = [
            e for e in errors if e.code == ASN1ObjValErr.INVALID_KEY
        ]

        for key in bogus_keys:
            assert any(
                key in e.msg for e in invalid_key_errors
            ), f"Expected INVALID_KEY error reporting '{key}'"
