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

from immuni_app_configuration.apis import settings
from immuni_app_configuration.core.managers import managers
from immuni_common.sanic import create_app, run_app

sanic_app = create_app(
    api_title="App Configuration Service",
    api_description="The App can be partially customised through the Configuration Settings "
    "downloaded at the App startup and updated every time the App starts a session, whether in the "
    "foreground or background. "
    "For example, these include information such as the weights to be used by the Mobile Client in "
    "the calculation of the Total Risk Score.",
    blueprints=(settings.bp,),
    managers=managers,
)

if __name__ == "__main__":  # pragma: no cover
    run_app(sanic_app)
