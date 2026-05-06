import importlib
import logging
from types import ModuleType

logger = logging.getLogger(__name__)

# revision to compiled codec module mapping
_codec_registry: dict[str, ModuleType] = {}
_SUPPORTED_REVISIONS = ["j2735_202409"]

for _rev in _SUPPORTED_REVISIONS:
    try:
        _codec_registry[_rev] = importlib.import_module(f"v2x_codecs.{_rev}")
        logger.info("Loaded codec for %s", _rev)
    except ImportError:
        logger.warning(
            "Codec for %s not available; compile it before use.", _rev
        )


def get_codec(revision: str) -> ModuleType:
    if revision not in _codec_registry:
        raise ImportError(
            f"Codec for '{revision}' is not available. "
            f"Make sure v2x_codecs.{revision} is compiled and installed."
        )
    return _codec_registry[revision]
