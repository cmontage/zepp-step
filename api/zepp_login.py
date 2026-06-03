from __future__ import annotations

import re
import uuid
from dataclasses import asdict, dataclass
from typing import Any
from urllib.parse import parse_qs, quote, urlparse

try:
    import requests
except ImportError:  # Keeps --help usable before installing dependencies.
    requests = None


REGISTRATION_URL = "https://api-user.huami.com/registrations/{account}/tokens"
CLIENT_LOGIN_URL = "https://api-mifit.zepp.com/v2/client/login"
APP_TOKEN_URL = "https://api-mifit.zepp.com/v1/client/app_tokens"

APP_NAME = "com.huami.midong"
DN = (
    "api-mifit.zepp.com,api-user.zepp.com,api-mifit.zepp.com,"
    "api-watch.zepp.com,app-analytics.zepp.com,auth.zepp.com,"
    "api-analytics.zepp.com"
)
DEFAULT_TIMEOUT = 30

__all__ = [
    "APP_NAME",
    "DN",
    "DEFAULT_TIMEOUT",
    "LoginResult",
    "ZeppLifeLoginError",
    "exchange_access_code",
    "get_app_token",
    "get_registration_access_code",
    "normalize_account",
    "result_to_dict",
    "zepp_login",
]


class ZeppLifeLoginError(RuntimeError):
    pass


@dataclass
class LoginResult:
    login_token: str
    app_token: str
    user_id: str


def mask_secret(value: str | None, keep: int = 6) -> str:
    if not value:
        return ""
    if len(value) <= keep * 2:
        return "*" * len(value)
    return f"{value[:keep]}...{value[-keep:]}"


def normalize_account(account: str) -> str:
    account = account.strip()
    is_phone = re.fullmatch(r"\+?\d+", account) is not None
    is_email = re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", account) is not None

    if not is_phone and not is_email:
        raise ZeppLifeLoginError("account must be a phone number or email address")

    if is_phone and not account.startswith("+"):
        return f"+86{account}"
    return account


def ensure_http_ok(response: Any, label: str) -> None:
    if response.status_code < 400:
        return

    retry_after = response.headers.get("retry-after") if response.headers else None
    detail = response.text[:800] if getattr(response, "text", None) else ""
    if response.status_code == 429:
        raise ZeppLifeLoginError(f"{label} rate limited, retry-after={retry_after or 'N/A'}")
    if response.status_code in (401, 403):
        raise ZeppLifeLoginError(f"{label} unauthorized: {detail}")
    raise ZeppLifeLoginError(f"{label} failed: HTTP {response.status_code} - {detail}")


def parse_response_json(response: Any, label: str) -> dict[str, Any]:
    try:
        data = response.json()
    except ValueError as exc:
        raise ZeppLifeLoginError(f"{label} returned non-json response: {response.text[:800]}") from exc

    if not isinstance(data, dict):
        raise ZeppLifeLoginError(f"{label} returned unexpected json type: {type(data).__name__}")
    return data


def extract_access_code(response: Any) -> str:
    if response.status_code == 200:
        data = parse_response_json(response, "registration login")
        code = data.get("access") or data.get("access_token") or data.get("code")
        if code:
            return str(code)
        raise ZeppLifeLoginError(f"registration login did not return access code: {data}")

    if response.status_code in (302, 303):
        location = response.headers.get("location", "")
        if not location:
            raise ZeppLifeLoginError("registration login redirect did not include Location")

        parsed = urlparse(location)
        query_code = parse_qs(parsed.query).get("access")
        if query_code and query_code[0]:
            return query_code[0]

        match = re.search(r"access=([^&]+)", location)
        if match:
            return match.group(1)

    raise ZeppLifeLoginError(f"registration login returned unexpected status: {response.status_code}")


def common_zepp_headers() -> dict[str, str]:
    return {
        "app_name": APP_NAME,
        "hm-privacy-ceip": "false",
        "x-request-id": str(uuid.uuid4()),
        "accept-language": "zh-CN",
        "appname": APP_NAME,
        "cv": "151689_9.12.5",
        "v": "2.0",
        "appplatform": "android_phone",
        "vb": "202509151347",
        "vn": "9.12.5",
        "user-agent": "Zepp/9.12.5 (2206122SC; Android 14; Density/2.625)",
        "accept-encoding": "gzip",
    }


def get_registration_access_code(session: Any, account: str, password: str, timeout: int) -> str:
    account = normalize_account(account)
    url = REGISTRATION_URL.format(account=quote(account, safe=""))

    data = {
        "client_id": "HuaMi",
        "country_code": "CN",
        "json_response": "true",
        "name": account,
        "password": password,
        "redirect_uri": "https://s3-us-west-2.amazonaws.com/hm-registration/successsignin.html",
        "state": "REDIRECTION",
        "token": "access",
    }
    headers = {
        "x-request-id": str(uuid.uuid4()),
        "app_name": "com.huami.webapp",
        "lang": "zh",
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0"
        ),
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://user.zepp.com",
        "referer": "https://user.zepp.com/",
        "dnt": "1",
        "accept-encoding": "gzip, deflate, br, zstd",
    }

    response = session.post(
        url,
        data=data,
        headers=headers,
        allow_redirects=False,
        timeout=timeout,
    )
    ensure_http_ok(response, "registration login")
    return extract_access_code(response)


def exchange_access_code(session: Any, access_code: str, timeout: int) -> tuple[str, str]:
    response = session.post(
        CLIENT_LOGIN_URL,
        data={
            "allow_registration": "false",
            "app_name": APP_NAME,
            "app_version": "9.12.5",
            "code": access_code,
            "country_code": "CN",
            "device_id": "2C8B4939-0CCD-4E94-8CBA-CB8EA6E613A1",
            "device_model": "android_phone",
            "dn": DN,
            "grant_type": "access_token",
            "lang": "zh",
            "source": "com.huami.watch.hmwatchmanager:9.12.5:151689",
            "third_name": "huami",
        },
        headers=common_zepp_headers(),
        timeout=timeout,
    )
    ensure_http_ok(response, "client login")
    result = parse_response_json(response, "client login")

    token_info = result.get("token_info") or {}
    login_token = token_info.get("login_token")
    user_id = token_info.get("user_id")
    if not login_token or not user_id:
        raise ZeppLifeLoginError(f"client login returned incomplete token_info: {token_info}")
    return str(login_token), str(user_id)


def get_app_token(session: Any, login_token: str, timeout: int) -> str:
    response = session.get(
        APP_TOKEN_URL,
        params={
            "app_name": APP_NAME,
            "dn": DN,
            "login_token": login_token,
        },
        headers={
            **common_zepp_headers(),
            "accept": "application/json, text/plain, */*",
        },
        timeout=timeout,
    )
    ensure_http_ok(response, "app token")
    result = parse_response_json(response, "app token")

    token_info = result.get("token_info") or {}
    app_token = token_info.get("app_token")
    if not app_token:
        raise ZeppLifeLoginError(f"app token response missing app_token: {token_info}")
    return str(app_token)


def zepp_login(account: str, password: str, timeout: int = DEFAULT_TIMEOUT) -> LoginResult:
    if requests is None:
        raise ZeppLifeLoginError("missing dependency: install requests with `python -m pip install requests`")

    session = requests.Session()
    access_code = get_registration_access_code(session, account, password, timeout)
    login_token, user_id = exchange_access_code(session, access_code, timeout)
    app_token = get_app_token(session, login_token, timeout)
    return LoginResult(login_token=login_token, app_token=app_token, user_id=user_id)


def result_to_dict(result: LoginResult, *, mask: bool = False) -> dict[str, str]:
    data = asdict(result)
    if mask:
        data["login_token"] = mask_secret(result.login_token)
        data["app_token"] = mask_secret(result.app_token)
    return data
