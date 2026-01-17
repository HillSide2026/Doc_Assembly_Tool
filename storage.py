from pathlib import Path
import re

ENGAGEMENTS_ROOT = Path("engagements")


def sanitize_slug(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value)
    return value.strip("-")


def format_engagement_id(year: int, seq: int, slug: str) -> str:
    safe_slug = sanitize_slug(slug)
    return f"{year}-{seq:03d}-{safe_slug}"


def engagement_dir(engagement_id: str) -> Path:
    return ENGAGEMENTS_ROOT / engagement_id


def engagement_artifacts(engagement_id: str, version: int = 1) -> dict:
    base = engagement_dir(engagement_id)
    return {
        "dir": base,
        "intake": base / "intake.json",
        "docx": base / f"engagement_v{version}.docx",
        "pdf": base / f"engagement_v{version}.pdf",
        "manifest": base / "manifest.json",
    }
