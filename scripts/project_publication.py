"""Explicit source and publication gate for public project presentations."""

from urllib.parse import urlparse

MAX_VISIBLE_PROJECTS = 9
PUBLIC_STATUSES = {"concept", "reference"}


def is_public(project: dict) -> bool:
    source = project.get("publicationSource", {})
    return (
        project.get("publicationStatus") in PUBLIC_STATUSES
        and urlparse(source.get("url", "")).scheme == "https"
        and bool(source.get("checkedOn"))
        and bool(source.get("scope"))
    )


def visible_projects(projects: list[dict]) -> list[dict]:
    eligible = [project for project in projects if is_public(project)]
    return sorted(eligible, key=lambda project: not project.get("featured", False))[:MAX_VISIBLE_PROJECTS]
