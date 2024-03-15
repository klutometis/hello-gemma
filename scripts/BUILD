sh_binary(
    name = "deploy",
    srcs = ["deploy.sh"],
    data = [
        "@shflags//:shflags",
        "//:main",
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
        "//:main",
    ],
    tags = ["local"],
)

sh_binary(name = "run", srcs = ["run.sh"], data = ["//:main"])

sh_binary(name = "call", srcs = ["call.sh"], data = ["//:main"])
