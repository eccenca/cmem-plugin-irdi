"""IRDI Plugin tests"""

import random
import re
import string
from collections.abc import Callable, Generator, Iterator

import pytest
from cmem_plugin_base.dataintegration.entity import Entities, Entity, EntityPath, EntitySchema

from cmem_plugin_irdi.utils import base_36_encode
from cmem_plugin_irdi.workflow.irdi_plugin import IrdiPlugin
from tests.utils import TestExecutionContext, drop_graph, get_values, needs_cmem, set_counter

IRDI_FORMAT = r"^\d{4}-\d{4}-[a-zA-Z0-9]{0,35}-\d-(\d{4})?#[A-Z0-9]{2}-[A-Z0-9]{6}#001"
COUNTERS_GRAPH_FORMAT = "urn:tmp:{}"

IRDI_PARAMS_VALID = {
    "icd": "1234",
    "oi": "5678",
    "opi": "abcdefg",
    "opis": "5",
    "ai": "9123",
    "csi": "A4",
    "counted_object": "urn:object",
    "input_schema_path": "",
    "output_schema_path": "http://purl.org/dc/terms/identifier",
}

IRDI_PARAMS_INVALID = {"icd": "12345", "opis": "a"}
COUNTED_OBJECT_INVALID_URI = "object"
PATH_TO_URI = "pathToURI"

IRDI_PARAMS_PATH = {"input_schema_path": PATH_TO_URI}

# ZZZZZZ
COUNT_MAX = 2176782335

ENTITY_URI_FORMAT = "urn:entity_{}"

NUMBER_OF_ENTITIES = 10

INPUTS = [
    Entities(
        entities=[
            Entity(uri=ENTITY_URI_FORMAT.format(i), values=[[]]) for i in range(NUMBER_OF_ENTITIES)
        ],
        schema=EntitySchema(type_uri="", paths=[]),
    )
]

INPUTS_PATH = [
    Entities(
        entities=[
            Entity(uri="", values=[[ENTITY_URI_FORMAT.format(i)]])
            for i in range(NUMBER_OF_ENTITIES)
        ],
        schema=EntitySchema(type_uri="", paths=[EntityPath(path=PATH_TO_URI)]),
    )
]


@pytest.fixture(scope="module")
def counter_graph() -> Generator:
    """Return function which creates a random graph name"""
    created_graphs = []

    def _create_counter_graph() -> str:
        graph = COUNTERS_GRAPH_FORMAT.format(
            "".join(random.choice(string.ascii_letters) for i in range(10))  # noqa: S311
        )
        created_graphs.append(graph)
        return graph

    yield _create_counter_graph
    for created_graph in created_graphs:
        drop_graph(created_graph)


@pytest.fixture(
    params=[(IRDI_PARAMS_VALID, INPUTS), (IRDI_PARAMS_VALID | IRDI_PARAMS_PATH, INPUTS_PATH)],
    scope="module",
)
def plugin_setup(request, counter_graph: Callable) -> tuple[IrdiPlugin, list[Entities]]:  # noqa: ANN001
    """Create Plugin"""
    kwargs, inputs = request.param

    return IrdiPlugin(graph=counter_graph(), **kwargs), inputs


@pytest.fixture(scope="module")
def plugin_results(plugin_setup: tuple[IrdiPlugin, list[Entities]]) -> Iterator[Entities]:
    """Execute plugin and return created IRDIs"""
    plugin, inputs = plugin_setup
    result = plugin.execute(inputs=inputs, context=TestExecutionContext())
    if not result:
        pytest.fail("Failed to execute Plugin")
    else:
        yield result


def test_encode() -> None:
    """Test base36 encoding"""
    assert base_36_encode(0) == "0"
    assert base_36_encode(100) == "2S"


@needs_cmem
def test_irdis_created(plugin_results: Entities) -> None:
    """Assert an IRDI was created for every input"""
    for input_entity_uri in [ENTITY_URI_FORMAT.format(i) for i in range(NUMBER_OF_ENTITIES)]:
        for result_entity in plugin_results.entities:
            if result_entity.uri == input_entity_uri:
                match = result_entity
        assert match is not None, f"No output for entity {input_entity_uri}"
        assert len(match.values[0]) > 0, f"No IRDI for entity {input_entity_uri} created"


@needs_cmem
def test_irdis_unique(plugin_results: Entities) -> None:
    """Assert no duplicate IRDIs are created"""
    irdis = get_values(plugin_results)
    assert len(irdis) == len(set(irdis))


@needs_cmem
def test_irdis_correct_format(plugin_results: Entities) -> None:
    """Assert all created IRDIS have the correct format"""
    irdis = get_values(plugin_results)
    for irdi in irdis:
        assert re.match(IRDI_FORMAT, irdi) is not None


def test_parameter_validation(counter_graph: Callable) -> None:
    """Assert error is raised when creating Plugin with invalid parameters"""
    params_invalid = IRDI_PARAMS_VALID | IRDI_PARAMS_INVALID

    # Assert error message contains name of violating parameter
    regex = "|".join(IRDI_PARAMS_INVALID.keys())

    with pytest.raises(ValueError, match=regex):
        IrdiPlugin(graph=counter_graph(), **params_invalid)


@needs_cmem
def test_path_not_exists(counter_graph: Callable) -> None:
    """Assert error is raised if specified input path is not in schema of input entities"""
    path = PATH_TO_URI + "suffix"
    params = IRDI_PARAMS_VALID | {"input_schema_path": path}
    plugin = IrdiPlugin(graph=counter_graph(), **params)
    with pytest.raises(ValueError, match=path):
        plugin.execute(inputs=INPUTS_PATH, context=TestExecutionContext())


@needs_cmem
def test_out_of_irdis(plugin_setup: tuple[IrdiPlugin, list[Entities]]) -> None:
    """Assert error is raised when counter exceeds limit"""
    plugin, inputs = plugin_setup
    graph, identifier = plugin.graph, plugin.counter
    set_counter(graph, identifier, COUNT_MAX)
    with pytest.raises(ValueError, match=identifier):
        plugin.execute(inputs=inputs, context=TestExecutionContext())


def test_no_input(counter_graph: Callable) -> None:
    """Assert error is raised if executed without inputs"""
    plugin = IrdiPlugin(graph=counter_graph(), **IRDI_PARAMS_VALID)
    with pytest.raises(ValueError, match="Input"):
        plugin.execute(inputs=[], context=TestExecutionContext())


def test_invalid_uri(counter_graph: Callable) -> None:
    """Assert error is raised if URI of counted object is invalid"""
    params = IRDI_PARAMS_VALID | {"counted_object": COUNTED_OBJECT_INVALID_URI}
    with pytest.raises(ValueError, match=COUNTED_OBJECT_INVALID_URI):
        IrdiPlugin(graph=counter_graph(), **params)
