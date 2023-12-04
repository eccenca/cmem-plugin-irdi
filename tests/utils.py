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

SET_COUNTER = SparqlQuery(
    text="""
    PREFIX co: <http://purl.org/ontology/co/core#>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    WITH <{{graph}}>
    DELETE {
        ?counter co:count ?count_old .
    }
    INSERT {
        ?counter co:count {{count}} .
    }
    USING <{{graph}}>
    WHERE {
        ?counter a co:Counter ;
                co:object / dcterms:identifier "{{identifier}}" ;
                co:count ?count_old .
    }
    """,
    query_type="UPDATE",
)

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


def set_counter(graph: str, identifier: str, count: int) -> None:
    """Set (initialized) counter to specific value"""
    SET_COUNTER.get_results(
        placeholder={"graph": graph, "identifier": identifier, "count": str(count)}
    )
