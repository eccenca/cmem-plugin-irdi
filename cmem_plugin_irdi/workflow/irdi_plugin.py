"""IRDI creation Plugin"""
import re
from typing import Sequence  # noqa: UP035

from cmem_plugin_base.dataintegration.context import ExecutionContext
from cmem_plugin_base.dataintegration.description import Plugin, PluginParameter
from cmem_plugin_base.dataintegration.entity import (
    Entities,
    Entity,
    EntityPath,
    EntitySchema,
)
from cmem_plugin_base.dataintegration.parameter.graph import GraphParameterType
from cmem_plugin_base.dataintegration.plugins import WorkflowPlugin
from cmem_plugin_base.dataintegration.utils import setup_cmempy_user_access

from cmem_plugin_irdi.components import components
from cmem_plugin_irdi.item_code import generate_item_code, init_counter

# Version Identifier
VI = "001"

PARAMETERS = [
    PluginParameter(
        name="graph",
        label="Graph",
        description="Graph in which the Item Code (IC) counter is stored",
        param_type=GraphParameterType(allow_only_autocompleted_values=False),
    ),
    PluginParameter(
        name="irdi_property",
        label="Property",
        default_value="http://purl.org/dc/terms/identifier",
        advanced=True,
    ),
    PluginParameter(
        name="csi_label",
        label="CSI label",
        default_value="",
        advanced=True,
    ),
    PluginParameter(
        name="csi_description", label="CSI description", default_value="", advanced=True
    ),
] + [parameter["parameter"] for parameter in components.values()]


@Plugin(label="IRDI", parameters=PARAMETERS)
class IrdiPlugin(WorkflowPlugin):  # pylint: disable=R0902
    """IRDI Plugin"""

    def __init__(  # noqa: PLR0913
        self,
        graph: str,
        icd: str,
        oi: str,
        opi: str,
        opis: str,
        ai: str,
        csi: str,
        csi_label: str,
        csi_description: str,
        irdi_property: str = "http://purl.org/dc/terms/identifier",
    ):
        self.graph = graph
        self.irdi_property = irdi_property
        self.icd = icd
        self.oi = oi
        self.opi = opi.upper()
        self.opis = opis
        self.ai = ai
        self.csi = csi.upper() if csi else ""
        self.csi_label = csi_label or self.csi
        self.csi_description = csi_description

        for component, definition in components.items():
            value = self.__dict__.get(component)
            if value and (re.match(definition["regex"], value) is None):
                raise ValueError(component + ": wrong format")

        self.counter = self.icd + self.oi + self.opi + self.opis + self.ai + self.csi

    def execute(self, inputs: Sequence[Entities], context: ExecutionContext) -> Entities | None:
        """Execute Workflow plugin"""
        setup_cmempy_user_access(context.user)
        init_counter(self.graph, self.counter, self.csi, self.csi_label, self.csi_description)

        schema = EntitySchema(type_uri="urn:type", paths=[EntityPath(self.irdi_property)])
        output = []
        for entities in inputs:
            for entity in entities.entities:
                item_code = generate_item_code(self.graph, self.counter)
                irdi = (
                    f"{self.icd}-{self.oi}-{self.opi}-{self.opis}-{self.ai}"
                    f"#{self.csi}-{item_code}#{VI}"
                )
                output.append(Entity(uri=entity.uri, values=[[irdi]]))

        return Entities(entities=output, schema=schema)
