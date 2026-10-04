from __future__ import annotations


DEFAULT_TENANT_ROLES: dict[str, dict[str, list[str]]] = {
    "Admin": {
        "*": ["*"],
    },

    "Manager": {
        "datasets": [
            "read",
            "create",
            "update",
            "delete",
        ],
        "documents": [
            "read",
            "create",
            "update",
            "delete",
        ],
        "search": [
            "execute",
        ],
        "exports": [
            "create",
        ],
        "members": [
            "read",
            "manage",
        ],
        "roles": [
            "read",
        ],
    },

    "Analyst": {
        "datasets": [
            "read",
        ],
        "documents": [
            "read",
        ],
        "search": [
            "execute",
        ],
        "exports": [
            "create",
        ],
    },

    "Viewer": {
        "datasets": [
            "read",
        ],
        "documents": [
            "read",
        ],
    },
}