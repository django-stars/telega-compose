#!/usr/bin/env python

import argparse


def get_version():
    with open('../VERSION', 'r') as f:
        version_str = f.read().strip()
    assert version_str
    version_parts = list(map(int, version_str.split('.')))
    assert len(version_parts) == 3, "Incorrect version pattern"
    return version_parts


def bump_version(major_version, minor_version, patch_version, kind):
    if kind.lower() == 'major':
        return major_version + 1, 0, 0
    elif kind.lower() == 'minor':
        return major_version, minor_version + 1, 0
    elif kind.lower() == 'patch':
        return major_version, minor_version, patch_version + 1
    else:
        assert False, "Wrong kind"


def set_version(version):
    with open('../VERSION', 'w') as f:
        f.write(version)
    print("Bumped to version {version}".format(version=version))


parser = argparse.ArgumentParser()
parser.add_argument('kind', help="major | minor | patch")
args = parser.parse_args()

major, minor, patch = get_version()
new_version = '.'.join(map(str, bump_version(major, minor, patch, args.kind)))
set_version(new_version)
