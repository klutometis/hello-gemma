load("@pip//:requirements.bzl", "requirement")
load("@rules_python//python:pip.bzl", "compile_pip_requirements")
load("@rules_python//python:py_binary.bzl", "py_binary")

# NB: Regenaret `requirements.txt` with:
#
#   bazel run :requirements.update
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
        requirement("google-cloud-aiplatform"),
        requirement("langchain-google-vertexai"),
        requirement("pyparsing"),
        requirement("twilio"),
    ],
    data = [":requirements", "params.json", "nurse.prompt"],
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

sh_library(name = "venv", srcs = ["venv.sh"])

sh_test(
    name = "lint",
    srcs = ["lint.sh"],
    data = [
        ":venv",
        ":main",
    ],
    tags = ["local"],
)

sh_binary(name = "run", srcs = ["run.sh"], data = [":main", "params.json"])

sh_binary(name = "call", srcs = ["call.sh"], data = [":main"])
