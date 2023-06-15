# Instruction

## Note
This step work on version below:
- `Docker Compose`: v2.17.3
- `Docker`: 23.0.5
- `containerd`: 1.6.20
- `runc`: 1.1.5
- `docker-init`: 0.19.0

## Step by Step
1. Running application and push log to `/tmp/log`
example

```zsh
go build -o app && ./app > /tmp/log/app.log
```

2. run docker compose
```
docker compose up -d
```

3. If you want to clean it run this command
```
docker compose down
```