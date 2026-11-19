"""Public rank-eleven certificate database distributed in Zenodo record 23979316."""
import os
from pathlib import Path

DATABASE_SHA256 = "982eaf73232af64ccf3ad2123d5e1f3eef169976cb1a90b2f45eaae4389c59e8"

def database_path():
    return Path(os.environ["RANK9_CERTIFICATE_DB"]).resolve(strict=True)
