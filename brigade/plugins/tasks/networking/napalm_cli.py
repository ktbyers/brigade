from brigade.core.task import Result

from napalm import get_network_driver


def napalm_cli(task, commands, hostname=None, username=None, password=None,
               driver=None, timeout=60, optional_args=None):
    """
    Run commands on remote devices using napalm

    Arguments:
        commands (list): list of commands to execute on the device
        hostname (string, optional): defaults to ``brigade_ip``
        username (string, optional): defaults to ``brigade_username``
        password (string, optional): defaults to ``brigade_password``
        driver (string, optional): defaults to ``nos``
        timeout (int, optional): defaults to 60
        optional_args (dict, optional): defaults to ``{"port": task.host["napalm_port"]}``


    Returns:
        :obj:`brigade.core.task.Result`:
          * result (``dict``): dictionary with the result of the commands
    """
    parameters = {
        "hostname": hostname or task.host["brigade_ip"],
        "username": username or task.host["brigade_username"],
        "password": password or task.host["brigade_password"],
        "timeout": timeout,
        "optional_args": optional_args or {"port": task.host["napalm_port"]},
    }
    network_driver = get_network_driver(driver or task.host["nos"])

    with network_driver(**parameters) as device:
        result = device.cli(commands)
    return Result(host=task.host, result=result)
