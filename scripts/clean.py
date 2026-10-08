"""
Clean generated datasets and intermediate files
"""

import os
import shutil


def main():
    targets = [
        'data',
        'merged_ipv4.tsv',
        'merged_ipv6.tsv',
        'geoip_ipv4.mmdb',
        'geoip_ipv6.mmdb',
        'geoip.mmdb',
    ]

    for target in targets:
        if os.path.isdir(target):
            shutil.rmtree(target, ignore_errors=True)
            print(f"Removed directory: {target}")
        elif os.path.isfile(target):
            try:
                os.remove(target)
                print(f"Removed file: {target}")
            except OSError as e:
                print(f"Error removing {target}: {e}")


if __name__ == '__main__':
    main()
