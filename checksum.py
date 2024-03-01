import base64
import hashlib
from pathlib import Path
import sys
import textwrap


def main():
    dep_checksums = []
    for dep in sorted(sys.argv[1:]):
        # In general, dep is a glob
        for path in sorted(Path().glob(dep)):
            dep_checksums.append((path, hashlib.md5(path.read_bytes()).hexdigest()))
    dep_checksums_str = "\n".join(
        [f"{path} {checksum}" for path, checksum in dep_checksums]
    )
    sys.stderr.write(
        f"Dependency checksums:\n{textwrap.indent(dep_checksums_str, '    ')}\n"
    )
    overall_checksum = base64.urlsafe_b64encode(
        hashlib.md5(dep_checksums_str.encode()).digest()
    ).decode()
    sys.stderr.write(f"Overall checksum: {overall_checksum}\n")
    sys.stdout.write(overall_checksum)


if __name__ == "__main__":
    main()
