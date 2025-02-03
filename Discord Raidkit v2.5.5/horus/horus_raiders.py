"""
horus_raiders.py

This namespace contains raider classes which determine what cogs 
are to be loaded by Horus.
"""

import shared.dr.dr_types as dr_types


class Anubis(dr_types.IH_Raider):
    """A raider that provides the Anubis cogs as its social engineering method.
    """
    def extensions(self) -> list[str]:
        return [
            dr_types.EH_Cogs.aModeration.value,
            dr_types.EH_Cogs.aRaidPrevention.value,
            dr_types.EH_Cogs.aSurfing.value,
            dr_types.EH_Cogs.aHelp.value,
            dr_types.EH_Cogs.sCmds.value,
            dr_types.EH_Cogs.sHandler.value
        ]
    
    def __str__(self) -> str:
        return dr_types.EH_Raiders.ANUBIS.name.title()


class Qetesh(dr_types.IH_Raider):
    """A raider that provides the Quetesh cogs as its social engineering method.
    """
    def extensions(self) -> list[str]:
        return [
            dr_types.EH_Cogs.qNsfw.value,
            dr_types.EH_Cogs.qHelp.value,
            dr_types.EH_Cogs.sCmds.value,
            dr_types.EH_Cogs.sHandler.value
        ]
    
    def __str__(self) -> str:
        return dr_types.EH_Raiders.QETESH.name.title()
