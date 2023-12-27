import subprocess
import psutil
from dld_tools.core.config import cfg


def parse_lol_auth_info(pid):
    process = psutil.Process(pid)
    cmdline = process.cmdline()
    cmd_info = {}

    for cmd in cmdline:
        if cmd and "=" in cmd:
            key, value = cmd[2:].split('=', 1)
            cmd_info[key] = value

    return cmd_info


def get_lol_process_pid():
    try:
        processes = subprocess.check_output(
            'tasklist /FI "imagename eq LeagueClientUx.exe" /NH', shell=True
        )
    except Exception:
        return 0

    if b"LeagueClientUx.exe" in processes:
        arr = processes.split()
        return int(arr[1])
    else:
        return 0


def is_lol_game_process_exist():
    processes = subprocess.check_output(
        'tasklist /FI "imagename eq League of Legends.exe" /NH', shell=True
    )

    return b"League of Legends.exe" in processes

