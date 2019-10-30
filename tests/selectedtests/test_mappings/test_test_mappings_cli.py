import json

from click.testing import CliRunner
from unittest.mock import patch, MagicMock
from selectedtests.test_mappings.cli import cli

NS = "selectedtests.test_mappings.cli"
MAPPINGS_NS = "selectedtests.test_mappings.mappings"


def ns(relative_name):
    """Return a full name from a name relative to the tested module"s name space."""
    return NS + "." + relative_name


def m_ns(relative_name):
    """Return a full name to mappings from a name relative to the tested module"s name space."""
    return MAPPINGS_NS + "." + relative_name


class TestCli:
    @patch(ns("RetryingEvergreenApi"))
    @patch(ns("generate_test_mappings"))
    def test_arguments_passed_in(self, generate_test_mappings_mock, evg_api):
        mock_evg_api = MagicMock()
        evg_api.get_api.return_value = mock_evg_api
        generate_test_mappings_mock.return_value = "mock-response"

        runner = CliRunner()
        with runner.isolated_filesystem():
            output_file = "output.txt"
            result = runner.invoke(
                cli,
                [
                    "create",
                    "mongodb-mongo-master",
                    "--module-name",
                    "my-module",
                    "--source-file-regex",
                    ".*",
                    "--test-file-regex",
                    ".*",
                    "--module-source-file-regex",
                    ".*",
                    "--module-test-file-regex",
                    ".*",
                    "--output-file",
                    output_file,
                    "--start",
                    "2019-10-11T19:10:38",
                    "--end",
                    "2019-10-11T19:30:38",
                ],
            )
            assert result.exit_code == 0
            with open(output_file, "r") as data:
                output = json.load(data)
                assert output == "mock-response"

    @patch(ns("RetryingEvergreenApi"))
    @patch(ns("generate_test_mappings"))
    def test_invalid_dates(self, generate_test_mappings_mock, evg_api):
        mock_evg_api = MagicMock()
        evg_api.get_api.return_value = mock_evg_api
        generate_test_mappings_mock.return_value = "mock-response"

        runner = CliRunner()
        with runner.isolated_filesystem():
            output_file = "output.txt"
            result = runner.invoke(
                cli,
                [
                    "create",
                    "mongodb-mongo-master",
                    "--module-name",
                    "my-module",
                    "--source-file-regex",
                    ".*",
                    "--test-file-regex",
                    ".*",
                    "--module-source-file-regex",
                    ".*",
                    "--module-test-file-regex",
                    ".*",
                    "--output-file",
                    output_file,
                    "--start",
                    "2019",
                    "--end",
                    "2019",
                ],
            )
            assert result.exit_code == 1
            assert (
                "The start or end date could not be parsed - make sure it's an iso date"
                in result.stdout
            )

    @patch(ns("RetryingEvergreenApi"))
    @patch(ns("generate_test_mappings"))
    def test_module_regexes_not_passed_in(self, generate_test_mappings_mock, evg_api):
        mock_evg_api = MagicMock()
        evg_api.get_api.return_value = mock_evg_api
        generate_test_mappings_mock.return_value = "mock-response"

        runner = CliRunner()
        with runner.isolated_filesystem():
            output_file = "output.txt"
            result = runner.invoke(
                cli,
                [
                    "create",
                    "mongodb-mongo-master",
                    "--module-name",
                    "my-module",
                    "--source-file-regex",
                    ".*",
                    "--test-file-regex",
                    ".*",
                    "--output-file",
                    output_file,
                    "--start",
                    "2019-10-11T19:10:38",
                    "--end",
                    "2019-10-11T19:30:38",
                ],
            )
            assert result.exit_code == 1
            assert (
                "A module source file regex is required when a module is being analyzed"
                in result.stdout
            )