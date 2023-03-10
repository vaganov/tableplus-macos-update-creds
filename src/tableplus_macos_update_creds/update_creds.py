import os
import plistlib
import shutil
from tempfile import TemporaryDirectory
from typing import Optional

from .update_password_in_keychain import update_password_in_keychain


__all__ = ['update_creds']


def update_creds(
        connection_name: str,
        *,
        username: str,
        password: str,
        create: bool = False,
        app_path: str = '/Applications/TablePlus.app',
        connections_path: str = '~/Library/Application Support/com.tinyapp.TablePlus/Data/Connections.plist',
        account_name: str = '{ID}_database',
        service_name: str = 'com.tableplus.TablePlus',
        label: Optional[str] = 'TablePlus',
        teamid: Optional[str] = None,
        keychain_password: Optional[str] = None,
):
    """Update TablePlus connection credentials

    The function will first find the specified connection in the TablePlus connections config. It will then update the
    corresponding entry in the system keychain as well as the partition list for that entry so that the password is
    available for TablePlus application. Finally, the TablePlus connections config will be updated.
    The function may raise:
        - 'RuntimeError' if any spawned subprocess ('codesign', 'security') returns non-zero
        - 'KeyError' if specified connection is not present and 'create == False'
        - 'NotImplementedError' if specified connection is not present and 'create == True'

    :param str connection_name: connection name as it is displayed in TablePlus
    :param str username: connection username
    :param str password: connection password
    :param bool create: whether to create a new connection (creating not yet implemented)
    :param str app_path: path to the TablePlus application.
        defaults to '/Applications/TablePlus.app'
    :param str connections_path: path to the TablePath connections config.
        defaults to '~/Library/Application Support/com.tinyapp.TablePlus/Data/Connections.plist'
    :param str account_name: template for account name in the system keychain fulfilled with connection fields.
        defaults to '{ID}_database'
    :param str service_name: service name used by TablePlus in the system keychain.
        defaults to 'com.tableplus.TablePlus'
    :param str label: password entry label in the system keychain.
        defaults to 'TablePlus'
    :param str teamid: teamid used by TablePlus in ACL.
        obtained automatically via 'codesign' if not specified
    :param str keychain_password: password for the default keychain (required to set ACL for keychain entry).
        prompted if not specified
    """
    connections_path = os.path.expanduser(connections_path)
    with open(connections_path, mode='rb') as file:
        connections = plistlib.load(file)

    for connection in connections:
        if connection['ConnectionName'] == connection_name:
            break
    else:
        if create:
            raise NotImplementedError('''Creating connections not yet implemented.
            If you really need this please upvote https://github.com/vaganov/tableplus-macos-update-creds/issues/1''')
        else:
            raise KeyError(f'Connection name "{connection_name}" not found')

    update_password_in_keychain(
        password,
        account_name=account_name.format(**connection),
        label=label,
        service_name=service_name,
        app_path=app_path,
        teamid=teamid,
        keychain_password=keychain_password,
    )

    connection['DatabaseUser'] = username

    # TablePlus would not pick changes in the config file if edited inplace. Moreover, it would override them on close.
    # We have to move another file over instead -- this works fine.
    with TemporaryDirectory() as tmp_dir:
        tmp_path = f'{tmp_dir}/Connections.plist'
        with open(tmp_path, mode='wb') as file:
            plistlib.dump(connections, file)
        shutil.move(src=tmp_path, dst=connections_path)
