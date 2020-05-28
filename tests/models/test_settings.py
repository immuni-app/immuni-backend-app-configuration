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

from mongoengine.connection import get_db
from mongoengine.errors import NotUniqueError
from pytest import raises

from immuni_app_configuration.models.setting import Setting
from immuni_common.models.enums import Platform


def test_index(
    ios_int_setting_v1: Setting,
    ios_int_setting_v2: Setting,
    ios_string_setting: Setting,
    android_int_setting: Setting,
) -> None:
    explain = get_db().command(
        "aggregate",
        "setting",
        pipeline=Setting.get_build_and_platform_pipeline(platform=Platform.IOS, build=1),
        explain=True,
    )

    assert (
        explain["stages"][0]["$cursor"]["queryPlanner"]["winningPlan"]["inputStage"]["stage"]
        == "IXSCAN"
    )
    # sort should not be executed
    assert len(explain["stages"]) == 2


def test_index_uniqueness() -> None:
    Setting(name="unique", platform=Platform.IOS, starting_build=1, value="no_matter_what").save()
    Setting(name="unique", platform=Platform.IOS, starting_build=2, value="no_matter_what").save()
    Setting(
        name="unique", platform=Platform.ANDROID, starting_build=1, value="no_matter_what"
    ).save()
    with raises(NotUniqueError):
        Setting(
            name="unique", platform=Platform.IOS, starting_build=1, value="no_matter_what"
        ).save()
