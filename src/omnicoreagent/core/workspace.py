"""
Workspace Path Resolver

Central module for all agent runtime data paths.
All data directories live under a single workspace root so the entire
workspace can be mounted on cloud storage (S3 FUSE, R2, GCS, NFS, etc.)
and everything works transparently as if it were local.

Directory Layout:
    workspace/
    ├── artifacts/     # offloaded tool responses
    ├── memories/      # memory tool local storage
    └── config/        # agent runtime config files

Environment Variables:
    OMNICOREAGENT_WORKSPACE_DIR   – override workspace root (default: ./workspace)
    OMNICOREAGENT_ARTIFACTS_DIR   – explicit override for artifacts path
    OMNICOREAGENT_MEMORY_DIR      – explicit override for memories path
"""

import os
from pathlib import Path


# ---------------------------------------------------------------------------
# Workspace root
# ---------------------------------------------------------------------------

_DEFAULT_WORKSPACE = "./workspace"
WORKSPACE_DIR = os.environ.get("OMNICOREAGENT_WORKSPACE_DIR", _DEFAULT_WORKSPACE)


def get_workspace_dir() -> str:
    """Return the workspace root directory path."""
    return WORKSPACE_DIR


# ---------------------------------------------------------------------------
# Sub-directory resolvers
# ---------------------------------------------------------------------------

def get_artifacts_dir() -> str:
    """
    Return the artifacts directory path.

    Precedence:
      1. OMNICOREAGENT_ARTIFACTS_DIR env var (explicit override)
      2. <workspace>/artifacts
    """
    explicit = os.environ.get("OMNICOREAGENT_ARTIFACTS_DIR")
    if explicit:
        return explicit
    return str(Path(WORKSPACE_DIR) / "artifacts")


def get_memories_dir() -> str:
    """
    Return the memories directory path.

    Precedence:
      1. OMNICOREAGENT_MEMORY_DIR env var (explicit override)
      2. <workspace>/memories
    """
    explicit = os.environ.get("OMNICOREAGENT_MEMORY_DIR")
    if explicit:
        return explicit
    return str(Path(WORKSPACE_DIR) / "memories")


def get_config_dir() -> str:
    """Return the config directory path (<workspace>/config)."""
    return str(Path(WORKSPACE_DIR) / "config")


def ensure_workspace():
    """Create the workspace directory structure if it doesn't exist."""
    for dir_path in [get_workspace_dir(), get_artifacts_dir(), get_memories_dir(), get_config_dir()]:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
