import copy
import random
from pathlib import Path

import pytest
import yaml

from pycrate_asn1rt.err import ASN1ObjValErr

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def psm_full_data():
    with open(FIXTURES_DIR / "PSM_full.yaml", "r") as f:
        data = yaml.safe_load(f)
    return data


class TestValidFullMessage:
    def test_valid_full_message(self, validator, psm_full_data):
        errors = validator.validate(psm_full_data)
        assert errors == [], f"Expected no errors but got: {errors}"


class TestMissingRequiredKeys:
    @pytest.fixture
    def data(self, psm_full_data):
        return copy.deepcopy(psm_full_data)

    def _inner(self, data):
        return data["value"]["PersonalSafetyMessage"]

    def test_missing_basicType(self, validator, data):
        del self._inner(data)["basicType"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "basicType" in e.msg
            for e in errors
        )

    def test_missing_secMark(self, validator, data):
        del self._inner(data)["secMark"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "secMark" in e.msg
            for e in errors
        )

    def test_missing_msgCnt(self, validator, data):
        del self._inner(data)["msgCnt"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "msgCnt" in e.msg
            for e in errors
        )

    def test_missing_id(self, validator, data):
        del self._inner(data)["id"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "id" in e.msg
            for e in errors
        )

    def test_missing_position(self, validator, data):
        del self._inner(data)["position"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "position" in e.msg
            for e in errors
        )

    def test_missing_accuracy(self, validator, data):
        del self._inner(data)["accuracy"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "accuracy" in e.msg
            for e in errors
        )

    def test_missing_speed(self, validator, data):
        del self._inner(data)["speed"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "speed" in e.msg
            for e in errors
        )

    def test_missing_heading(self, validator, data):
        del self._inner(data)["heading"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "heading" in e.msg
            for e in errors
        )

    def test_missing_position_lat(self, validator, data):
        del self._inner(data)["position"]["lat"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "lat" in e.msg
            for e in errors
        )

    def test_missing_position_long(self, validator, data):
        del self._inner(data)["position"]["long"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "long" in e.msg
            for e in errors
        )

    def test_missing_accuracy_semiMajor(self, validator, data):
        del self._inner(data)["accuracy"]["semiMajor"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "semiMajor" in e.msg
            for e in errors
        )

    def test_missing_accuracy_semiMinor(self, validator, data):
        del self._inner(data)["accuracy"]["semiMinor"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "semiMinor" in e.msg
            for e in errors
        )

    def test_missing_accuracy_orientation(self, validator, data):
        del self._inner(data)["accuracy"]["orientation"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "orientation" in e.msg
            for e in errors
        )

    def test_missing_accelSet_long(self, validator, data):
        del self._inner(data)["accelSet"]["long"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "long" in e.msg
            for e in errors
        )

    def test_missing_accelSet_lat(self, validator, data):
        del self._inner(data)["accelSet"]["lat"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "lat" in e.msg
            for e in errors
        )

    def test_missing_accelSet_vert(self, validator, data):
        del self._inner(data)["accelSet"]["vert"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "vert" in e.msg
            for e in errors
        )

    def test_missing_accelSet_yaw(self, validator, data):
        del self._inner(data)["accelSet"]["yaw"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "yaw" in e.msg
            for e in errors
        )

    def test_missing_pathPrediction_radiusOfCurve(self, validator, data):
        del self._inner(data)["pathPrediction"]["radiusOfCurve"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY
            and "radiusOfCurve" in e.msg
            for e in errors
        )

    def test_missing_pathPrediction_confidence(self, validator, data):
        del self._inner(data)["pathPrediction"]["confidence"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "confidence" in e.msg
            for e in errors
        )


class TestInvalidValues:
    def test_invalid_values_all_required_fields(self, validator, psm_full_data):
        data = copy.deepcopy(psm_full_data)
        inner = data["value"]["PersonalSafetyMessage"]

        inner["basicType"] = "nonExistent"
        inner["secMark"] = "bad"
        inner["msgCnt"] = "bad"
        inner["id"] = "000"
        inner["position"]["lat"] = "bad"
        inner["position"]["long"] = "bad"
        inner["accuracy"]["semiMajor"] = "bad"
        inner["accuracy"]["semiMinor"] = "bad"
        inner["accuracy"]["orientation"] = "bad"
        inner["speed"] = "bad"
        inner["heading"] = "bad"

        errors = validator.validate(data)

        expected_keys = [
            "PersonalSafetyMessage.basicType",
            "PersonalSafetyMessage.secMark",
            "PersonalSafetyMessage.msgCnt",
            "PersonalSafetyMessage.id",
            "PersonalSafetyMessage.position.lat",
            "PersonalSafetyMessage.position.long",
            "PersonalSafetyMessage.accuracy.semiMajor",
            "PersonalSafetyMessage.accuracy.semiMinor",
            "PersonalSafetyMessage.accuracy.orientation",
            "PersonalSafetyMessage.speed",
            "PersonalSafetyMessage.heading",
        ]
        for expected_key in expected_keys:
            assert any(
                e.code == ASN1ObjValErr.INVALID_VALUE and e.key == expected_key
                for e in errors
            ), f"Expected INVALID_VALUE error for key '{expected_key}'"


class TestInvalidKeys:
    def test_invalid_keys_at_random_levels(self, validator, psm_full_data):
        data = copy.deepcopy(psm_full_data)
        inner = data["value"]["PersonalSafetyMessage"]

        rng = random.Random(42)

        targets = [
            inner,
            inner["position"],
            inner["accuracy"],
            inner["accelSet"],
            inner["pathPrediction"],
            inner,
            inner["position"],
            inner["accuracy"],
            inner["accelSet"],
            inner["pathPrediction"],
        ]

        rng.shuffle(targets)

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
