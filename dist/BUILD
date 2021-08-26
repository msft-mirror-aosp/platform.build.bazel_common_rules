load(":dist.bzl", "copy_to_dist_dir")
exports_files(["dist.py"])

# bazel run --package_path=out/soong/workspace //build/bazel_common_rules/dist:dist_bionic_example -- --dist_dir=/tmp/dist
copy_to_dist_dir(
    name = "dist_bionic_example",
    data = [
        "//bionic/libc:libc",
        "//bionic/libdl:libdl",
    ],
)
