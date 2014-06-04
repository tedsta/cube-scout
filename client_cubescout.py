#!/usr/bin/env python

import subprocess

from src.client import CubeScoutClient

def main():
    client = CubeScoutClient("localhost", 20000)
    while True:
        name = client.receive()
        if name:
            print(name+" is entering the cubicle")
            subprocess.call(["sh", "on_enter.sh", name])

if __name__ == "__main__":
    main()
