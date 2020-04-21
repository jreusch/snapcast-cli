#!/usr/bin/python3
import asyncio
import snapcast.control
import argparse

loop = None

def parse_args():
    parser = argparse.ArgumentParser(description='Control snapcast remotely')

    parser.add_argument('--host', default="localhost", help='snapserver host')
    parser.add_argument('command', help='command to execute')
    parser.add_argument('client', help='client to control')
    parser.add_argument('stream', help='steam to set')

    args = parser.parse_args()
    return args


def get_client(name, server):
    for client in server.clients:
        if client.friendly_name == name:
            return client
    else:
        raise KeyError("client not found: {}".format(name))


def set_stream(server, client_name, stream_name):
    client = get_client(client_name, server)
    loop.run_until_complete(client.group.set_stream(stream_name))


def main():
    global loop
    args = parse_args()
    host = args.host

    loop = asyncio.get_event_loop()
    server = loop.run_until_complete(snapcast.control.create_server(loop, host))

    if args.command == "set-stream":
        set_stream(server, args.client, args.stream)
    else:
        raise NotImplementedError("command not implemented")

#    # print all client names
#    for client in server.clients:
#        print(client.friendly_name)
#        print(client.group.identifier, client.group.friendly_name)

#    for group in server.groups:
#        print(group.identifier, group.friendly_name)


if __name__ == "__main__":
    main()