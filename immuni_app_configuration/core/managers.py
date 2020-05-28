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

from typing import Optional

from mongoengine import connect
from pymongo import MongoClient

from immuni_app_configuration.core import config
from immuni_common.core.exceptions import ImmuniException
from immuni_common.core.managers import BaseManagers


class Managers(BaseManagers):
    """
    Collection of managers, lazily initialised.
    """

    _app_configuration_mongo: Optional[MongoClient] = None

    @property
    def app_configuration_mongo(self) -> MongoClient:
        """
        Return the MongoDB manager to handle app configurations.

        :return: the MongoDB manager to handle app configurations.
        :raise: ImmuniException if the manager is not initialized.
        """
        if self._app_configuration_mongo is None:
            raise ImmuniException("Cannot use the MongoDB manager before initializing it.")
        return self._app_configuration_mongo

    async def initialize(self) -> None:
        """
        Initialize managers on demand.
        """
        await super().initialize()
        self._app_configuration_mongo = connect(host=f"{config.APP_CONFIGURATION_MONGO_URL}")

    async def teardown(self) -> None:
        """
        Perform cleanup actions (e.g., close open connections).
        """
        await super().teardown()
        if self._app_configuration_mongo is not None:
            self._app_configuration_mongo.close()


managers = Managers()
