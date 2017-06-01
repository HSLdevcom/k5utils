
# oscad

OpenStackClient in Alpine Linux Docker container.

## Usage

Following assumes that you have tagged your image as `oscad`. If another name
was used, adapt the commands as necessary.

A volume is used to share authentication credentials and other information with
the container. To convey credentials to the container, create a file
`identity.sh` and bind mount the enclosing directory. File should be sourceable
by the shell and it should set meaningful values for environment variables for
your OpenStack environment. Some example variables:

    export OS_USERNAME=
    export OS_PASSWORD=
    export OS_REGION_NAME=
    export OS_PROJECT_NAME=
    export OS_PROJECT_ID=
    export OS_AUTH_URL=
    export OS_IDENTITY_API_VERSION=
    export OS_DEFAULT_DOMAIN=
    export OS_USER_DOMAIN_NAME=

The `openstack` command is set as the entrypoint to the container, thus any and
all arguments are passed to it by default. Assuming the `identity.sh` is in
current working directory, following should work:

    docker run -ti --rm -v $(pwd):/opt oscad <ARGS...>

If you whish to run any other command (such as `heat` or `nova`) or inspect the
container, change the entrypoint:

    docker run -ti --rm -v $(pwd):/opt --entrypoint /bin/sh oscad

You must source authentication credentials manually when using non-default
entrypoint!
