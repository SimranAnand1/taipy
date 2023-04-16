# Copyright 2023 Avaiga Private Limited
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

from datetime import datetime

import pytest

from src.taipy.core.cycle._cycle_manager_factory import _CycleManagerFactory
from src.taipy.core.cycle.cycle import Cycle
from taipy.config.common.frequency import Frequency
from taipy.config.config import Config


def test_save_and_load(tmpdir, cycle):
    repository = _CycleManagerFactory._build_repository()
    repository.base_path = tmpdir
    repository._save(cycle)
    cc = repository._load(cycle.id)

    assert isinstance(cc, Cycle)
    assert cc.id == cycle.id
    assert cc.name == cycle.name
    assert cc.creation_date == cycle.creation_date


@pytest.mark.skip("Deprecated: Old repository version")
def test_from_and_to_model(cycle, cycle_model):
    repository = _CycleManagerFactory._build_repository().repo
    assert repository._to_model(cycle) == cycle_model
    assert repository._from_model(cycle_model) == cycle


@pytest.mark.skip("Deprecated: Old repository version")
def test_get_primary(tmpdir, cycle, current_datetime):
    cycle_repository = _CycleManagerFactory._build_repository()
    cycle_repository.base_path = tmpdir

    assert len(cycle_repository._load_all()) == 0

    cycle_repository._save(cycle)
    cycle_1 = cycle_repository.load(cycle.id)
    cycle_2 = Cycle(Frequency.MONTHLY, {}, current_datetime, current_datetime, current_datetime, name="foo")
    cycle_repository._save(cycle_2)
    cycle_2 = cycle_repository.load(cycle_2.id)

    assert len(cycle_repository._load_all()) == 2
    assert len(cycle_repository.get_cycles_by_frequency_and_start_date(cycle_1.frequency, cycle_1.start_date)) == 1
    assert len(cycle_repository.get_cycles_by_frequency_and_start_date(cycle_2.frequency, cycle_2.start_date)) == 1
    assert (
        len(cycle_repository.get_cycles_by_frequency_and_start_date(Frequency.WEEKLY, datetime(2000, 1, 1, 1, 0, 0, 0)))
        == 0
    )

    assert (
        len(cycle_repository.get_cycles_by_frequency_and_overlapping_date(cycle_1.frequency, cycle_1.creation_date))
        == 1
    )
    assert (
        cycle_repository.get_cycles_by_frequency_and_overlapping_date(cycle_1.frequency, cycle_1.creation_date)[0]
        == cycle_1
    )
    assert (
        len(
            cycle_repository.get_cycles_by_frequency_and_overlapping_date(
                Frequency.WEEKLY, datetime(2000, 1, 1, 1, 0, 0, 0)
            )
        )
        == 0
    )


@pytest.mark.skip("Deprecated: Old repository version")
def test_save_and_load_for_sql_repo(tmpdir, cycle):
    Config.configure_global_app(repository_type="sql")

    repository = _CycleManagerFactory._build_repository()
    repository.base_path = tmpdir
    repository._save(cycle)
    cc = repository.load(cycle.id)

    assert isinstance(cc, Cycle)
    assert cc.id == cycle.id
    assert cc.name == cycle.name
    assert cc.creation_date == cycle.creation_date


@pytest.mark.skip("Deprecated: Old repository version")
def test_from_and_to_model_for_sql_repo(cycle, cycle_model):
    Config.configure_global_app(repository_type="sql")

    repository = _CycleManagerFactory._build_repository().repo._table
    assert repository._to_model(cycle) == cycle_model
    assert repository._from_model(cycle_model) == cycle


def test_get_primary_for_sql_repo(tmpdir, cycle, current_datetime):
    Config.configure_global_app(repository_type="sql")

    cycle_repository = _CycleManagerFactory._build_repository()

    cycle_repository._delete_all()
    assert len(cycle_repository._load_all()) == 0

    cycle_repository._save(cycle)
    cycle_1 = cycle_repository.load(cycle.id)
    cycle_2 = Cycle(Frequency.MONTHLY, {}, current_datetime, current_datetime, current_datetime, name="foo")
    cycle_repository._save(cycle_2)
    cycle_2 = cycle_repository.load(cycle_2.id)

    assert len(cycle_repository._load_all()) == 2
    assert len(cycle_repository.get_cycles_by_frequency_and_start_date(cycle_1.frequency, cycle_1.start_date)) == 1
    assert len(cycle_repository.get_cycles_by_frequency_and_start_date(cycle_2.frequency, cycle_2.start_date)) == 1
    assert (
        len(cycle_repository.get_cycles_by_frequency_and_start_date(Frequency.WEEKLY, datetime(2000, 1, 1, 1, 0, 0, 0)))
        == 0
    )

    assert (
        len(cycle_repository.get_cycles_by_frequency_and_overlapping_date(cycle_1.frequency, cycle_1.creation_date))
        == 1
    )
    assert (
        cycle_repository.get_cycles_by_frequency_and_overlapping_date(cycle_1.frequency, cycle_1.creation_date)[0]
        == cycle_1
    )
    assert (
        len(
            cycle_repository.get_cycles_by_frequency_and_overlapping_date(
                Frequency.WEEKLY, datetime(2000, 1, 1, 1, 0, 0, 0)
            )
        )
        == 0
    )
