#!/usr/bin/python3
"""
This is a fabric script to distribute an archive to web servers
using the function do_deploy:
"""

import os
from datetime import datetime
from fabric.api import env, local, put, run, runs_once


env.hosts = ['100.25.138.158', '18.214.87.67']


def do_deploy(archive_path):
    """Distributes archives to a server
    """
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
        archize_size = os.stat(output).st_size
        print("web_static packed: {} -> {} Bytes".format(output, archize_size))
    except Exception:
        return None


def do_deploy(archive_path):
    """Deploys the static files to the host servers."""
    if not os.path.exists(archive_path):
        return False
    file_name = os.path.basename(archive_path)
    folder_name = file_name.replace(".tgz", "")
    folder_path = "/data/web_static/releases/{}/".format(folder_name)
    success = False
    try:
        put(archive_path, "/tmp/{}".format(file_name))
        run("sudo mkdir -p {}".format(folder_path))
        run("sudo tar -xzf /tmp/{} -C {}".format(file_name, folder_path))
        run("sudo rm -rf /tmp/{}".format(file_name))
        run("sudo mv {}web_static/* {}".format(folder_path, folder_path))
        run("sudo rm -rf {}web_static".format(folder_path))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(folder_path))
        print('New version deployed!')
        success = True
    except Exception:
        return False
