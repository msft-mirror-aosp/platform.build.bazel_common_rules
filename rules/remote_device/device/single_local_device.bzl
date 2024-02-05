load("//build/bazel_common_rules/rules/remote_device/device:device_environment.bzl", "DeviceEnvironment")

def _local_device_impl(ctx):
    ctx.actions.expand_template(
        template = ctx.file._source_script,
        output = ctx.outputs.out,
        is_executable = True,
    )

    return DeviceEnvironment(
        runner = depset([ctx.outputs.out]),
        data = ctx.runfiles(files = [ctx.outputs.out]),
    )

local_device = rule(
    attrs = {
        "_source_script": attr.label(
            default = ":single_local_device.sh",
            allow_single_file = True,
        ),
        "out": attr.output(mandatory = True),
    },
    implementation = _local_device_impl,
)