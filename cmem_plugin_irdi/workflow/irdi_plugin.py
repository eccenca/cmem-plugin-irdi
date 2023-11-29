"""IRDI creation Plugin"""
import re
from typing import Sequence, Optional

from cmem_plugin_base.dataintegration.context import ExecutionContext
from cmem_plugin_base.dataintegration.description import Plugin, PluginParameter
from cmem_plugin_base.dataintegration.entity import (
    Entities, Entity, EntitySchema, EntityPath,
)
from cmem_plugin_base.dataintegration.parameter.graph import GraphParameterType
from cmem_plugin_base.dataintegration.plugins import WorkflowPlugin
from cmem_plugin_base.dataintegration.utils import setup_cmempy_user_access

from cmem_plugin_irdi.components import components
from cmem_plugin_irdi.item_code import generate_item_code

PARAMETERS = [
                 PluginParameter(
                     name="graph",
                     label="Graph",
                     description="Graph in which the Item Code (IC) counter is stored",
                     param_type=GraphParameterType(
                         allow_only_autocompleted_values=False)
                 ),
                 PluginParameter(
                     name="irdi_property",
                     label="Property"
                 )
             ] + [
                 parameter["parameter"] for parameter in components.values()]


@Plugin(
    label="IRDI",
    parameters=PARAMETERS)
# PluginParameter(
#     name="graph",
#     label="Graph",
#     description="Graph in which the Item Code (IC) counter is stored",
#     param_type=GraphParameterType(allow_only_autocompleted_values=False)
# ),
# PluginParameter(
#     name="icd",
#     label="ICD",
#     description="International Code Designator"
# ),
# PluginParameter(
#     name="oi",
#     label="OI",
#     description="Organization Identifier"
# ),
# PluginParameter(
#     name="opi",
#     label="OPI",
#     description="Organization Part Identifier"
# ),
# PluginParameter(
#     name="opis",
#     label="OPIS",
#     description="OPI Source Indicator"
# ),
# PluginParameter(
#     name="ai",
#     label="AI",
#     description="Additional information"
# ),
# PluginParameter(
#     name="csi",
#     label="CSI",
#     description="Code-space identifier"
# )
class IrdiPlugin(WorkflowPlugin):  # pylint: disable=R0902
    """IRDI Plugin"""

    def __init__(
            self, graph: str, irdi_property: str, icd: str, oi: str, opi: str = "",
            opis: str = "", ai: str = "", csi=None,
    ):  # pylint: disable=C0103,R0913
        # for key, value in kwargs.items():
        #     if regex := components[key]["regex"]:
        #         if re.match(regex, value) is None:
        #             raise ValueError("test")
        #     self.__dict__[key] = value
        self.graph = graph
        self.irdi_property = irdi_property
        self.icd = icd
        self.oi = oi
        self.opi = opi.upper()
        self.opis = opis
        self.ai = ai
        self.csi = csi.upper()

        for component, definition in components.items():
            if value := self.__dict__[component]:
                if re.match(definition["regex"], value) is None:
                    raise ValueError(component + ": wrong format")

        self.counter = icd + oi + opi + opis + ai + csi

    def execute(
            self, inputs: Sequence[Entities], context: ExecutionContext
    ) -> Optional[Entities]:
        setup_cmempy_user_access(context.user)
        schema = EntitySchema(type_uri="urn:type",
                              paths=[EntityPath(self.irdi_property)])
        output = []
        for entities in inputs:
            for entity in entities.entities:
                item_code = generate_item_code(self.graph, self.counter)
                irdi = f"{self.icd}-{self.oi}-{self.opi}-{self.opis}-{self.ai}" \
                       f"#{self.csi}-{item_code}#001"
                output.append(Entity(uri=entity.uri, values=[[irdi]]))

        return Entities(entities=output, schema=schema)
