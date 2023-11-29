"""creating and storing item codes"""
from cmem.cmempy.queries import SparqlQuery
from cmem_plugin_irdi.utils import base_36_encode

GET_COUNT: SparqlQuery = SparqlQuery(text="""
    PREFIX co: <http://purl.org/ontology/co/core#>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    SELECT ?count FROM <{{graph}}> WHERE {
        ?counter a co:Counter ;
                 dcterms:identifier "{{identifier}}" ;
                 co:count ?count .
    }
    """)

UPDATE_COUNT: SparqlQuery = SparqlQuery(text="""
    PREFIX co: <http://purl.org/ontology/co/core#>
    PREFIX dcterms: <http://purl.org/dc/terms/>

    WITH <{{graph}}>
    DELETE {
        ?counter co:count ?count_old .
    }
    INSERT {
        ?counter a co:Counter ;
                dcterms:identifier "{{identifier}}" ;
                co:count ?count_new .
    }
    USING <{{graph}}>
    WHERE {
        OPTIONAL {
            ?counter a co:Counter ;
                     dcterms:identifier "{{identifier}}" ;
                     co:count ?count_old .
            BIND((?count_old + 1) as ?count_new)
        }
        OPTIONAL {
            BIND(URI(CONCAT("https://example.org/counter/",SHA256("{{identifier}}")))
                as ?counter)
            BIND(1 as ?count_new)
        }
    }
""", query_type="UPDATE")


# TODO max IC length
def generate_item_code(graph: str, identifier: str) -> str:
    """Generates a base 36 IC (item code)

    :param graph: The graph in which the counter and its value is stored
    :param identifier: A unique identifier for the counter.
    :return: A base 36 item code
    """
    # setup_cmempy_user_access()

    placeholders = {"graph": graph, "identifier": identifier}

    UPDATE_COUNT.get_results(placeholder=placeholders)

    res = GET_COUNT.get_json_results(placeholder=placeholders)

    # TODO empty result
    count = int(res["results"]["bindings"][0]["count"]["value"])

    item_code = base_36_encode(count)
    if len(item_code) > 6:
        raise ValueError(f"Maximum Item Code length (6) for "
                         f"counter {identifier} reached")

    return item_code
