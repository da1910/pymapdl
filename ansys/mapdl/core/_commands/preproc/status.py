from typing import Optional, Union

from ansys.mapdl.core.mapdl_types import MapdlInt, MapdlFloat


def areas(self, **kwargs):
    """Specifies "Areas" as the subsequent status topic.

    APDL Command: AREAS

    Notes
    -----
    This is a status [STAT] topic command.  Status topic commands are
    generated by the GUI and will appear in the log file (Jobname.LOG) if
    status is requested for some items under Utility Menu> List> Status.
    This command will be immediately followed by a STAT command, which will
    report the status for the specified topic.

    If entered directly into the program, the STAT command should
    immediately follow this command.
    """
    command = f"AREAS,"
    return self.run(command, **kwargs)


def bool(self, **kwargs):
    """Specifies "Booleans" as the subsequent status topic.

    APDL Command: BOOL

    Notes
    -----
    This is a status [STAT] topic command.  Status topic commands are
    generated by the GUI and will appear in the log file (Jobname.LOG) if
    status is requested for some items under Utility Menu> List> Status.
    This command will be immediately followed by a STAT command, which will
    report the status for the specified topic.

    If entered directly into the program, the STAT command should
    immediately follow this command.
    """
    command = f"BOOL,"
    return self.run(command, **kwargs)


def ceqn(self, **kwargs):
    """Specifies "Constraint equations" as the subsequent status topic.

    APDL Command: CEQN

    Notes
    -----
    This is a status [STAT] topic command.  Status topic commands are
    generated by the GUI and will appear in the log file (Jobname.LOG) if
    status is requested for some items under Utility Menu> List> Status.
    This command will be immediately followed by a STAT command, which will
    report the status for the specified topic.

    If entered directly into the program, the STAT command should
    immediately follow this command.
    """
    command = f"CEQN,"
    return self.run(command, **kwargs)


def couple(self, **kwargs):
    """Specifies "Node coupling" as the subsequent status topic.

    APDL Command: COUPLE

    Notes
    -----
    This is a status [STAT] topic command.  Status topic commands are
    generated by the GUI and will appear in the log file (Jobname.LOG) if
    status is requested for some items under Utility Menu> List> Status.
    This command will be immediately followed by a STAT command, which will
    report the status for the specified topic.

    If entered directly into the program, the STAT command should
    immediately follow this command.
    """
    command = f"COUPLE,"
    return self.run(command, **kwargs)


def digit(self, **kwargs):
    """Specifies "Node digitizing" as the subsequent status topic.

    APDL Command: DIGIT

    Notes
    -----
    This is a status [STAT] topic command.  Status topic commands are
    generated by the GUI and will appear in the log file (Jobname.LOG) if
    status is requested for some items under Utility Menu> List> Status.
    This command will be immediately followed by a STAT command, which will
    report the status for the specified topic.

    If entered directly into the program, the STAT command should
    immediately follow this command.
    """
    command = f"DIGIT,"
    return self.run(command, **kwargs)


def elem(self, **kwargs) -> Optional[str]:
    """Specifies "Elements" as the subsequent status topic.

    APDL Command: ELEM

    Notes
    -----

    The STAT command should immediately follow this command,
    which should report the status for the specified topic.
    """
    command = f"ELEM,"
    return self.run(command, **kwargs)


def etype(self, **kwargs) -> Optional[str]:
    """Specify "Element types" as the subsequent status topic.

    APDL Command: ETYPE

    Examples
    --------
    >>> mapdl.et(1, 'SOLID186')
    >>> mapdl.etype()
    >>> mapdl.stat()
     ELEMENT TYPE        1 IS SOLID186     3-D 20-NODE STRUCTURAL SOLID
      KEYOPT( 1- 6)=        0      0      0        0      0      0
      KEYOPT( 7-12)=        0      0      0        0      0      0
      KEYOPT(13-18)=        0      0      0        0      0      0

    Notes
    -----
    This is a status [STAT] topic command.
    The STAT command should immediately follow this command,
    which should report the status for the specified topic.
    """
    return self.run("ETYPE", **kwargs)


def febody(self, **kwargs):
    """Specifies "Body loads on elements" as the subsequent status topic.

    APDL Command: FEBODY

    Notes
    -----
    This is a status [STAT] topic command.  Status topic commands are
    generated by the GUI and will appear in the log file (Jobname.LOG) if
    status is requested for some items under Utility Menu> List> Status.
    This command will be immediately followed by a STAT command, which will
    report the status for the specified topic.

    If entered directly into the program, the STAT command should
    immediately follow this command.
    """
    command = f"FEBODY,"
    return self.run(command, **kwargs)


def fecons(self, **kwargs):
    """Specifies "Constraints on nodes" as the subsequent status topic.

    APDL Command: FECONS

    Notes
    -----
    This is a status [STAT] topic command.  Status topic commands are
    generated by the GUI and will appear in the log file (Jobname.LOG) if
    status is requested for some items under Utility Menu> List> Status.
    This command will be immediately followed by a STAT command, which will
    report the status for the specified topic.

    If entered directly into the program, the STAT command should
    immediately follow this command.
    """
    command = f"FECONS,"
    return self.run(command, **kwargs)


def fefor(self, **kwargs):
    """Specifies "Forces on nodes" as the subsequent status topic.

    APDL Command: FEFOR

    Notes
    -----
    This is a status [STAT] topic command.  Status topic commands are
    generated by the GUI and will appear in the log file (Jobname.LOG) if
    status is requested for some items under Utility Menu> List> Status.
    This command will be immediately followed by a STAT command, which will
    report the status for the specified topic.

    If entered directly into the program, the STAT command should
    immediately follow this command.
    """
    command = f"FEFOR,"
    return self.run(command, **kwargs)


def fesurf(self, **kwargs):
    """Specifies "Surface loads on elements" as the subsequent status topic.

    APDL Command: FESURF

    Notes
    -----
    This is a status [STAT] topic command.  Status topic commands are
    generated by the GUI and will appear in the log file (Jobname.LOG) if
    status is requested for some items under Utility Menu> List> Status.
    This command will be immediately followed by a STAT command, which will
    report the status for the specified topic.

    If entered directly into the program, the STAT command should
    immediately follow this command.
    """
    command = f"FESURF,"
    return self.run(command, **kwargs)


def geometry(self, **kwargs):
    """Specifies "Geometry" as the subsequent status topic.

    APDL Command: GEOMETRY

    Notes
    -----
    This is a status [STAT] topic command.  Status topic commands are
    generated by the GUI and will appear in the log file (Jobname.LOG) if
    status is requested for some items under Utility Menu> List> Status.
    This command will be immediately followed by a STAT command, which will
    report the status for the specified topic.

    If entered directly into the program, the STAT command should
    immediately follow this command.
    """
    command = f"GEOMETRY,"
    return self.run(command, **kwargs)


def keypts(self, **kwargs):
    """Specifies "Keypoints" as the subsequent status topic.

    APDL Command: KEYPTS

    Notes
    -----
    This is a status [STAT] topic command.  Status topic commands are
    generated by the GUI and will appear in the log file (Jobname.LOG) if
    status is requested for some items under Utility Menu> List> Status.
    This command will be immediately followed by a STAT command, which will
    report the status for the specified topic.

    If entered directly into the program, the STAT command should
    immediately follow this command.
    """
    command = f"KEYPTS,"
    return self.run(command, **kwargs)


def line(self, **kwargs):
    """Specifies "Lines" as the subsequent status topic.

    APDL Command: LINE

    Notes
    -----
    This is a status [STAT] topic command.  Status topic commands are
    generated by the GUI and will appear in the log file (Jobname.LOG) if
    status is requested for some items under Utility Menu> List> Status.
    This command will be immediately followed by a STAT command, which will
    report the status for the specified topic.

    If entered directly into the program, the STAT command should
    immediately follow this command.
    """
    command = f"LINE,"
    return self.run(command, **kwargs)


def mater(self, **kwargs):
    """Specifies "Material properties" as the subsequent status topic.

    APDL Command: MATER

    Notes
    -----
    This is a status [STAT] topic command.  Status topic commands are
    generated by the GUI and will appear in the log file (Jobname.LOG) if
    status is requested for some items under Utility Menu> List> Status.
    This command will be immediately followed by a STAT command, which will
    report the status for the specified topic.

    If entered directly into the program, the STAT command should
    immediately follow this command.
    """
    command = f"MATER,"
    return self.run(command, **kwargs)


def meshing(self, **kwargs):
    """Specifies "Meshing" as the subsequent status topic.

    APDL Command: MESHING

    Notes
    -----
    This is a status [STAT] topic command.  Status topic commands are
    generated by the GUI and will appear in the log file (Jobname.LOG) if
    status is requested for some items under Utility Menu> List> Status.
    This command will be immediately followed by a STAT command, which will
    report the status for the specified topic.

    If entered directly into the program, the STAT command should
    immediately follow this command.
    """
    command = f"MESHING,"
    return self.run(command, **kwargs)


def nodes(self, **kwargs):
    """Specifies "Nodes" as the subsequent status topic.

    APDL Command: NODES

    Notes
    -----
    This is a status [STAT] topic command.  Status topic commands are
    generated by the GUI and will appear in the log file (Jobname.LOG) if
    status is requested for some items under Utility Menu> List> Status.
    This command will be immediately followed by a STAT command, which will
    report the status for the specified topic.

    If entered directly into the program, the STAT command should
    immediately follow this command.
    """
    command = f"NODES,"
    return self.run(command, **kwargs)


def prim(self, **kwargs):
    """Specifies "Solid model primitives" as the subsequent status topic.

    APDL Command: PRIM

    Notes
    -----
    This is a status [STAT] topic command.  Status topic commands are
    generated by the GUI and will appear in the log file (Jobname.LOG) if
    status is requested for some items under Utility Menu> List> Status.
    This command will be immediately followed by a STAT command, which will
    report the status for the specified topic.

    If entered directly into the program, the STAT command should
    immediately follow this command.
    """
    command = f"PRIM,"
    return self.run(command, **kwargs)


def rcon(self, **kwargs):
    """Specifies "Real constants" as the subsequent status topic.

    APDL Command: RCON

    Notes
    -----
    This is a status [STAT] topic command.  Status topic commands are
    generated by the GUI and will appear in the log file (Jobname.LOG) if
    status is requested for some items under Utility Menu> List> Status.
    This command will be immediately followed by a STAT command, which will
    report the status for the specified topic.

    If entered directly into the program, the STAT command should
    immediately follow this command.
    """
    command = f"RCON,"
    return self.run(command, **kwargs)


def selm(self, **kwargs):
    """Specifies "Superelements" as the subsequent status topic.

    APDL Command: SELM

    Notes
    -----
    This is a status [STAT] topic command.  Status topic commands
    are generated by the GUI and will appear in the log file
    (Jobname.LOG) if status is requested for some items under
    Utility Menu> List> Status.  This command will be immediately
    followed by a STAT command, which will report the status for
    the specified topic.

    If entered directly into the program, the STAT command should
    immediately follow this command.

    Distributed ANSYS Restriction: This command is not supported in
    Distributed ANSYS.
    """
    return self.run("SELM,", **kwargs)


def tble(self, **kwargs):
    """Specifies "Data table properties" as the subsequent status topic.

    APDL Command: TBLE

    Notes
    -----
    This is a status (STAT) topic command.  Status topic commands are
    generated by the GUI and will appear in the log file (Jobname.LOG) if
    status is requested for some items under Utility Menu> List> Status.
    This command will be immediately followed by a STAT command, which will
    report the status for the specified topic.

    If entered directly into the program, the STAT command should
    immediately follow this command.
    """
    command = f"TBLE,"
    return self.run(command, **kwargs)


def volumes(self, **kwargs):
    """Specifies "Volumes" as the subsequent status topic.

    APDL Command: VOLUMES

    Notes
    -----
    This is a status [STAT] topic command.  Status topic commands are
    generated by the GUI and appear in the log file (Jobname.LOG) if status
    is requested for some items by choosing Utility Menu> List> Status.
    This command will be immediately followed by a STAT command, which will
    report the status for the specified topic.

    If entered directly into the program, the STAT command should
    immediately follow this command.
    """
    command = f"VOLUMES,"
    return self.run(command, **kwargs)
