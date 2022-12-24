# tableplus-macos-update-creds
A python library to update credentials for a connection in TablePlus macOS client without using GUI

[TablePlus](https://tableplus.com) is a neat SQL GUI client. As virtually any decent SQL client it allows juggling
multiple connections, storing the credentials [in a secure manner](https://tableplus.com/privacy). However, updating
a lot of ephemeral credentials via GUI may be quite annoying even though importing connections
[is supported](https://docs.tableplus.com/gui-tools/manage-connections#export-and-import-connections).

This library's main goal is to allow updating credentials programmatically, without using GUI.

Please note that this project is not affiliated with TablePlus and all the techniques have been developed through (poor)
reverse engineering. The library has only been tested against TablePlus 4.2.0 (build 388) on macOS 13.1 with python
3.7/3.8/3.9/3.10. The techniques employed may stop working if any of these happens:
- TablePlus changes its connections config format
- TablePlus changes keychain account name format used for storing connection passwords
- macOS changes ACL mechanics
- codesign output format changes

## Example
The following code may be used as a shell script

    #!/usr/bin/env python3
    
    from argparse import ArgumentParser
    import sys
    
    from tableplus_macos_update_creds import update_creds
    
    
    def main():
        parser = ArgumentParser()
        parser.add_argument('--connection', dest='connection')
        parser.add_argument('--username', dest='username')
        parser.add_argument('--password', dest='password')
        args = parser.parse_args(sys.argv[1:])
    
        update_creds(args.connection, username=args.username, password=args.password)
    
    
    if __name__ == '__main__':
        main()
