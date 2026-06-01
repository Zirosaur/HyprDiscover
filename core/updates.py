import subprocess


def get_updates():

    result = subprocess.run(
        ["pkcon", "get-updates"],
        capture_output=True,
        text=True
    )

    output = result.stdout + result.stderr

    count = sum(
        1 for line in output.splitlines()
        if any(
            line.startswith(x)
            for x in [
                "Tersedia",
                "Keamanan",
                "Perbaikan bug",
                "Enhancement"
            ]
        )
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