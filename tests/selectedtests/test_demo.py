import git
import os
import pytest
import pytz
import pdb

from datetime import datetime, time, timedelta

import selectedtests.test_mappings.create_test_mappings as under_test


def test_files_changed_within_range():
    two_days_ago = str(datetime.combine(datetime.now() - timedelta(days=2), time()))
    os.environ["GIT_AUTHOR_DATE"] = two_days_ago
    os.environ["GIT_COMMITTER_DATE"] = two_days_ago

    current_directory = os.path.dirname(os.path.abspath(__file__))
    repo = git.Repo.init(current_directory)
    repo.index.commit("initial commit -- no files changed")
    source_file = os.path.join(current_directory, "new-source-file")
    test_file = os.path.join(current_directory, "new-test-file")
    open(source_file, "wb").close()
    open(test_file, "wb").close()
    repo.index.add([source_file, test_file])
    repo.index.commit("add source and test file in same commit 2 days ago")

    three_days_ago = datetime.combine(datetime.now() - timedelta(days=3), time()).replace(
        tzinfo=pytz.UTC
    )
    test_mappings = under_test.TestMappings.create_mappings(
        repo=repo, after_date=three_days_ago
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
