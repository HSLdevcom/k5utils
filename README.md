
# k5utils

[bug]: https://github.com/humppa/k5utils/issues
[atc]: https://allthingscloud.eu/2016/07/29/uploading-a-custom-image-to-fujitsu-k5-uk-based-public-cloud

Docker container with OpenStackClient and Fujitsu K5 utilities.

Currently there is only one K5 related utility - a script to upload and
register custom operating system images.

## Prerequisites

The following environment variables should be set inside the container:

* OS_USERNAME
* OS_PASSWORD
* OS_REGION_NAME
* OS_USER_DOMAIN_NAME
* OS_PROJECT_NAME
* OS_PROJECT_ID
* OS_AUTH_URL
* OS_VOLUME_API_VERSION
* OS_IDENTITY_API_VERSION

If you have the values at hand you can pass them to docker with `--env-file`
and `-e`. Or you can use an interactive setup script such as:

* [humppa/k5env-script](https://github.com/humppa/k5env-script)
* [fujitsuk5/k5env-script](https://github.com/fujitsuk5/k5env-script)

If you need to convey any data (for example, the setup script) into the
container environment, use volumes.

## Usage

Build the image:

    docker build -t local/k5utils .

After building the container, just run it:

    docker run -it --rm --env-file=<os.env> local/k5utils

It will drop you to the shell. If you didn't set the environment variables
already you might need to run your setup script now.

The `openstack`, `heat`, `nova`, and `swift` clients are available for you.

### Uploading an image to K5

The script `k5-image-import` uploads and registers custom VMDK formatted
operating system images to K5. It is tested with *uk-1* and *fi-1* regions, but
might work out-of-the-box with other regions too. In any case, using custom
images with K5 is quite intricate, poorly supported, and I recommend you to
read official documentation about the subject.

Usage of the import script:

```
usage: k5-image-import [-h] [--debug] [-d MIN_DISK] [-r MIN_RAM] [-o OS_TYPE]
                       [-c SHA1] CONTAINER FILE NAME

positional arguments:
  CONTAINER             Name of the object storage container
  FILE                  Path to the VMDK image file
  NAME                  Name of the image

optional arguments:
  -h, --help            show this help message and exit
  --debug               Print debug information
  -d MIN_DISK, --min-disk MIN_DISK
                        Minimum amount of disk space required to use the image
                        (GB)
  -r MIN_RAM, --min-ram MIN_RAM
                        Minimum amount of memory required to use the image
                        (MB)
  -o OS_TYPE, --os-type OS_TYPE
                        Specify the type of the operating system. See some
                        documentation for possible values. If not specified,
                        default value 'ubuntu' is used.
  -c SHA1, --sha1 SHA1  (Experimental) SHA1 checksum of the image file
```

## Reporting bugs

If the import utility does not work for you, feel free to create an
[issue][bug]. Good issue should include full debug output (use the `--debug`
switch), but please note, that **debug output contains plaintext and Base64
encoded passwords**. One should sanitize all `password` fields.

## License

[ISC](LICENSE)
