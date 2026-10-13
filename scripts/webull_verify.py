#!/usr/bin/env python3
"""Verify Webull OpenAPI credentials with a read-only account-list call."""

from __future__ import annotations

import json
import logging
import os
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".webull.env"


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise SystemExit(f"Missing {name}. Fill it in {ENV_PATH}.")
    return value


def endpoint_for(env_name: str) -> str:
    env_name = env_name.lower()
    if env_name == "sandbox":
        return "api.sandbox.webull.com"
    if env_name == "prod":
        return "api.webull.com"
    raise SystemExit("WEBULL_ENV must be sandbox or prod.")


def env_int(name: str, default: int) -> int:
    raw = os.environ.get(name, "").strip()
    if not raw:
        return default
    try:
        value = int(raw)
    except ValueError:
        raise SystemExit(f"{name} must be an integer.")
    if value <= 0:
        raise SystemExit(f"{name} must be positive.")
    return value


SENSITIVE_KEY_PARTS = ("account", "id", "token", "secret", "key", "authorization")


def redact_value(value: Any) -> Any:
    if isinstance(value, dict):
        redacted: dict[str, Any] = {}
        for key, item in value.items():
            key_text = str(key).lower()
            if any(part in key_text for part in SENSITIVE_KEY_PARTS):
                redacted[key] = redact_scalar(item)
            else:
                redacted[key] = redact_value(item)
        return redacted
    if isinstance(value, list):
        return [redact_value(item) for item in value]
    return value


def redact_scalar(value: Any) -> str:
    text = str(value or "")
    if not text:
        return ""
    if len(text) <= 8:
        return "***"
    return f"{text[:4]}...{text[-4:]}"


def main() -> int:
    load_env_file(ENV_PATH)
    logging.disable(logging.CRITICAL)

    try:
        from webull.core.client import ApiClient
        from webull.trade.trade_client import TradeClient
    except ModuleNotFoundError as exc:
        print(f"Missing Python package: {exc.name}", file=sys.stderr)
        print(
            "Install the official SDK after pip is available:\n"
            "  python3 -m pip install --user --upgrade -r requirements-webull.txt",
            file=sys.stderr,
        )
        return 2

    app_key = require_env("WEBULL_APP_KEY")
    app_secret = require_env("WEBULL_APP_SECRET")
    region = os.environ.get("WEBULL_REGION", "us").strip() or "us"
    env_name = os.environ.get("WEBULL_ENV", "sandbox").strip() or "sandbox"
    endpoint = endpoint_for(env_name)
    token_check_seconds = env_int("WEBULL_TOKEN_CHECK_SECONDS", 10)
    token_check_interval = env_int("WEBULL_TOKEN_CHECK_INTERVAL_SECONDS", 2)

    try:
        api_client = ApiClient(
            app_key,
            app_secret,
            region,
            connect_timeout=5,
            timeout=15,
            token_check_duration_seconds=token_check_seconds,
            token_check_interval_seconds=token_check_interval,
        )
        api_client._stream_logger_set = True
        api_client._file_logger_set = True
        api_client.add_endpoint(region, endpoint)
        trade_client = TradeClient(api_client)
        response = trade_client.account_v2.get_account_list()
    except Exception as exc:
        print(
            f"Webull read-only verification failed for {env_name} endpoint {endpoint}: "
            f"{exc.__class__.__name__}: {exc}",
            file=sys.stderr,
        )
        return 1

    status_code = getattr(response, "status_code", None)
    print(f"Webull account-list status: {status_code}")

    try:
        payload = response.json()
    except Exception:
        payload = getattr(response, "text", "")

    if isinstance(payload, str):
        print(payload[:2000])
    else:
        print(json.dumps(redact_value(payload), indent=2, ensure_ascii=False))

    return 0 if status_code == 200 else 1


if __name__ == "__main__":
    raise SystemExit(main())
