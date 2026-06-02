import subprocess

UPDATE_TYPES = (
    "Available",
    "Security",
    "Bug fix",
    "Enhancement",
)


def get_updates():

    result = subprocess.run(
        ["pkcon", "--plain", "get-updates"],
        capture_output=True,
        text=True,
        env={"LANG": "C"}
    )

    output = result.stdout + result.stderr

    count = sum(
        1
        for line in output.splitlines()
        if line.startswith(UPDATE_TYPES)
    )

    return count, output


def install_updates():

    result = subprocess.run(
        ["pkcon", "update"],
        capture_output=True,
        text=True
    )

    output = result.stdout + result.stderr

    return result.returncode, output