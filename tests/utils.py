"""Testing utilities."""
import os
from typing import ClassVar

import pytest

# check for cmem environment and skip if not present
from cmem.cmempy.api import get_token
from cmem.cmempy.config import get_oauth_default_credentials
from cmem.cmempy.queries import SparqlQuery
from cmem_plugin_base.dataintegration.context import (
    ExecutionContext,
    PluginContext,
    ReportContext,
    TaskContext,
    UserContext,
)
from cmem_plugin_base.dataintegration.entity import Entities

needs_cmem = pytest.mark.skipif(
    os.environ.get("CMEM_BASE_URI", "") == "", reason="Needs CMEM configuration"
)


class TestUserContext(UserContext):
    """dummy user context that can be used in tests"""

    __test__ = False
    default_credential: ClassVar[dict] = {}

    def __init__(self):
        # get access token from default service account
        if not TestUserContext.default_credential:
            TestUserContext.default_credential = get_oauth_default_credentials()
        access_token = get_token(_oauth_credentials=TestUserContext.default_credential)[
            "access_token"
        ]
        self.token = lambda: access_token


class TestPluginContext(PluginContext):
    """dummy plugin context that can be used in tests"""

    __test__ = False

    def __init__(
        self,
        project_id: str = "dummyProject",
    ):
        self.project_id = project_id
        self.user = TestUserContext()


class TestTaskContext(TaskContext):
    """dummy Task context that can be used in tests"""

    __test__ = False

    def __init__(self, project_id: str = "dummyProject", task_id: str = "dummyTask"):
        self.project_id = lambda: project_id
        self.task_id = lambda: task_id


class TestExecutionContext(ExecutionContext):
    """dummy execution context that can be used in tests"""

    __test__ = False

    def __init__(self, project_id: str = "dummyProject", task_id: str = "dummyTask"):
        self.report = ReportContext()
        self.task = TestTaskContext(project_id=project_id, task_id=task_id)
        self.user = TestUserContext()


def drop_graph(graph: str) -> None:
    """Drop graph"""
    query = SparqlQuery(text="""DROP SILENT GRAPH <{{graph}}>""", query_type="UPDATE")
    query.get_results(placeholder={"graph": graph})


def get_values(entities: Entities) -> list[str]:
    """Return all values of all entities"""
    return [i for entity in entities.entities for j in entity.values for i in j]
