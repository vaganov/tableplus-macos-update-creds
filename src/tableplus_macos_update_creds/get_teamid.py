import subprocess
import sys


__all__ = ['get_teamid']


def get_teamid(app_path: str) -> str:
    result = subprocess.run(
        ['codesign', '-dv', '--verbose=4', app_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        print(result.stderr.decode(), end='', file=sys.stderr, flush=True)
        raise RuntimeError(result.returncode)

    mapping = {}
    for line in result.stderr.decode().split('\n'):  # codesign outputs to stderr
        tokens = line.split('=')
        if len(tokens) == 2:
            key, value = tokens
            mapping[key] = value

    return mapping['TeamIdentifier']
