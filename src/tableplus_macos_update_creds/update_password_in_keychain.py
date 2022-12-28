from getpass import getpass
import errno
import subprocess
import sys
from typing import Optional

from .get_teamid import get_teamid


__all__ = ['update_password_in_keychain']


def update_password_in_keychain(
        password: str,
        *,
        account_name: str,
        label: Optional[str] = None,
        service_name: str,
        app_path: str,
        teamid: Optional[str] = None,
        keychain_password: Optional[str] = None,
):
    security_add_generic_password_args = [
        'security', 'add-generic-password',
        '-a', account_name,  # Specify account name
        '-s', service_name,  # Specify service name
        '-w', password,  # Specify password to be added
    ]
    if label is not None:
        security_add_generic_password_args += [
            '-l', label,  # Specify label
        ]

    result = subprocess.run(
        security_add_generic_password_args + [
            '-T', app_path,  # Specify an application which may access this item
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode == errno.ENOTSUP:
        # security: SecKeychainItemCreateFromContent (<default>): The specified item already exists in the keychain.
        result = subprocess.run(
            security_add_generic_password_args + [
                '-U',  # Update item if it already exists
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if result.returncode != 0:
            print(result.stderr.decode(), end='', file=sys.stderr, flush=True)
            raise RuntimeError(result.returncode)
    elif result.returncode != 0:
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
            '-S', f'teamid:{teamid}',  # Comma-separated list of allowed partition IDs
            '-k', keychain_password,  # The password for the keychain
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        print(result.stderr.decode(), end='', file=sys.stderr, flush=True)
        raise RuntimeError(result.returncode)
