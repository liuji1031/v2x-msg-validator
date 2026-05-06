from pycrate_asn1rt.asnobj import ASN1Obj

# build the map between message id and the corresponding set_val function
VALIDATOR_MAP = {}


def init(codec):
    """Initialize the validator map from the compiled codec module."""
    if VALIDATOR_MAP:
        return
    for d in codec.MessageFrame.MessageTypes._val.root:
        # d is a dictionary that looks like each of the following:
        # {'Type': <Type ([BasicSafetyMessage] SEQUENCE)>, 'id': 20}
        # {'Type': <Type ([MapData] SEQUENCE)>, 'id': 18}
        # ...
        # The VALIDATOR_MAP after being filled will look like this:
        # {19: ("MapData", j2735_202409.MapData.MapData.set_val),
        # 20: ("BasicSafetyMessage", j2735_202409.BasicSafetyMessage.BasicSafetyMessage.set_val), ...}
        VALIDATOR_MAP[d["id"]] = (
            d["Type"]._typeref.get()._name,
            d["Type"]._typeref.get().set_val,
        )


def validate_msg(data: dict) -> list[str]:
    """Validate actual message."""
    errors = []
    if "messageId" not in data:
        errors.append("key 'messageId' missing from input data")
        return errors
    if "value" not in data:
        errors.append("key 'value' missing from input data")
        return errors

    msg_id = int(data["messageId"])
    if msg_id not in VALIDATOR_MAP:
        errors.append(f"messageId {data['messageId']} is not valid")
        return errors

    msg_name, validator = VALIDATOR_MAP[msg_id]
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
