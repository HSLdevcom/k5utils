#!/bin/sh

set -eu

if [ -f "/opt/identity.sh" ]; then
  . "/opt/identity.sh"
else
  echo
  echo "ERROR: File /opt/identity.sh not found"
  echo "ERROR: Unable to source authentication credentials"
  echo
fi

/usr/bin/openstack "$@"
