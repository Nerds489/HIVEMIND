"""
Lightweight memory store for HIVEMIND sessions.

This keeps session context on disk without requiring external services.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class MemoryStore:
    """Persist minimal session memory in the repo memory directory."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.sessions_dir = self.root / "sessions" / "active"
        self.completed_dir = self.root / "sessions" / "completed"
        self.working_dir = self.root / "working"
        self.session_id: Optional[str] = None
        self.session_path: Optional[Path] = None
        self._ensure_dirs()

    def _ensure_dirs(self) -> None:
        for path in (self.sessions_dir, self.completed_dir, self.working_dir):
            path.mkdir(parents=True, exist_ok=True)

    def _now(self) -> str:
        return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    def start_session(self) -> str:
        if self.session_id and self.session_path:
            return self.session_id

        timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        self.session_id = f"SESSION-{timestamp}"
        self.session_path = self.sessions_dir / f"{self.session_id}.json"
        if not self.session_path.exists():
            self._write(
                self.session_path,
                {
                    "session_id": self.session_id,
                    "started_at": self._now(),
                    "updated_at": self._now(),
                    "entries": [],
                },
            )
        return self.session_id

    def _read(self, path: Path) -> Dict[str, Any]:
        try:
            with path.open("r", encoding="utf-8") as handle:
                return json.load(handle)
        except (OSError, json.JSONDecodeError):
            return {}

    def _write(self, path: Path, payload: Dict[str, Any]) -> None:
        tmp_path = path.with_suffix(".tmp")
        with tmp_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
        tmp_path.replace(path)

    def record_task(
        self,
        task: str,
        agents: List[str],
        gates: Dict[str, str],
        report: str,
        status_lines: List[str],
    ) -> None:
        session_id = self.start_session()
        if not self.session_path:
            return

        payload = self._read(self.session_path)
        entries = payload.get("entries", [])
        entry = {
            "timestamp": self._now(),
            "task": task,
            "agents": agents,
            "gates": gates,
            "status_lines": status_lines,
            "report": report,
        }
        entries.append(entry)
        payload["entries"] = entries
        payload["updated_at"] = self._now()
        payload["session_id"] = session_id
        self._write(self.session_path, payload)

        current_task = {
            "session_id": session_id,
            "updated_at": self._now(),
            "task": task,
            "agents": agents,
            "gates": gates,
        }
        self._write(self.working_dir / "current-task.json", current_task)

    def recall(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        if not self.session_path or not self.session_path.exists():
            return []

        payload = self._read(self.session_path)
        entries = payload.get("entries", [])
        if not query:
            return entries[-limit:]

        query_lower = query.lower()
        matches = []
        for entry in reversed(entries):
            haystack = " ".join(
                [
                    entry.get("task", ""),
                    " ".join(entry.get("agents", [])),
                    " ".join(entry.get("status_lines", [])),
                    entry.get("report", ""),
                ]
            ).lower()
            if query_lower in haystack:
                matches.append(entry)
            if len(matches) >= limit:
                break

        return matches
