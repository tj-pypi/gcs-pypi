from __future__ import print_function

import argparse
import logging
import sys

from gcspypi2 import __prog__, __version__
from gcspypi2.exceptions import gcspypiError
from gcspypi2.package import Package
from gcspypi2.storage import GCSStorage

log = logging.getLogger()


def create_and_upload_package(args):
    package = Package.create(args.wheel, args.sdist, args.dist_path)
    storage = GCSStorage(
        args.bucket, args.secret, args.bare, args.private, args.profile
    )

    index = storage.get_index(package)
    index.add_package(package, args.force)

    storage.put_package(package, args.dist_path)
    storage.put_index(package, index)


def parse_args(args):
    p = argparse.ArgumentParser(prog=__prog__)
    p.add_argument("--bucket", required=True, help="GCS bucket")
    p.add_argument("--secret", help="GCS secret")
    p.add_argument("--profile", help="AWS profile")
    p.add_argument("--force", action="store_true", help="Overwrite existing packages")
    p.add_argument(
        "--no-wheel", dest="wheel", action="store_false", help="Skip wheel distribution"
    )
    p.add_argument(
        "--no-sdist", dest="sdist", action="store_false", help="Skip sdist distribution"
    )
    p.add_argument(
        "--dist-path", help="Path to directory with wheel/sdist to be uploaded"
    )
    p.add_argument(
        "--bare", action="store_true", help="Store index as bare package name"
    )
    p.add_argument(
        "--private", action="store_true", help="Store GCS Keys as private objects"
    )
    p.add_argument("--verbose", action="store_true", help="Turn on verbose output.")
    p.add_argument("--version", action="version", version=__version__)
    return p.parse_args(args)


def main(*args):
    args = parse_args(args or sys.argv[1:])

    log.setLevel(logging.DEBUG if args.verbose else logging.INFO)

    try:
        create_and_upload_package(args)
    except gcspypiError as e:
        print("error: %s" % e)
        sys.exit(1)


if __name__ == "__main__":
    main()
