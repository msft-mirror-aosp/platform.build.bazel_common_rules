#!/usr/bin/env python3
#
# Copyright (C) 2021 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""A script to copy outputs from Bazel rules to a user specified dist directory.

This script is only meant to be executed with `bazel run`. `bazel build <this
script>` doesn't actually copy the files, you'd have to `bazel run` a
copy_to_dist_dir target.

This script copies files from Bazel's output tree into a directory specified by
the user. It does not check if the dist dir already contains the file, and will
simply overwrite it.

One approach is to wipe the dist dir every time this script runs, but that may
be overly destructive and best left to an explicit rm -rf call outside of this
script.

Another approach is to error out if the file being copied already exist in the
dist dir, or perform some kind of content hash checking.
"""

import argparse
import glob
import os
import shutil
import sys


def files_to_dist():
    # Assume that dist.bzl is in the same package as dist.py
    runfiles_directory = os.path.dirname(__file__)
    dist_manifests = glob.glob(
        os.path.join(runfiles_directory, "*_dist_manifest.txt"))
    if not dist_manifests:
        print("Warning: could not find a file ending in *_dist_manifest.txt" +
              "in the runfiles directory: %s" % runfiles_directory)
    files_to_dist = []
    for dist_manifest in dist_manifests:
        with open(dist_manifest, "r") as f:
            files_to_dist += [line.strip() for line in f]
    return files_to_dist


def copy_files_to_dist_dir(files, dist_dir, flat, prefix):
    for src in files:
        if not os.path.isfile(src):
            continue

        src_relpath = os.path.basename(src) if flat else src
        src_relpath = os.path.join(prefix, src_relpath)
        src_abspath = os.path.abspath(src)

        dst = os.path.join(dist_dir, src_relpath)
        dst_dirname = os.path.dirname(dst)
        print("[dist] Copying file: %s" % dst)
        if not os.path.exists(dst_dirname):
            os.makedirs(dst_dirname)

        shutil.copyfile(src_abspath, dst, follow_symlinks=True)


def main():
    parser = argparse.ArgumentParser(
        description="Dist Bazel output files into a custom directory.")
    parser.add_argument(
        "--dist_dir", required=True, help="absolute path to the dist dir")
    parser.add_argument(
        "--flat",
        action="store_true",
        help="ignore subdirectories in the manifest")
    parser.add_argument(
        "--prefix", default="", help="path prefix to apply within dist_dir")
    args = parser.parse_args()

    if not os.path.isabs(args.dist_dir):
        # BUILD_WORKSPACE_DIRECTORY is the root of the Bazel workspace containing
        # this binary target.
        # https://docs.bazel.build/versions/main/user-manual.html#run
        args.dist_dir = os.path.join(
            os.environ.get("BUILD_WORKSPACE_DIRECTORY"), args.dist_dir)

    copy_files_to_dist_dir(files_to_dist(), **vars(args))


if __name__ == "__main__":
    main()
