# Instruction

## Action
```bash
docker run --name agent --network grafanet -e AGENT_MODE=flow -v $(pwd)/config.river:/etc/agent/config.river -p 9999:9999 -p 12345:12345 grafana/agent run --server.http.listen-addr=0.0.0.0:12345 /etc/agent/config.river
```
**Or temporary configuration**
```bash
docker run --name agent --rm --network grafanet -e AGENT_MODE=flow -v $(pwd)/config.river:/etc/agent/config.river -p 4318:4318 -p 12345:12345 grafana/agent run --server.http.listen-addr=0.0.0.0:12345 /etc/agent/config.river
```
