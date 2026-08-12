"""Testing utilities.

Remove this and other example files after bootstrapping your project.
"""

import os

import pytest
from cmem_client.client import Client
from cmem_client.models.query_catalog import Query, QueryType
from cmem_plugin_base.dataintegration.context import (
    ExecutionContext,
    PluginContext,
    ReportContext,
    TaskContext,
    UserContext,
)
from cmem_plugin_base.dataintegration.entity import Entities
from cmem_plugin_base.testing import TestSystemContext

from cmem_plugin_irdi.item_code import execute_query

SET_COUNTER = Query(
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
                dcterms:identifier "{{identifier}}" ;
                co:count ?count_old .
    }
    """,
    query_type=QueryType.UPDATE,
)

needs_cmem = pytest.mark.skipif(
    os.environ.get("CMEM_BASE_URI", "") == "", reason="Needs CMEM configuration"
)


def get_client() -> Client:
    """Get a cmem-client client configured from the environment"""
    return Client.from_env()


class TestUserContext(UserContext):
    """dummy user context that can be used in tests"""

    __test__ = False

    def __init__(self):
        # get access token from default service account
        access_token = get_client().auth.get_access_token()
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
        self.system = TestSystemContext()


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
        self.system = TestSystemContext()


def drop_graph(graph: str) -> None:
    """Drop graph

    :param graph: graph to drop
    """
    query = Query(text="""DROP SILENT GRAPH <{{graph}}>""", query_type=QueryType.UPDATE)
    execute_query(get_client(), query, {"graph": graph})


def get_values(entities: Entities) -> list[str]:
    """Return all values of all entities in a single list

    :param entities: entities
    """
    return [i for entity in entities.entities for j in entity.values for i in j]


def set_counter(graph: str, identifier: str, count: int) -> None:
    """Set (initialized) counter to specific value

    :param graph: graph in which the counter is stored
    :param identifier: identifier of the counter
    :count number that counter will be set to
    """
    execute_query(
        get_client(),
        SET_COUNTER,
        {"graph": graph, "identifier": identifier, "count": str(count)},
    )
