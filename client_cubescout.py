#!/usr/bin/env python

from src.client import CubeScoutClient

def main():
    client = CubeScoutClient("localhost", 20000)
    while True:
        name = client.receive()
        if name:
            print(name)

if __name__ == "__main__":
    main()
