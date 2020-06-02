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

from datetime import timedelta
from http import HTTPStatus

from marshmallow import fields
from marshmallow.validate import Range
from sanic import Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse
from sanic_openapi import doc

from immuni_app_configuration.core import config
from immuni_app_configuration.models.setting import Setting
from immuni_app_configuration.models.swagger import SettingsResponse
from immuni_common.core.exceptions import SchemaValidationException
from immuni_common.helpers.cache import cache
from immuni_common.helpers.sanic import json_response, validate
from immuni_common.helpers.swagger import doc_exception
from immuni_common.models.enums import Location, Platform
from immuni_common.models.marshmallow.fields import EnumField

bp: Blueprint = Blueprint("settings", url_prefix="/settings")


@bp.route("", version=1, methods=["GET"])
@doc.summary("Fetch Configuration Settings (caller: Mobile Client).")
@doc.description(
    "The Mobile Client fetches the Configuration Settings. Different Configuration Settings may be "
    "made available for different platforms (i.e., iOS and Android) and App build numbers."
)
@doc.consumes(
    doc.Integer(name="build", description="The App's build number."),
    location="query",
    required=True,
)
@doc.consumes(
    doc.String(
        name="platform",
        choices=[p.value for p in Platform],
        description="The Mobile Client's platform.",
    ),
    location="query",
    required=True,
)
@doc.response(HTTPStatus.OK.value, SettingsResponse, description="A JSON-formatted dictionary.")
@doc_exception(SchemaValidationException)
@cache(max_age=timedelta(hours=1))
@validate(
    location=Location.QUERY,
    build=fields.Integer(required=True, validate=Range(min=1, max=config.MAX_ALLOWED_BUILD)),
    platform=EnumField(enum=Platform),
)
async def get_settings(request: Request, build: int, platform: Platform) -> HTTPResponse:
    """
    Provide the app settings given the build number and platform.

    :return: 200 and JSON-formatted dictionary, 400 on SchemaValidationException.
    """
    settings = Setting.with_build_and_platform(build=build, platform=platform)
    return json_response(settings)
