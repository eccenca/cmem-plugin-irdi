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
            param_type=GraphParameterType(allow_only_autocompleted_values=False)
        )
    ])
class IrdiPlugin(WorkflowPlugin):
    """IRDI Plugin"""
    def __init__(self, graph: str):
        self.graph = graph

    def execute(
            self, inputs: Sequence[Entities], context: ExecutionContext
    ) -> Optional[Entities]:
        pass
