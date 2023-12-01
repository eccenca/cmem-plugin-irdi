"""IRDI Plugin tests"""
import re
from collections.abc import Iterator

import pytest
from cmem_plugin_base.dataintegration.entity import Entities, Entity, EntitySchema

from cmem_plugin_irdi.utils import base_36_encode
from cmem_plugin_irdi.workflow.irdi_plugin import IrdiPlugin
from tests.utils import TestExecutionContext, drop_graph, get_values, needs_cmem

IRDI_FORMAT = r"^\d{4}-\d{4}-[a-zA-Z0-9]{0,35}-\d-(\d{4})?#[A-Z0-9]{2}-[A-Z0-9]{6}#001"
COUNTERS_GRAPH = "urn:counters_test"
INPUT_GRAPH = "urn:irdi_input_test"
OUTPUT_GRAPH = "urn:irdi_output_test"
IRDI_PARAMS_VALID = {
    "graph": COUNTERS_GRAPH,
    "icd": "1234",
    "oi": "5678",
    "opi": "abcdefg",
    "opis": "5",
    "ai": "9123",
    "csi": "A4",
    "csi_label": "",
    "csi_description": "",
}

IRDI_PARAMS_INVALID = {"icd": "12345", "opis": "a"}

INPUTS = [
    Entities(
        entities=[Entity(uri=f"urn:entity_{i}", values=[[]]) for i in range(10)],
        schema=EntitySchema(type_uri="urn:entity", paths=[]),
    ),
    Entities(
        entities=[Entity(uri=f"urn:entity_{i}", values=[[]]) for i in range(10, 20)],
        schema=EntitySchema(type_uri="urn:entity", paths=[]),
    ),
]


def test_encode() -> None:
    """Test base36 encoding"""
    assert base_36_encode(0) == "0"
    assert base_36_encode(100) == "2S"


@needs_cmem
def test_irdis_created(plugin_results: Entities) -> None:
    """Assert an IRDI was created for every input"""
    for input_entities in INPUTS:
        for input_entity in input_entities.entities:
            match = None
            for result_entity in plugin_results.entities:
                if result_entity.uri == input_entity.uri:
                    match = result_entity
            assert match is not None, f"No output for entity {input_entity.uri}"
            assert len(match.values[0]) > 0, f"No IRDI for entity {input_entity.uri} created"


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


def test_parameter_validation() -> None:
    """Assert error is raised when creating Plugin with invalid parameters"""
    params_invalid = IRDI_PARAMS_VALID
    params_invalid.update(IRDI_PARAMS_INVALID)

    # Assert error message contains name of violating parameter
    regex = "|".join(IRDI_PARAMS_INVALID.keys())

    with pytest.raises(ValueError, match=regex):
        IrdiPlugin(**params_invalid)


@pytest.fixture(scope="module")
def plugin_results() -> Iterator[Entities]:
    """Execute plugin and return created IRDIs"""
    plugin = IrdiPlugin(**IRDI_PARAMS_VALID)
    result = plugin.execute(inputs=INPUTS, context=TestExecutionContext())
    if not result:
        pytest.fail("Failed to execute Plugin")
    else:
        yield result
    drop_graph(COUNTERS_GRAPH)
