from getpass import getpass
import subprocess
import sys
from typing import Optional

from .get_teamid import get_teamid


__all__ = ['update_password_in_keychain']


def update_password_in_keychain(
        password: str,
        *,
        account_name: str,
        app_path: str,
        service_name: str,
        teamid: Optional[str] = None,
        keychain_password: Optional[str] = None,
):
    result = subprocess.run(
        [
            'security', 'add-generic-password',
            '-a', account_name,  # Specify account name
            '-s', service_name,  # Specify service name
            '-w', password,  # Specify password to be added
            # '-T', '/usr/bin/security',  # Specify an application which may access this item
            # '-T', app_path,  # (multiple -T options are allowed)
            '-U',  # Update item if it already exists
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        print(result.stderr.decode(), end='', file=sys.stderr, flush=True)
        raise RuntimeError(result.returncode)

    teamid = teamid or get_teamid(app_path)
    keychain_password = keychain_password or getpass(prompt='Please enter password for the default keychain: ')

    # https://mostlikelee.com/blog-1/2017/9/16/scripting-the-macos-keychain-partition-ids
    result = subprocess.run(
        [
            'security', 'set-generic-password-partition-list',
            '-a', account_name,  # Specify account name
            '-s', service_name,  # Specify service name
            '-S', f'apple-tool:,teamid:{teamid}',  # Comma-separated list of allowed partition IDs
            '-k', keychain_password,  # The password for the keychain
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        print(result.stderr.decode(), end='', file=sys.stderr, flush=True)
        raise RuntimeError(result.returncode)
