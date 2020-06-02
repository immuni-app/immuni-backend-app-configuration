#    Copyright (C) 2020 Presidenza del Consiglio dei Ministri.
#    Please refer to the AUTHORS file for more information.
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <https://www.gnu.org/licenses/>.

from http import HTTPStatus
from typing import Any, Dict

from pytest import mark
from pytest_sanic.utils import TestClient

from immuni_app_configuration.core import config
from immuni_app_configuration.models.setting import Setting
from immuni_common.core.exceptions import SchemaValidationException
from immuni_common.models.enums import Platform


@mark.parametrize(
    "platform, build, expected_result",
    [
        ("ios", "1", {"ios_int_setting": 1, "ios_string_setting": "string_value"},),
        ("ios", "2", {"ios_int_setting": 2, "ios_string_setting": "string_value"},),
        ("ios", "3", {"ios_int_setting": 2, "ios_string_setting": "string_value"},),
        ("android", "1", {},),
        ("android", config.MAX_ALLOWED_BUILD, {"android_int_setting": 100},),
    ],
)
async def test_get_settings(
    client: TestClient,
    ios_int_setting_v1: Setting,
    ios_int_setting_v2: Setting,
    ios_string_setting: Setting,
    android_int_setting: Setting,
    platform: str,
    build: str,
    expected_result: Dict,
) -> None:
    response = await client.get(f"/v1/settings?platform={platform}&build={build}",)
    assert response.status == 200
    assert "Cache-Control" in response.headers
    assert response.headers["Cache-Control"] == "public, max-age=3600"

    body = await response.json()
    assert body == expected_result


@mark.parametrize(
    "method", tuple(method for method in ("DELETE", "POST", "HEAD", "OPTIONS", "PATCH", "PUT")),
)
async def test_otp_method_not_allowed(method: str, client: TestClient) -> None:
    response = await client._request(
        method=method, uri=f"/v1/settings?platform={Platform.IOS.value}&build=1",
    )
    assert response.status == HTTPStatus.METHOD_NOT_ALLOWED.value


@mark.parametrize(
    "build",
    (
        0,
        -1,
        None,
        [],
        {},
        -100,
        "string",
        1.2,
        -1.0,
        "int('1')",
        23456789876543234567898765,  # > sys.maxsize
        config.MAX_ALLOWED_BUILD + 1,
        True,
        False,
        "true",
    ),
)
async def test_settings_raise_for_wrong_build(client: TestClient, build: Any) -> None:
    response = await client.get(f"/v1/settings?platform={Platform.IOS.value}&build={build}",)
    assert response.status == HTTPStatus.BAD_REQUEST.value
    assert await response.json() == {
        "error_code": SchemaValidationException.error_code,
        "message": SchemaValidationException.error_message,
    }


@mark.parametrize(
    "build",
    ["windows_phone", "blackberry", -1, None, [], {}, -100, "string", 1.2, -1.0, "int('1')"],
)
async def test_settings_raise_for_wrong_platform(client: TestClient, build: Any) -> None:
    build_number = 0
    response = await client.get(f"/v1/settings?platform={Platform.IOS.value}&build={build_number}",)
    assert response.status == HTTPStatus.BAD_REQUEST.value
    assert await response.json() == {
        "error_code": SchemaValidationException.error_code,
        "message": SchemaValidationException.error_message,
    }


@mark.parametrize("query", ["platform=ios", "build=1", "platform=ios&build=1&another=parameter"])
async def test_settings_raise_if_wrong_parameters(client: TestClient, query: str) -> None:
    response = await client.get(f"/v1/settings?{query}",)
    assert response.status == HTTPStatus.BAD_REQUEST.value
    assert await response.json() == {
        "error_code": SchemaValidationException.error_code,
        "message": SchemaValidationException.error_message,
    }


async def test_settings_raise_if_multiple_values(client: TestClient) -> None:
    query = "platform=ios&build=1&build=2"
    response = await client.get(f"/v1/settings?{query}",)
    assert response.status == HTTPStatus.BAD_REQUEST.value
    assert await response.json() == {
        "error_code": SchemaValidationException.error_code,
        "message": SchemaValidationException.error_message,
    }
