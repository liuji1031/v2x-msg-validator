import importlib
import logging
from types import ModuleType
from pycrate_asn1rt.asnobj import ASN1Obj

logger = logging.getLogger(__name__)    

def get_codec(revision: str) -> ModuleType:
    try:
        codec = importlib.import_module(f"v2x_codecs.{revision}")
        logger.info("Loaded codec for %s", revision)
        return codec
    except ImportError:
        raise ImportError(
            f"Codec for '{revision}' is not available. "
            f"Make sure {revision} is compiled using v2x-compile."
        )

def get_validator_map(codec):
    """Initialize the validator map from the compiled codec module."""
    validator_map = {}
    for d in codec.MessageFrame.MessageTypes._val.root:
        # d is a dictionary that looks like each of the following:
        # {'Type': <Type ([BasicSafetyMessage] SEQUENCE)>, 'id': 20}
        # {'Type': <Type ([MapData] SEQUENCE)>, 'id': 18}
        # ...
        # The map after being filled will look like this:
        # {19: ("MapData", j2735_202409.MapData.MapData.set_val),
        # 20: ("BasicSafetyMessage", j2735_202409.BasicSafetyMessage.BasicSafetyMessage.set_val), ...}
        validator_map[d["id"]] = (
            d["Type"]._typeref.get()._name,
            d["Type"]._typeref.get().set_val,
        )
    return validator_map


def validate_msg(data: dict, validator_map: dict) -> list[str]:
    """Validate actual message."""
    errors = []
    if "messageId" not in data:
        errors.append("key 'messageId' missing from input data")
        return errors
    if "value" not in data:
        errors.append("key 'value' missing from input data")
        return errors

    msg_id = int(data["messageId"])
    if msg_id not in validator_map:
        errors.append(f"messageId {data['messageId']} is not valid")
        return errors

    msg_name, validator = validator_map[msg_id]
    if not isinstance(data["value"], dict) or len(data["value"]) != 1:
        errors.append("'value' does not map to a valid dictionary")
        return errors
    data_msg_name, data_msg_val = next(iter(data["value"].items()))
    if msg_name != data_msg_name:
        errors.append(
            f"msg name {data_msg_name} does not match id {data['messageId']}"
        )
        return errors

    # finally do the actual validation
    validator(data_msg_val)

    # retrieve any errors from the ASN1Obj
    return ASN1Obj._errors


class V2XMessageValidator:
    def __init__(self, revision: str = "j2735_202409"):
        self._codec = get_codec(revision)
        self._revision = revision
        self._validator_map = get_validator_map(self._codec)

    def validate(self, data: dict) -> list:
        return validate_msg(data, self._validator_map)
