import copy
import random
from pathlib import Path

import pytest
import yaml

from pycrate_asn1rt.err import ASN1ObjValErr

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def tim_full_data():
    with open(FIXTURES_DIR / "TIM_full.yaml", "r") as f:
        data = yaml.safe_load(f)
    return data


class TestValidFullMessage:
    def test_valid_full_message(self, validator, tim_full_data):
        errors = validator.validate(tim_full_data)
        assert errors == [], f"Expected no errors but got: {errors}"


class TestMissingRequiredKeys:
    @pytest.fixture
    def data(self, tim_full_data):
        return copy.deepcopy(tim_full_data)

    def _inner(self, data):
        return data["value"]["TravelerInformation"]

    def _frame(self, data):
        return self._inner(data)["dataFrames"][0]

    def test_missing_msgCnt(self, validator, data):
        del self._inner(data)["msgCnt"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "msgCnt" in e.msg
            for e in errors
        )

    def test_missing_dataFrames(self, validator, data):
        del self._inner(data)["dataFrames"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "dataFrames" in e.msg
            for e in errors
        )

    def test_missing_frame_doNotUse1(self, validator, data):
        del self._frame(data)["doNotUse1"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "doNotUse1" in e.msg
            for e in errors
        )

    def test_missing_frame_frameType(self, validator, data):
        del self._frame(data)["frameType"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "frameType" in e.msg
            for e in errors
        )

    def test_missing_frame_msgId(self, validator, data):
        del self._frame(data)["msgId"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "msgId" in e.msg
            for e in errors
        )

    def test_missing_frame_startTime(self, validator, data):
        del self._frame(data)["startTime"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "startTime" in e.msg
            for e in errors
        )

    def test_missing_frame_durationTime(self, validator, data):
        del self._frame(data)["durationTime"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "durationTime" in e.msg
            for e in errors
        )

    def test_missing_frame_priority(self, validator, data):
        del self._frame(data)["priority"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "priority" in e.msg
            for e in errors
        )

    def test_missing_frame_doNotUse2(self, validator, data):
        del self._frame(data)["doNotUse2"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "doNotUse2" in e.msg
            for e in errors
        )

    def test_missing_frame_regions(self, validator, data):
        del self._frame(data)["regions"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "regions" in e.msg
            for e in errors
        )

    def test_missing_frame_doNotUse3(self, validator, data):
        del self._frame(data)["doNotUse3"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "doNotUse3" in e.msg
            for e in errors
        )

    def test_missing_frame_doNotUse4(self, validator, data):
        del self._frame(data)["doNotUse4"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "doNotUse4" in e.msg
            for e in errors
        )

    def test_missing_frame_content(self, validator, data):
        del self._frame(data)["content"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "content" in e.msg
            for e in errors
        )

    def test_missing_roadSignID_position(self, validator, data):
        del self._frame(data)["msgId"]["roadSignID"]["position"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "position" in e.msg
            for e in errors
        )

    def test_missing_roadSignID_viewAngle(self, validator, data):
        del self._frame(data)["msgId"]["roadSignID"]["viewAngle"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "viewAngle" in e.msg
            for e in errors
        )

    def test_missing_position_lat(self, validator, data):
        del self._frame(data)["msgId"]["roadSignID"]["position"]["lat"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "lat" in e.msg
            for e in errors
        )

    def test_missing_position_long(self, validator, data):
        del self._frame(data)["msgId"]["roadSignID"]["position"]["long"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "long" in e.msg
            for e in errors
        )


class TestInvalidValues:
    def test_invalid_values_all_required_fields(self, validator, tim_full_data):
        data = copy.deepcopy(tim_full_data)
        inner = data["value"]["TravelerInformation"]
        frame = inner["dataFrames"][0]

        inner["msgCnt"] = "bad"
        frame["doNotUse1"] = "bad"
        frame["frameType"] = "nonExistent"
        frame["startTime"] = "bad"
        frame["durationTime"] = "bad"
        frame["priority"] = "bad"
        frame["doNotUse2"] = "bad"
        frame["doNotUse3"] = "bad"
        frame["doNotUse4"] = "bad"
        frame["msgId"]["roadSignID"]["position"]["lat"] = "bad"
        frame["msgId"]["roadSignID"]["position"]["long"] = "bad"
        frame["msgId"]["roadSignID"]["viewAngle"] = 99999

        errors = validator.validate(data)

        expected_keys = [
            "TravelerInformation.msgCnt",
            "TravelerInformation.dataFrames[0].doNotUse1",
            "TravelerInformation.dataFrames[0].frameType",
            "TravelerInformation.dataFrames[0].startTime",
            "TravelerInformation.dataFrames[0].durationTime",
            "TravelerInformation.dataFrames[0].priority",
            "TravelerInformation.dataFrames[0].doNotUse2",
            "TravelerInformation.dataFrames[0].doNotUse3",
            "TravelerInformation.dataFrames[0].doNotUse4",
            "TravelerInformation.dataFrames[0].msgId.roadSignID.position.lat",
            "TravelerInformation.dataFrames[0].msgId.roadSignID.position.long",
            "TravelerInformation.dataFrames[0].msgId.roadSignID.viewAngle",
        ]
        for expected_key in expected_keys:
            assert any(
                e.code == ASN1ObjValErr.INVALID_VALUE and e.key == expected_key
                for e in errors
            ), f"Expected INVALID_VALUE error for key '{expected_key}'"


class TestInvalidKeys:
    def test_invalid_keys_at_random_levels(self, validator, tim_full_data):
        data = copy.deepcopy(tim_full_data)
        inner = data["value"]["TravelerInformation"]
        frame = inner["dataFrames"][0]

        rng = random.Random(42)

        targets = [
            inner,
            frame,
            frame["msgId"]["roadSignID"],
            frame["msgId"]["roadSignID"]["position"],
            frame["regions"][0],
            frame["regions"][0]["anchor"],
            frame["regions"][0]["description"]["path"],
            frame["regions"][0]["description"]["path"]["offset"]["xy"]["nodes"][0],
            frame["regions"][0]["description"]["path"]["offset"]["xy"]["nodes"][0][
                "delta"
            ]["node-XY6"],
            inner,
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
