"""PluginParameters and validation regex's for IRDI components"""
from cmem_plugin_base.dataintegration.description import PluginParameter

components = {
    "icd": {
        "parameter": PluginParameter(
            name="icd",
            label="ICD (International Code Designator): Numeric, 4 characters",
            description="International Code Designator"
        ),
        "regex": r"^\d{4}$"
    },
    "oi": {
        "parameter": PluginParameter(
            name="oi",
            label="OI (Organization Identifier): Numeric, 4 characters",
            description="Organization Identifier"
        ),
        "regex": r"^\d{4}$"
    },
    "opi": {
        "parameter": PluginParameter(
            name="opi",
            label="OPI (Organization Part Identifier): "
                  "Alphanumeric, up to 35 characters (base36)",
            description="Organization Part Identifier",
            default_value=""
        ),
        "regex": r"^[a-zA-Z0-9]{0,35}$"
    },
    "opis": {
        "parameter": PluginParameter(
            name="opis",
            label="OPIS (OPI Source Indicator): Numeric, 1 character",
            description="OPI Source Indicator",
            default_value=""
        ),
        "regex": r"^\d$"
    },
    "ai": {
        "parameter": PluginParameter(
            name="ai",
            label="AI (Additional information): Numeric, 4 characters",
            description="Additional information",
            default_value=""
        ),
        "regex": r"^\d{4}$"
    },
    "csi": {
        "parameter": PluginParameter(
            name="csi",
            label="CSI (Code-space identifier): Alphanumeric, 2 character (base36)",
            description="Code-space identifier",

        ),
        "regex": r"^[a-zA-Z0-9]{2}$"
    }
}
