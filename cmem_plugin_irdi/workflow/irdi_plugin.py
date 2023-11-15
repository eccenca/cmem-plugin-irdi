"""IRDI creation Plugin"""
from typing import Sequence, Optional

from cmem_plugin_base.dataintegration.context import ExecutionContext
from cmem_plugin_base.dataintegration.description import Plugin, PluginParameter
from cmem_plugin_base.dataintegration.entity import (
    Entities,
)
from cmem_plugin_base.dataintegration.parameter.graph import GraphParameterType
from cmem_plugin_base.dataintegration.plugins import WorkflowPlugin


@Plugin(
    label="Irdi",
    parameters=[
        PluginParameter(
            name="graph",
            label="Graph",
            description="Graph in which the Item Code (IC) counter is stored",
            param_type=GraphParameterType(allow_only_autocompleted_values=False)
        ),
        PluginParameter(
            name="icd",
            label="ICD",
            description="International Code Designator"
        ),
        PluginParameter(
            name="oi",
            label="OI",
            description="Organization Identifier"
        ),
        PluginParameter(
            name="opi",
            label="OPI",
            description="Organization Part Identifier"
        ),
        PluginParameter(
            name="opis",
            label="OPIS",
            description="OPI Source Indicator"
        ),
        PluginParameter(
            name="ai",
            label="AI",
            description="Additional information"
        ),
        PluginParameter(
            name="csi",
            label="CSI",
            description="Code-space identifier"
        )
    ])
class IrdiPlugin(WorkflowPlugin):
    """IRDI Plugin"""

    def __init__(
            self, graph: str, icd: str, oi: str, opi: str, opis: str, ai: str, csi: str
    ):  # pylint: disable=C0103,R0913
        self.graph = graph
        self.icd = icd
        self.oi = oi
        self.opi = opi
        self.opis = opis
        self.ai = ai
        self.csi = csi

    def execute(
            self, inputs: Sequence[Entities], context: ExecutionContext
    ) -> Optional[Entities]:
        pass
