#!/usr/bin/env python3
import subprocess
from pathlib import Path

def get_local_addresses():
    import netifaces
    ips = set()
    for iface in netifaces.interfaces():
        for addr_type in netifaces.ifaddresses(iface).values():
            for addr in addr_type:
                ips.add(addr["addr"])
    return ips

LOCAL_IPS = get_local_addresses()

BOUND_MOUNT_POINT = "/mnt/netshares"

MACHINES = {
    "odoo@192.168.1.48": [
        ("/home/odoo/prout", "prout"),
        ("/home/odoo/Downloads", "Downloads")
    ],
    "prout@192.168.1.4": [
        ("/home/odoo/Downloads", "Downloads")
    ]
}

MOUNT_TEMPLATE = BOUND_MOUNT_POINT + "/{ip}/{alias}"
SSH_OPTIONS = [
    "-o", "compression=no",
]


def mount_bind(path_from, path_to):
    path_from = Path(path_from)
    if not path_from.exists():
        raise Exception("source for bind invalid")
    cmd = ["bindfs","--no-allow-other", path_from, path_to]


def mount(path_from, path_to, is_local):
    as_path = Path(path_to)

    if is_local

    if not as_path.exists():
        as_path.mkdir(parents=True)
    if is_local:
        cmd = ["bindfs","--no-allow-other", path_from, path_to]
    else:
        cmd = ["sshfs"]
        cmd.extend([
            path_from, path_to
        ])
        cmd.extend(SSH_OPTIONS)

    try:
        subprocess.run(cmd, check=True)
    except Exception as e:
        try:
            as_path.rmdir()
        except Exception as sube:
            print(sube)
        print(e)


for ip_raw, directories in MACHINES.items():
    ip_split = ip_raw.split("@")
    if len(ip_split) == 2:
        user, ip = ip_split
    else:
        ip = ip_split[0]
        user = "ran"
    is_local = ip in LOCAL_IPS
    for dir, alias in directories:
        mount_point =  MOUNT_TEMPLATE.format(ip=ip, alias=alias)
        to_mount = dir if is_local else ip_raw + ":" + dir
        mount(to_mount, mount_point, is_local)
