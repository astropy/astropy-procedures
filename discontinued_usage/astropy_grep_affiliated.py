#!/usr/bin/env python
# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, unicode_literals, print_function

import six
from six.moves.urllib.request import urlopen
from six.moves.urllib.parse import urlencode

import json
import sys
import webbrowser


def get_registry():
    req = urlopen("http://astropy.org/affiliated/registry.json")
    return json.load(req)


def search_astropy_affiliated_packages(args):
    search_string = ' '.join(args)

    registry = get_registry()
    repos = []
    for package in registry['packages']:
        repo_url = package.get('repo_url', '')
        if repo_url.startswith('http://github.com/'):
            if repo_url.endswith('.git'):
                repo_url = repo_url[:-4]
            repos.append('repo:' + repo_url[len('http://github.com/'):])

    query = ' '.join(repos + [search_string])

    url = 'http://github.com/search?' + urlencode({
        'q': query,
        'type': 'Code'})

    print(url)

    webbrowser.open(url)


def main():
    if len(sys.argv) == 1 or '--help' in sys.argv:
        print("Searches for a string across all affiliated packages on github, ")
        print("and opens the results in the default webbrowser.")
        print()
        print("Usage: astropy_grep_affiliated [SEARCH STRING]")
        sys.exit(0)

    search_astropy_affiliated_packages(sys.argv[1:])


if __name__ == '__main__':
    main()
