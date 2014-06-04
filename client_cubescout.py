#!/usr/bin/env python

import sys
import subprocess

from src.client import CubeScoutClient

def main():
    host = "localhost"
    port = 20000
    if len(sys.argv) > 1:
        host = sys.argv[1]
    client = CubeScoutClient(host, port)
    while True:
        name = client.receive()
        if name:
            print(name+" is entering the cubicle")
            subprocess.call(["sh", "on_enter.sh", name])

if __name__ == "__main__":
    main()
