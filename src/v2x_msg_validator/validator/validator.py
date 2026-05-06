from importlib import import_module
from .codec import get_codec


class V2XMessageValidator:
    def __init__(self, revision: str = "j2735_202409"):
        self._codec = get_codec(revision)
        self._revision = revision
        # import the local validator module
        self._validator_module = import_module(f".{revision}", package=__package__)
        self._validator_module.init(self._codec)

    def validate(self, data: dict) -> list:
        return self._validator_module.validate_msg(data)
