import subprocess


def get_self_ip() -> str:
    out = subprocess.check_output("hostname -I", shell=True, text=True)  # noqa: S602, S607
    if not out:
        raise RuntimeError("Couldn't get self ip")
    ips = out.split()
    return ips[0]


# SELF_IP = get_self_ip()
SELF_IP = "127.0.0.1"
