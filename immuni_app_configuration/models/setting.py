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

from typing import Dict, List

from bson import ObjectId
from mongoengine import Document, IntField, ObjectIdField, StringField
from mongoengine.base import BaseField

from immuni_common.models.enums import Platform
from immuni_common.models.mongoengine.enum_field import EnumField


class Setting(Document):
    """
    The setting document structure.
    """

    _id: ObjectId = ObjectIdField()
    name = StringField(required=True)
    platform = EnumField(Platform)
    starting_build = IntField(required=True)
    value = BaseField(required=True)

    meta = {"indexes": [{"fields": ["platform", "-starting_build", "name"], "unique": True}]}

    @classmethod
    def with_build_and_platform(cls, *, build: int, platform: Platform) -> Dict:
        """
        Return the settings matching the given build and platform.
        If there are more settings with the same name, the one with the higher starting build
        version is returned.

        :param build: the app build number.
        :param platform: the app platform.
        :return: a dictionary containing the settings name and value.
        """

        settings = cls.objects.aggregate(
            *cls.get_build_and_platform_pipeline(platform=platform, build=build)
        )
        return {s["name"]: s["value"] for s in settings}

    @staticmethod
    def get_build_and_platform_pipeline(*, build: int, platform: Platform,) -> List[Dict]:
        """
        Return the aggregation pipeline for retrieving the settings with platform and build.

        :param build: the app build number.
        :param platform: the app platform.
        :return: the list of aggregation stages to perform the query.
        """
        return [
            {"$match": {"platform": platform.name, "starting_build": {"$lte": build}}},
            {"$sort": {"starting_build": -1}},
            {
                "$group": {
                    "_id": "$name",
                    "name": {"$first": "$name"},
                    "value": {"$first": "$value"},
                }
            },
        ]
