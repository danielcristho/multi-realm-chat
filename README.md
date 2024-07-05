# Multi Realm Chat

## Start Project

### Setup Environmnet

Linux

```bash
git clone https://github.com/danielcristho/multi-realm-chat.git && cd multi-realm-chat
python3 -m venv .venv
source env/bin/activate
```

Windows

```bash
git clone https://github.com/danielcristho/multi-realm-chat.git && cd multi-realm-chat
python -m .venv
.venv\Scripts\activate
```

Install requirements

```bash
pip install -r requirements.txt
```

## Run UI

### Run using browser

```bash
flet run --web ui
```

Jika di direktori `ui`

```bash
flet run --web .
```

### Run as mobile (optional)

Install MPV

Linux

```bash
sudo apt install libmpv-dev mpv
```

Windows

Install from the official website [MPV](https://mpv.io)

```bash
cd ui
```

```bash
flet run
```

Tampilan

![Start](ui/assets/start.png)

### Todo List

- [x] Setup project

- [x] Integrasi frontend dan backend

- [x] Login & Register

- [X] Private chat

- [X] Group chat

- [X] Send files

- [X] Chat antar realm (private & group)