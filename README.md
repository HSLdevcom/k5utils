
# k5utils

[bug]: https://github.com/humppa/k5utils/issues
[atc]: https://allthingscloud.eu/2016/07/29/uploading-a-custom-image-to-fujitsu-k5-uk-based-public-cloud

Docker container with OpenStackClient and Fujitsu K5 utilities.

Currently there is only one K5 related utility - a script to upload and
register custom operating system images.

## Prerequisites

You need to have a directory, which can be bind mounted to the container. The
directory is used to save and convey authentication credentials (and possibly
any other data) into the containerized environment.

Also `set-k5env.sh` script must reside in the aforementioned directory. It is
used to authenticate, set up environment, and save credentials for future use.
You can download the script from either of these repositories:

* [humppa/k5env-script](https://github.com/humppa/k5env-script)
* [fujitsuk5/k5env-script](https://github.com/fujitsuk5/k5env-script)

## Usage

Following assumes that you have created a directory `~/.k5` and downloaded the
environment script to `~/.k5/set-k5env.sh`.

After building the container, run it:

    docker run -ti --rm -v $HOME/.k5:/vol CONTAINER

It will first set up the environment and the drop you to the shell. The
`openstack`, `heat`, `nova`, and `swift` clients are available.

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
