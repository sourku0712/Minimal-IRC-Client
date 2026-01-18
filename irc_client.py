import socket
import sys
import threading
import argparse
import time

RESET = "\033[0m"
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RED = "\033[91m"

def ts():
    return time.strftime("%H:%M:%S")

class IRCClient:
    def __init__(self, server, port, nick, username, channel, color=True):
        self.server = server
        self.port = port
        self.nick = nick
        self.username = username
        self.channel = channel
        self.color = color
        self.sock = None
        self.running = False

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.server, self.port))
        self.running = True

        self.send_cmd(f"NICK {self.nick}")
        self.send_cmd(f"USER {self.username} 0 * :{self.username}")

    def send_cmd(self, cmd):
        if not cmd.endswith("\r\n"):
            cmd += "\r\n"
        self.sock.sendall(cmd.encode("utf-8"))

    def handle_server_message(self, line):
        if line.startswith("PING"):
            payload = line.split(" ", 1)[1]
            self.send_cmd(f"PONG {payload}")
            return

        parts = line.split()
        if len(parts) >= 4 and parts[1] == "PRIVMSG":
            sender = parts[0].split("!")[0][1:]
            channel = parts[2]
            msg = " ".join(parts[3:])[1:]
            self.print_msg(sender, channel, msg)
        else:
            self.print_info(line)

    def recv_loop(self):
        buf = ""
        while self.running:
            try:
                data = self.sock.recv(4096).decode("utf-8", errors="ignore")
                if not data:
                    break
                buf += data
                while "\r\n" in buf:
                    line, buf = buf.split("\r\n", 1)
                    self.handle_server_message(line)
            except Exception:
                break
        self.running = False

    def input_loop(self):
        while self.running:
            try:
                line = sys.stdin.readline()
                if not line:
                    break
                line = line.rstrip("\n")

                if line.startswith("/"):
                    self.handle_user_command(line)
                else:
                    if self.channel:
                        self.send_cmd(f"PRIVMSG {self.channel} :{line}")
            except Exception:
                break
        self.running = False

    def handle_user_command(self, line):
        if line.startswith("/join"):
            parts = line.split()
            if len(parts) == 2:
                self.channel = parts[1]
                self.send_cmd(f"JOIN {self.channel}")
        elif line.startswith("/quit"):
            self.send_cmd("QUIT :Bye")
            self.running = False
            self.sock.close()
        else:
            self.print_error("Unknown command")

    def print_msg(self, sender, channel, msg):
        prefix = f"[{ts()}] "
        if self.color:
            print(f"{prefix}{GREEN}<{sender}>{RESET} {msg}")
        else:
            print(f"{prefix}<{sender}> {msg}")

    def print_info(self, msg):
        prefix = f"[{ts()}] "
        if self.color:
            print(f"{prefix}{BLUE}{msg}{RESET}")
        else:
            print(f"{prefix}{msg}")

    def print_error(self, msg):
        prefix = f"[{ts()}] "
        if self.color:
            print(f"{prefix}{RED}{msg}{RESET}")
        else:
            print(f"{prefix}{msg}")

    def run(self):
        self.connect()

        if self.channel:
            self.send_cmd(f"JOIN {self.channel}")

        t_recv = threading.Thread(target=self.recv_loop, daemon=True)
        t_recv.start()

        self.input_loop()

def main():
    parser = argparse.ArgumentParser(description="Minimal IRC client (raw sockets)")
    parser.add_argument("--server", required=True, help="IRC server hostname")
    parser.add_argument("--port", type=int, default=6667, help="IRC server port")
    parser.add_argument("--nick", required=True, help="Nickname")
    parser.add_argument("--user", default="ircuser", help="Username")
    parser.add_argument("--channel", help="Channel to join")
    parser.add_argument("--no-color", action="store_true", help="Disable ANSI colors")

    args = parser.parse_args()

    client = IRCClient(
        server=args.server,
        port=args.port,
        nick=args.nick,
        username=args.user,
        channel=args.channel,
        color=not args.no_color,
    )

    try:
        client.run()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()