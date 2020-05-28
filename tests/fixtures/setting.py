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

from pytest import fixture

from immuni_app_configuration.models.setting import Platform, Setting


@fixture()
def ios_int_setting_v1() -> Setting:
    return Setting(name="ios_int_setting", platform=Platform.IOS, starting_build=1, value=1,).save()


@fixture()
def ios_int_setting_v2() -> Setting:
    return Setting(name="ios_int_setting", platform=Platform.IOS, starting_build=2, value=2,).save()


@fixture()
def android_int_setting() -> Setting:
    return Setting(
        name="android_int_setting", platform=Platform.ANDROID, starting_build=2, value=100,
    ).save()


@fixture()
def ios_string_setting() -> Setting:
    return Setting(
        name="ios_string_setting", platform=Platform.IOS, starting_build=1, value="string_value",
    ).save()
