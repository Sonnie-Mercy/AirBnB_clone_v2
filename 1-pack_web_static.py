#!/usr/bin/python3
"""
This is a Fabric script that generates a .tgz archive from the contents
of the web_static folder using the function do_pack.
"""
import os
from datetime import datetime
from fabric.api import local, runs_once


@runs_once
def do_pack():
    """The function do_pack that does the archiving."""
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    dtime = datetime.now()
    output = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        dtime.year,
        dtime.month,
        dtime.day,
        dtime.hour,
        dtime.minute,
        dtime.second
    )
    try:
        print("Packing web_static to {}".format(output))
        local("tar -cvzf {} web_static".format(output))
        size = os.stat(output).st_size
        print("web_static packed: {} -> {} Bytes".format(output, size))
    except Exception:
        output = None
    return output
