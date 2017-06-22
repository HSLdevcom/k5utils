#!/bin/sh

set -eu

cd /vol

if [ -f identity.sh ]; then
  . identity.sh
else
  echo
  echo "ERROR: Cannot find file identity.sh from volume"
  echo "ERROR: Unable to source authentication credentials"
  echo
fi

/usr/bin/openstack "$@"
