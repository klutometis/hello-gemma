load("@rules_python//python:pip.bzl", "compile_pip_requirements")
load("@pip//:requirements.bzl", "requirement")
load("@rules_python//python:py_binary.bzl", "py_binary")

package(default_visibility = ["//visibility:public"])

# NB: Regenaret `requirements.txt` with:
#
#   bazel run :requirements.update
#
compile_pip_requirements(
    name = "requirements",
    src = "requirements.in",
    requirements_txt = "requirements.txt",
    visibility = ["//visibility:public"],
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
    data = [":requirements", "//data:params.json", "//data:nurse.prompt"],
)
