from unipath import Path
import os

PROJECTROOT = Path(__file__).parent.parent
DATADIR = os.environ.get("PCGEN_DATADIR", None)

try:
    from .settings_local import *
except ImportError:
    pass

if not DATADIR:
    raise ImproperlyConfigured("No DATADIR defined and PCGEN_DATADIR not set in environment")

DATADIR = Path(DATADIR)
