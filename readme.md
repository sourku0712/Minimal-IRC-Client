# 🧠 Minimal IRC Client (Python, Raw Sockets)

A **terminal-based IRC (Internet Relay Chat) client** written in **pure Python** using **raw TCP sockets** only.  
This project demonstrates how real-world text-based network protocols work without relying on external IRC libraries.

---

## ✨ Features

- 🔌 Connects to real IRC servers (e.g., Libera.Chat)
- 🧵 Uses **raw TCP sockets** (no IRC libraries)
- 👤 NICK / USER handshake
- 💬 Join channels and send/receive messages
- 🔄 Automatic **PING → PONG** handling (keep-alive)
- ⌨️ Interactive terminal input
- 🎨 Optional ANSI-colored output
- 🕒 Message timestamps
- ❌ Clean quit handling

---

## 📁 Project Structure

```
.
├── irc_client.py   # Main IRC client implementation
├── README.md       # Project documentation
```

---

## 🚀 Getting Started

### 1️⃣ Requirements

- Python **3.7+**
- Internet connection
- Linux / macOS / Windows (WSL recommended on Windows)

No third-party libraries required.

---

### 2️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/minimal-irc-client.git
cd minimal-irc-client
```

---

### 3️⃣ Run the Client

```bash
python irc_client.py --server irc.libera.chat --nick mynick123
```

Join a channel **after connecting**:

```text
/join #testchannel
```

⚠️ **Note:** Channel names must be quoted if passed as CLI arguments:

```bash
--channel "#testchannel"
```

---

## 🧑‍💻 Usage (Inside the Program)

| Action | Command |
|------|--------|
| Send message | `Hello everyone` |
| Join channel | `/join #channel` |
| Quit client | `/quit` |

---

## 🔁 How PING–PONG Works

IRC servers periodically send `PING` messages to verify client connectivity.

This client:

- Listens for `PING`
- Automatically responds with `PONG`
- Prevents server timeout disconnections

No user action is required.

---

## 🧠 How It Works (Internals)

- **Main thread** → reads user input
- **Receiver thread** → listens to server messages
- **Socket-based protocol parsing**
- Messages are processed line-by-line (`\r\n` delimited)

---

## 🧪 Example Session

```text
$ python irc_client.py --server irc.libera.chat --nick student123

/join #testchannel
Hello everyone!

[12:01:10] <alice> hi!
/quit
```

---

## 📚 Educational Use Cases

- Computer Networks Lab
- TCP/IP socket programming practice
- Text-based protocol parsing
- Client–server architecture demonstration

---

## 🔧 Possible Extensions

- `/msg <user> <message>` (private messaging)
- `/names` (list users in channel)
- `/nick` (change nickname)
- SSL/TLS support (port 6697)
- Async / non-blocking sockets

---

## ⚠️ Limitations

- Single server connection
- Basic command support
- No reconnection logic
- No authentication (NickServ)

---