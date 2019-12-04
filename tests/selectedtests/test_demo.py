import git
import os
import pytest
import pytz
import pdb

from datetime import datetime, time, timedelta

import selectedtests.test_mappings.create_test_mappings as under_test


@pytest.fixture(scope="function")
def repo_with_files_added_two_days_ago(monkeypatch, tmpdir):
    two_days_ago = str(datetime.combine(datetime.now() - timedelta(days=2), time()))
    monkeypatch.setenv("GIT_AUTHOR_DATE", two_days_ago)
    monkeypatch.setenv("GIT_COMMITTER_DATE", two_days_ago)

    repo = git.Repo.init(tmpdir)
    repo.index.commit("initial commit -- no files changed")
    source_file = os.path.join(tmpdir, "new-source-file")
    test_file = os.path.join(tmpdir, "new-test-file")
    open(source_file, "wb").close()
    open(test_file, "wb").close()
    repo.index.add([source_file, test_file])
    repo.index.commit("add source and test file in same commit 2 days ago")

    return repo


def test_files_changed_within_range(repo_with_files_added_two_days_ago):
    three_days_ago = datetime.combine(datetime.now() - timedelta(days=3), time()).replace(
        tzinfo=pytz.UTC
    )
    test_mappings = under_test.TestMappings.create_mappings(
        repo=repo_with_files_added_two_days_ago, after_date=three_days_ago
    )
    test_mappings_list = test_mappings.get_mappings()

    assert test_mappings_list == [
        {
            "source_file": "new-source-file",
            "project": "my_project",
            "branch": "master",
            "source_file_seen_count": 1,
            "test_files": [{"name": "new-test-file", "test_file_seen_count": 1}],
        }
    ]


def test_files_changed_outside_range(repo_with_files_added_two_days_ago):
    one_day_ago = datetime.combine(datetime.now() - timedelta(days=1), time()).replace(
        tzinfo=pytz.UTC
    )
    test_mappings = under_test.TestMappings.create_mappings(
        repo=repo_with_files_added_two_days_ago, after_date=one_day_ago
    )
    test_mappings_list = test_mappings.get_mappings()
    assert len(test_mappings_list) == 0
