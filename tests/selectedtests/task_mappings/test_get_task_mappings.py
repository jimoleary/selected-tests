from unittest.mock import MagicMock

import selectedtests.task_mappings.get_task_mappings as under_test


class TestGetCorrelatedTaskMappings:
    def test_mappings_found(self):
        collection_mock = MagicMock()
        task_mapping = {
            "project": "my_project",
            "source_file": "src/file1.js",
            "source_file_seen_count": 1,
            "tasks": [
                {"name": "test1.js", "variant": "my-variant", "flip_count": 1},
                {"name": "test2.js", "variant": "my-variant", "flip_count": 1},
            ],
        }
        collection_mock.aggregate.side_effect = [[task_mapping]]
        changed_files = ["src/file1.js"]
        project = "my-project"
        task_mappings = under_test.get_correlated_task_mappings(
            collection_mock, changed_files, project, 0
        )

        assert task_mappings == [task_mapping]
        collection_mock.aggregate.assert_called_once()

    def test_no_mappings_found(self):
        collection_mock = MagicMock()
        collection_mock.aggregate.return_value = []
        changed_files = ["src/file1.js", "src/file2.js"]
        project = "my-project"
        task_mappings = under_test.get_correlated_task_mappings(
            collection_mock, changed_files, project, 0
        )

        assert task_mappings == []
        collection_mock.aggregate.assert_called_once()
