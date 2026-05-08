import copy

import pytest
import yaml
from pycrate_asn1rt.err import ASN1ObjValErr


@pytest.fixture
def map_full_data(fixtures_dir):
    with open(fixtures_dir / "MAP.yaml", "r") as f:
        data = yaml.safe_load(f)
    return data


class TestValidFullMessage:
    def test_valid_full_message(self, validator, map_full_data):
        errors = validator.validate(map_full_data)
        assert errors == [], f"Expected no errors but got: {errors}"


class TestMissingRequiredKeys:
    """Each test removes one required key and asserts MISSING_MANDATORY_KEY error."""

    @pytest.fixture
    def data(self, map_full_data):
        return copy.deepcopy(map_full_data)

    def _inner(self, data):
        return data["value"]["MapData"]

    def test_missing_msgIssueRevision(self, validator, data):
        del self._inner(data)["msgIssueRevision"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY
            and "msgIssueRevision" in e.msg
            for e in errors
        )

    def test_missing_intersection_id(self, validator, data):
        del self._inner(data)["intersections"][0]["id"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "id" in e.msg
            for e in errors
        )

    def test_missing_intersection_revision(self, validator, data):
        del self._inner(data)["intersections"][0]["revision"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "revision" in e.msg
            for e in errors
        )

    def test_missing_intersection_refPoint(self, validator, data):
        del self._inner(data)["intersections"][0]["refPoint"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "refPoint" in e.msg
            for e in errors
        )

    def test_missing_intersection_laneSet(self, validator, data):
        del self._inner(data)["intersections"][0]["laneSet"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "laneSet" in e.msg
            for e in errors
        )

    def test_missing_intersectionReferenceID_id(self, validator, data):
        del self._inner(data)["intersections"][0]["id"]["id"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "id" in e.msg
            for e in errors
        )

    def test_missing_refPoint_lat(self, validator, data):
        del self._inner(data)["intersections"][0]["refPoint"]["lat"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "lat" in e.msg
            for e in errors
        )

    def test_missing_refPoint_long(self, validator, data):
        del self._inner(data)["intersections"][0]["refPoint"]["long"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "long" in e.msg
            for e in errors
        )

    def test_missing_genericLane_laneID(self, validator, data):
        del self._inner(data)["intersections"][0]["laneSet"][0]["laneID"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "laneID" in e.msg
            for e in errors
        )

    def test_missing_genericLane_laneAttributes(self, validator, data):
        del self._inner(data)["intersections"][0]["laneSet"][0]["laneAttributes"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY
            and "laneAttributes" in e.msg
            for e in errors
        )

    def test_missing_genericLane_nodeList(self, validator, data):
        del self._inner(data)["intersections"][0]["laneSet"][0]["nodeList"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "nodeList" in e.msg
            for e in errors
        )

    def test_missing_laneAttributes_directionalUse(self, validator, data):
        del self._inner(data)["intersections"][0]["laneSet"][0]["laneAttributes"][
            "directionalUse"
        ]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY
            and "directionalUse" in e.msg
            for e in errors
        )

    def test_missing_laneAttributes_sharedWith(self, validator, data):
        del self._inner(data)["intersections"][0]["laneSet"][0]["laneAttributes"][
            "sharedWith"
        ]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "sharedWith" in e.msg
            for e in errors
        )

    def test_missing_laneAttributes_laneType(self, validator, data):
        del self._inner(data)["intersections"][0]["laneSet"][0]["laneAttributes"][
            "laneType"
        ]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "laneType" in e.msg
            for e in errors
        )

    def test_missing_nodeXY_delta(self, validator, data):
        del self._inner(data)["intersections"][0]["laneSet"][0]["nodeList"]["nodes"][0][
            "delta"
        ]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "delta" in e.msg
            for e in errors
        )

    def test_missing_nodeOffsetPointXY_choice_key(self, validator, data):
        node = self._inner(data)["intersections"][0]["laneSet"][0]["nodeList"]["nodes"][
            0
        ]
        node["delta"] = {}
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.INVALID_STRUCTURE
            for e in errors
        )

    def test_missing_nodeXY32b_x(self, validator, data):
        del self._inner(data)["intersections"][0]["laneSet"][0]["nodeList"]["nodes"][0][
            "delta"
        ]["node-XY6"]["x"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "x" in e.msg
            for e in errors
        )

    def test_missing_nodeXY32b_y(self, validator, data):
        del self._inner(data)["intersections"][0]["laneSet"][0]["nodeList"]["nodes"][0][
            "delta"
        ]["node-XY6"]["y"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "y" in e.msg
            for e in errors
        )

    def test_missing_roadSegment_id(self, validator, data):
        del self._inner(data)["roadSegments"][0]["id"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "id" in e.msg
            for e in errors
        )

    def test_missing_roadSegment_revision(self, validator, data):
        del self._inner(data)["roadSegments"][0]["revision"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "revision" in e.msg
            for e in errors
        )

    def test_missing_roadSegment_refPoint(self, validator, data):
        del self._inner(data)["roadSegments"][0]["refPoint"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "refPoint" in e.msg
            for e in errors
        )

    def test_missing_roadSegment_roadLaneSet(self, validator, data):
        del self._inner(data)["roadSegments"][0]["roadLaneSet"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "roadLaneSet" in e.msg
            for e in errors
        )

    def test_missing_roadSegmentReferenceID_id(self, validator, data):
        del self._inner(data)["roadSegments"][0]["id"]["id"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "id" in e.msg
            for e in errors
        )

    def test_missing_connectingLane_lane(self, validator, data):
        del self._inner(data)["intersections"][0]["laneSet"][0]["connectsTo"][0][
            "connectingLane"
        ]["lane"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "lane" in e.msg
            for e in errors
        )

    def test_missing_connection_connectingLane(self, validator, data):
        del self._inner(data)["intersections"][0]["laneSet"][0]["connectsTo"][0][
            "connectingLane"
        ]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY
            and "connectingLane" in e.msg
            for e in errors
        )

    def test_missing_restrictionClassAssignment_id(self, validator, data):
        del self._inner(data)["restrictionList"][0]["id"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "id" in e.msg
            for e in errors
        )

    def test_missing_restrictionClassAssignment_users(self, validator, data):
        del self._inner(data)["restrictionList"][0]["users"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "users" in e.msg
            for e in errors
        )

    def test_missing_regulatorySpeedLimit_type(self, validator, data):
        del self._inner(data)["intersections"][0]["speedLimits"][0]["type"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "type" in e.msg
            for e in errors
        )

    def test_missing_regulatorySpeedLimit_speed(self, validator, data):
        del self._inner(data)["intersections"][0]["speedLimits"][0]["speed"]
        errors = validator.validate(data)
        assert any(
            e.code == ASN1ObjValErr.MISSING_MANDATORY_KEY and "speed" in e.msg
            for e in errors
        )


class TestInvalidValues:
    """Mutate all required fields to invalid values and check all are reported."""

    def test_invalid_values_all_required_fields(self, validator, map_full_data):
        data = copy.deepcopy(map_full_data)
        inner = data["value"]["MapData"]

        inner["msgIssueRevision"] = "abc"
        inner["intersections"][0]["revision"] = "xyz"
        inner["intersections"][0]["refPoint"]["lat"] = "not_a_number"
        inner["intersections"][0]["refPoint"]["long"] = "not_a_number"
        inner["intersections"][0]["id"]["id"] = "bad"
        inner["intersections"][0]["laneSet"][0]["laneID"] = "bad"
        inner["intersections"][0]["laneSet"][0]["laneAttributes"][
            "directionalUse"
        ] = 99999
        inner["intersections"][0]["laneSet"][0]["laneAttributes"]["sharedWith"] = 99999
        inner["intersections"][0]["laneSet"][0]["laneAttributes"]["laneType"] = {
            "vehicle": 12345
        }
        inner["intersections"][0]["laneSet"][0]["nodeList"]["nodes"][0]["delta"][
            "node-XY6"
        ]["x"] = "bad"
        inner["intersections"][0]["laneSet"][0]["nodeList"]["nodes"][0]["delta"][
            "node-XY6"
        ]["y"] = "bad"
        inner["intersections"][0]["laneSet"][0]["connectsTo"][0]["connectingLane"][
            "lane"
        ] = "bad"
        inner["intersections"][0]["speedLimits"][0]["speed"] = "bad"
        inner["intersections"][0]["speedLimits"][0]["type"] = "nonExistentType"
        inner["roadSegments"][0]["revision"] = "bad"
        inner["roadSegments"][0]["refPoint"]["lat"] = "bad"
        inner["roadSegments"][0]["id"]["id"] = "bad"
        inner["restrictionList"][0]["id"] = "bad"

        errors = validator.validate(data)

        expected_keys = [
            "MapData.msgIssueRevision",
            "MapData.intersections[0].id.id",
            "MapData.intersections[0].revision",
            "MapData.intersections[0].refPoint.lat",
            "MapData.intersections[0].refPoint.long",
            "MapData.intersections[0].speedLimits[0].type",
            "MapData.intersections[0].speedLimits[0].speed",
            "MapData.intersections[0].laneSet[0].laneID",
            "MapData.intersections[0].laneSet[0].laneAttributes.directionalUse",
            "MapData.intersections[0].laneSet[0].laneAttributes.sharedWith",
            "MapData.intersections[0].laneSet[0].laneAttributes.laneType.vehicle",
            "MapData.intersections[0].laneSet[0].nodeList.nodes[0].delta.node-XY6.x",
            "MapData.intersections[0].laneSet[0].nodeList.nodes[0].delta.node-XY6.y",
            "MapData.intersections[0].laneSet[0].connectsTo[0].connectingLane.lane",
            "MapData.roadSegments[0].id.id",
            "MapData.roadSegments[0].revision",
            "MapData.roadSegments[0].refPoint.lat",
            "MapData.restrictionList[0].id",
        ]
        for expected_key in expected_keys:
            assert any(
                e.code == ASN1ObjValErr.INVALID_VALUE and e.key == expected_key
                for e in errors
            ), f"Expected INVALID_VALUE error for key '{expected_key}'"


class TestInvalidKeys:
    """Insert 10 bogus keys at random levels and assert all are detected."""

    def test_invalid_keys_at_random_levels(self, validator, map_full_data):
        data = copy.deepcopy(map_full_data)
        inner = data["value"]["MapData"]

        targets = [
            inner,
            inner["intersections"][0],
            inner["intersections"][0]["id"],
            inner["intersections"][0]["refPoint"],
            inner["intersections"][0]["laneSet"][0],
            inner["intersections"][0]["laneSet"][0]["laneAttributes"],
            inner["intersections"][0]["laneSet"][0]["nodeList"]["nodes"][0],
            inner["intersections"][0]["laneSet"][0]["nodeList"]["nodes"][0]["delta"][
                "node-XY6"
            ],
            inner["intersections"][0]["laneSet"][0]["connectsTo"][0],
            inner["roadSegments"][0],
        ]

        bogus_keys = [f"bogus_key_{i}" for i in range(len(targets))]
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
