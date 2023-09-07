#!/usr/bin/python3
"""
This is a fabric script to distribute an archive to web servers
using the function do_deploy:
"""

import os
from datetime import datetime
from fabric.api import env, local, put, run, cd

env.hosts = ['100.25.138.158', '18.214.87.67']


def do_deploy(archive_path):
    """Deploys the static files to the host servers."""
    if not os.path.exists(archive_path):
        return False

    try:
        file_name = os.path.basename(archive_path)
        folder_name = file_name.replace(".tgz", "")
        folder_path = "/data/web_static/releases/{}/".format(folder_name)
        # Upload the archive to the /tmp/ directory on the web server
        put(archive_path, "/tmp/{}".format(file_name))
        # Create the release directory and unpack the archive
        with cd("/data/web_static/releases/"):
            run("sudo mkdir -p {}".format(folder_name))
            run("sudo tar -xzf /tmp/{} -C {}".format(file_name, folder_name))

        # Remove the temporary archive
        run("sudo rm /tmp/{}".format(file_name))

        # Move the contents to the appropriate location
        with cd(folder_path):
            run("sudo mv web_static/* .")
            run("sudo rm -rf web_static")

        # Update the symbolic link
        with cd("/data/web_static/"):
            run("sudo rm -rf current")
            run("sudo ln -s {} current".format(folder_path))

        print('New version deployed!')
        return True

    except Exception as e:
        return False


# Ensure that the 'versions' directory exists locally
if not os.path.exists("versions"):
    os.mkdir("versions")

# Create a new archive and deploy it
dtime = datetime.now()
output = "versions/web_static_{}{}{}{}{}{}.tgz".format(
    dtime.year,
    dtime.month,
    dtime.day,
    dtime.hour,
    dtime.minute,
    dtime.second
)
local("tar -cvzf {} web_static".format(output))
deploy_result = do_deploy(output)

# Check if the deployment was successful
if deploy_result:
    print("Deployment successful!")
else:
    print("Deployment failed.")
