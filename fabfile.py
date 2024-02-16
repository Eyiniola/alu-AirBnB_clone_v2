#!/usr/bin/python3
#script that distributes an archive to web servers
from fabric import task, Connection
from fabric.state import env
import os

env.hosts = ['34.224.173.76', '54.196.152.183']
env.user = 'ubuntu'
env.key_filename = '/root/.ssh/'

@task
def do_deploy(c, archive_path):
    """Distribute an archive to web servers"""
    if not os.path.exists(archive_path):
        print(f"Error: Archive not found at {archive_path}")
        return False

    # Upload archive to /tmp/ on web servers
    remote_archive_path = "/tmp/"
    c.put(archive_path, remote_archive_path)

    # Extract archive to /data/web_static/releases/<filename without extension>/
    filename = os.path.basename(archive_path)
    folder_name = os.path.splitext(filename)[0]
    releases_path = "/data/web_static/releases/"
    c.run(f"mkdir -p {releases_path}{folder_name}")
    c.run(f"tar -xzf {remote_archive_path}{filename} -C {releases_path}{folder_name}/")

    # Delete archive from web servers
    c.run(f"rm {remote_archive_path}{filename}")

    # Delete symbolic link /data/web_static/current
    c.run("rm -f /data/web_static/current")

    # Create new symbolic link to the new version
    c.run(f"ln -s {releases_path}{folder_name}/ /data/web_static/current")

    print("Deployment successful.")
    return True

