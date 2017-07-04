#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import sys
import json
import requests

from uuid import uuid4
from time import sleep
from base64 import b64encode
from argparse import ArgumentParser

from keystoneauth1 import session as v1session
from keystoneauth1.identity import v3 as v1identity
from keystoneclient.v3 import client as v3client
from swiftclient.service import SwiftError, SwiftService, SwiftUploadObject

from pprint import pprint

IMPORT_STATUS_INTERVAL = 42
IMPORT_STATUS_MSG = 'Status: HTTP {} {} ({}%)'
IMPORT_BASE_URL = 'https://vmimport.{}.cloud.global.fujitsu.com/v1/imageimport'

HELP_MIN_DISK = 'Minimum amount of disk space required to use the image'
HELP_MIN_RAM = 'Minimum amount of memory required to use the image'

# "Fujitsu Cloud Service K5 IaaS Foundation Service API Reference version 2.0"
# says that the possible values include: Rhel | centos | ubuntu
# "Fujitsu Cloud Service K5 IaaS Features Handbook version 2.7" says the
# possible values include: rhel6 | rhel7 | centos | ubuntu
HELP_OS_TYPE = \
"""Specify the type of the operating system. See some documentation for
possible values. If not specified, default value 'ubuntu' is used."""


def get_env(name):
    try:
        val = os.environ[name]
    except KeyError as e:
        print("error: Environment variable %s not set" % name, file=sys.stderr)
        sys.exit(1)
    return val


def get_auth_token(opts):
    auth = v1identity.Password(
        auth_url=opts['auth_url'],
        username=opts['username'],
        password=opts['password'],
        project_id=opts['project_id'],
        user_domain_name=opts['domain_name']
    )
    return v1session.Session(auth=auth).get_auth_headers()


def upload(opts):
    image = SwiftUploadObject(opts['image_file'])
    with SwiftService({'os_auth_token': opts['os_auth_token']}) as swift:
        try:
            for res in swift.upload(opts['container'], [image]):
                if 'response_dict' in res:
                    res['response_dict']['response_dicts'] = []
                pprint(res)
        except SwiftError as e:
            print("error: %s" % str(e), file=sys.stderr)


def register(opts):
    action_url = IMPORT_BASE_URL.format(opts['region'])
    location = '/v1/AUTH_{}/{}/{}'.format(
        opts['project_id'],
        opts['container'],
        opts['image_file']
    )
    headers = ({
        'Content-Type': 'application/json',
        'X-Auth-Token': opts['os_auth_token']
    })
    payload = {
        'id': opts['image_id'],
        'name': opts['image_name'],
        'location': location,
        'conversion': 'true',
        'disk_format': 'raw',
        'os_type': opts['os_type'],
        'user_name': opts['username'],
        'password': b64encode(opts['password']),
        'domain_name': opts['domain_name']
    }

    if opts['sha1']:
        payload.update({ 'checksum': opts['sha1'] })
    if opts['min_ram']:
        payload.update({ 'min_ram': opts['min_ram'] })
    if opts['min_disk']:
        payload.update({ 'min_disk': opts['min_disk'] })

    pprint(payload)
    job = requests.post(action_url, headers=headers, data=json.dumps(payload)).json()
    pprint(job)

    countdown = 99
    status_url = (IMPORT_BASE_URL + '/{}/status').format(opts['region'], job['import_id'])

    while countdown > 0:
        countdown -= 1
        res = requests.get(status_url, headers=headers)
        data = res.json()
        pprint(data)
        status = data.get('import_status', 'unknown')
        print(IMPORT_STATUS_MSG.format(res.status_code, status, data.get('progress', '?')))
        if status not in ['succeeded', 'failed']:
            sleep(IMPORT_STATUS_INTERVAL)
        else:
            return status


def main():
    parser = ArgumentParser()
    parser.add_argument('-d', '--min-disk', type=int, help=HELP_MIN_DISK)
    parser.add_argument('-r', '--min-ram', type=int, help=HELP_MIN_RAM)
    parser.add_argument('-o', '--os-type', help=HELP_OS_TYPE)
    parser.add_argument('-c', '--sha1', help='SHA1 checksum of the image file')
    parser.add_argument('CONTAINER', help='Name of the object storage container')
    parser.add_argument('FILE', help='Path to the VMDK image file')
    parser.add_argument('NAME', help='Name of the image')
    args = parser.parse_args()

    path = os.path.abspath(args.FILE)

    if not os.path.exists(path) or not os.path.isfile(path):
        print("error: Could not find image file: %s" % path, file=sys.stderr)
        sys.exit(1)

    os.chdir(os.path.dirname(path))

    opts = {
        'region': get_env('OS_REGION_NAME'),
        'auth_url': get_env('OS_AUTH_URL'),
        'username': get_env('OS_USERNAME'),
        'password': get_env('OS_PASSWORD'),
        'project_id': get_env('OS_PROJECT_ID'),
        'project_name': get_env('OS_PROJECT_NAME'),
        'container': args.CONTAINER,
        'image_id': str(uuid4()),
        'image_name': args.NAME,
        'image_file': os.path.basename(path),
        'os_type': args.os_type if args.os_type else 'ubuntu',
        'min_disk': args.min_disk if args.min_disk else None,
        'min_ram': args.min_ram if args.min_ram else None,
        'sha1': args.sha1 if args.sha1 else None
    }

    if 'CONTRACT' in os.environ:
        opts.update({ 'domain_name': os.environ['CONTRACT'] })
    elif 'OS_DEFAULT_DOMAIN' in os.environ:
        opts.update({ 'domain_name': os.environ['OS_DEFAULT_DOMAIN'] })
    else:
        print("error: Environment variables CONTRACT or OS_DEFAULT_DOMAIN not set", file=sys.stderr)
        sys.exit(1)

    try:
        auth_headers = get_auth_token(opts)
    except:
        print("error: Authentication failed", file=sys.stderr)
        print("error: Please check required environment variables", file=sys.stderr)
        sys.exit(1)

    opts.update({
        'os_auth_token': auth_headers.get('X-Auth-Token', None)
    })

    if not opts['os_auth_token']:
        print("error: Unable to get authentication token", file=sys.stderr)
        print("error: Please check required environment variables", file=sys.stderr)
        sys.exit(1)

    pprint(opts)
    upload(opts)
    status = register(opts)

    if status != 'succeeded':
        print("error: Image import failed", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
