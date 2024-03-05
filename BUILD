load("@pip//:requirements.bzl", "requirement")
load("@rules_python//python:pip.bzl", "compile_pip_requirements")
load("@rules_python//python:py_binary.bzl", "py_binary")

# NB: Regenaret `requirements.txt` with:
#
#   bazel run :requirpments.update
#
compile_pip_requirements(
    name = "requirements",
    src = "requirements.in",
    requirements_txt = "requirements.txt",
)

py_binary(
    name = "main",
    srcs = ["main.py"],
    deps = [
        requirement("functions-framework"),
        requirement("twilio"),
    ],
    data = [":requirements"],
)

sh_binary(
    name = "deploy",
    srcs = ["deploy.sh"],
    data = [
        "@shflags//:shflags",
        ":main",
    ],
)

sh_binary(
    name = "test",
    srcs = ["test.sh"],
    data = [
        "@shflags//:shflags",
    ],
)

sh_binary(name = "run", srcs = ["run.sh"], data = [":main"])

sh_binary(name = "call", srcs = ["call.sh"], data = [":main"])
