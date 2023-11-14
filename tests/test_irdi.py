"""Plugin tests."""
import random
import string

from cmem_plugin_irdi.item_code import generate_item_code
from cmem_plugin_irdi.utils import base_36_encode
from tests.utils import needs_cmem

COUNTER_GRAPH = "https://example.org/counters"


def test_encode():
    assert base_36_encode(100) == "2s"


@needs_cmem
def test_item_code():
    """test creation of item code"""
    identifier = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    ic_0 = generate_item_code(COUNTER_GRAPH, identifier)
    for i in range(20):
        ic_n = generate_item_code(COUNTER_GRAPH, identifier)

    assert ic_0 == "1"
    assert ic_n == "l"
