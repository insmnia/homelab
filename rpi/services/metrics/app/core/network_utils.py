from functools import lru_cache
import subprocess


@lru_cache
def get_self_ip() -> str:
    out = subprocess.check_output("hostname -I", shell=True, text=True)  # noqa: S602, S607
    if not out:
        raise RuntimeError("Couldn't get self ip")

    ips = out.split()

    try:
        return ips[0]
    except IndexError:
        raise RuntimeError("Couldn't get self ip")
