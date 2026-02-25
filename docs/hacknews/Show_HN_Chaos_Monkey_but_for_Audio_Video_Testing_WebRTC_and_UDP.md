URL: https://github.com/MdSadiqMd/AV-Chaos-Monkey

# AV Chaos Monkey

AV Chaos Monkey

Distributed chaos engineering platform for load testing video conferencing systems. Simulates 1500+ WebRTC participants with H.264/Opus streams and injects network chaos spikes to validate system resilience under degraded conditions

用于视频会议系统负载测试的分布式混沌工程平台。模拟1500+个WebRTC参与者，使用H.264/Opus流，并注入网络混沌尖峰以验证系统在降级条件下的韧性。

## Architecture

架构

<img width="1850" height="1776" alt="image" src="https://github.com/user-attachments/assets/7486488c-9092-4de2-a02a-f699c8d34c93" />

1. **Media Processing Pipeline**:
   - FFmpeg converts input video to H.264 Annex-B and Ogg/Opus at startup
   - NAL Reader parses H.264 stream (SPS/PPS/IDR/Slices)
   - Opus Reader extracts 20ms audio frames from Ogg container
   - Frames cached in memory, shared across all participants (zero-copy)
   - Reduces CPU by ~90% vs per-participant encoding

   **媒体处理管道：**
   - FFmpeg在启动时将输入视频转换为H.264 Annex-B和Ogg/Opus格式
   - NAL读取器解析H.264流（SPS/PPS/IDR/切片）
   - Opus读取器从Ogg容器中提取20ms音频帧
   - 帧缓存在内存中，在所有参与者之间共享（零拷贝）
   - 与每个参与者单独编码相比，CPU使用率降低约90%

2. **Control Plane**:
   - HTTP Server (:8080) manages test生命周期via REST API
   - Spike Scheduler distributes chaos events (even/random/front/back/legacy)
   - Network Degrader applies chaos: packet loss (1-25%), jitter (10-50ms), bitrate reduction (30-80%), frame drops (10-60%)
   - Loaded chaos configuration applied to participant pool

   **控制平面：**
   - HTTP服务器（:8080）通过REST API管理测试生命周期
   - 尖峰调度器分发混沌事件（均匀/随机/前加载/后加载/传统）
   - 网络降级器应用混沌：丢包（1-25%）、抖动（10-50ms）、码率降低（30-80%）、帧丢弃（10-60%）
   - 将加载的混沌配置应用到参与者池

3. **Participant Pool**:
   - Auto-partitioned across pods using: `participant_id % total_partitions = partition_id`
   - Each participant generates RTP streams (PT=96 video, PT=111 audio)
   - Participant ID embedded in RTP extension header (ID=1)
   - Pool size: 1-100 (local), 100-500 (Docker), 500-1500 (Kubernetes)

   **参与者池：**
   - 使用`participant_id % total_partitions = partition_id`自动跨Pod分区
   - 每个参与者生成RTP流（PT=96视频，PT=111音频）
   - 参与者ID嵌入RTP扩展头（ID=1）
   - 池大小：1-100（本地）、100-500（Docker）、500-1500（Kubernetes）

4. **Kubernetes Auto-Configuration**:
   - Pods auto-detect partition ID from pod name: `orchestrator-3` → `PARTITION_ID=3`
   - Port allocation: `base_port + (partition_id × 10000) + participant_index`
   - Example: Partition 0 uses 5000-14999, Partition 1 uses 15000-24999
   - StatefulSet with 10 replicas, each handling ~150 participants
   - Resources: 1-4 CPU, 2-4Gi memory per pod
   - Auto-configures based on host machine specs

   **Kubernetes自动配置：**
   - Pod从Pod名称自动检测分区ID：`orchestrator-3` → `PARTITION_ID=3`
   - 端口分配：`base_port + (partition_id × 10000) + participant_index`
   - 示例：分区0使用5000-14999，分区1使用15000-24999
   - StatefulSet包含10个副本，每个处理约150个参与者
   - 资源：每个Pod 1-4 CPU、2-4Gi内存
   - 基于主机规格自动配置

5. **UDP Relay Chain** (Kubernetes only):
   ```
   Orchestrator Pods (10×) → UDP :5000 → udp-relay Pod (Python)
   → Length-Prefixed TCP :5001 → kubectl port-forward 15001:5001
   → tools/udp-relay (Go) → UDP :5002 → Your Receiver
   ```
   - **Why**: kubectl port-forward only supports TCP, not UDP
   - **In-cluster relay**: Python script aggregates UDP from all pods, streams as TCP with 2-byte length prefix
   - **Local relay**: Go tool converts TCP stream back to UDP packets
   - Aggregates 1500 participant streams into single connection

   **UDP中继链**（仅Kubernetes）：
   ```
   编排器Pod（10个）→ UDP :5000 → udp-relay Pod（Python）
   → 带长度前缀的TCP :5001 → kubectl port-forward 15001:5001
   → tools/udp-relay（Go）→ UDP :5002 → 您的接收器
   ```
   - **原因**：kubectl port-forward仅支持TCP，不支持UDP
   - **集群内中继**：Python脚本聚合来自所有Pod的UDP，以带2字节长度前缀的TCP流形式传输
   - **本地中继**：Go工具将TCP流转换回UDP数据包
   - 将1500个参与者流聚合到单个连接中

6. **WebRTC Infrastructure**:
   - **Coturn StatefulSet**: 3 initial replicas, HPA scales 1-10 based on load (~500 participants/replica)
   - **coturn-lb Service**: Load balances TURN traffic across replicas
   - **webrtc-connector**: Optional proxy layer (Deployment + HPA 2-10 replicas), handles SDP signaling
   - **Docker Mode**: Single Coturn container for local testing
   - Ports: 3478 (TURN), 49152-65535 (relay range)
   - Credentials: webrtc/webrtc123

   **WebRTC基础设施：**
   - **Coturn StatefulSet**：3个初始副本，HPA根据负载扩展1-10个（每个副本约500个参与者）
   - **coturn-lb服务**：在副本之间负载均衡TURN流量
   - **webrtc-connector**：可选代理层（Deployment + HPA 2-10个副本），处理SDP信令
   - **Docker模式**：单个Coturn容器用于本地测试
   - 端口：3478（TURN）、49152-65535（中继范围）
   - 凭证：webrtc/webrtc123

7. **Client Integration**:
   - **UDP Receiver**: Receives aggregated RTP stream from all participants via relay chain
   - **WebRTC Receiver**: Establishes 1:1 WebRTC connections via SDP exchange through TURN servers
   - Both forward to your video call system under test (SFU/MCU/Mesh)

   **客户端集成：**
   - **UDP接收器**：通过中继链接收来自所有参与者的聚合RTP流
   - **WebRTC接收器**：通过TURN服务器的SDP交换建立1:1 WebRTC连接
   - 两者都将转发到您正在测试的视频通话系统（SFU/MCU/网状）

8. **Observability Stack** (Optional):
   - **Prometheus**: Scrapes `/metrics` endpoint from all orchestrator pods every 5s
   - **Grafana**: Visualizes metrics via pre-configured dashboard (admin/admin)
   - Metrics exposed: participant count, packets sent, bytes sent, active spikes, packet loss %, jitter, MOS score
   - Access: Prometheus on :30090, Grafana on :30030 (NodePort)
   - Orchestrator pods annotated for auto-discovery: `prometheus.io/scrape: "true"`

   **可观测性堆栈**（可选）：
   - **Prometheus**：每5秒从所有编排器Pod抓取`/metrics`端点
   - **Grafana**：通过预配置的仪表板可视化指标（admin/admin）
   - 公开的指标：参与者数量、发送的数据包、发送的字节数、活动尖峰、丢包率%、抖动、MOS分数
   - 访问：Prometheus在:30090，Grafana在:30030（NodePort）
   - 编排器Pod带有自动发现注释：`prometheus.io/scrape: "true"`

## Core Concepts

核心概念

### Participant Simulation

参与者模拟

Each virtual participant generates real media streams:
- **Video**: H.264 NAL units from actual video files, packetized per RFC 6184
- **Audio**: Opus frames from Ogg containers, packetized per RFC 7587
- **RTP**: Standards-compliant headers with participant ID extensions
- **Timing**: Frame-accurate timing (30fps video, 20ms audio packets)

每个虚拟参与者生成真实的媒体流：
- **视频**：来自实际视频文件的H.264 NAL单元，按照RFC 6184分包
- **音频**：来自Ogg容器的Opus帧，按照RFC 7587分包
- **RTP**：符合标准的头部，带有参与者ID扩展
- **时序**：帧精确时序（30fps视频，20ms音频包）

### Chaos Injection

混沌注入

Five spike types simulate real-world network conditions:
- **Packet Loss**: Drops RTP packets at application layer (1-100%)
- **Network Jitter**: Adds latency variation (base + gaussian jitter)
- **Bitrate Reduction**: Throttles video encoding (30-80% reduction)
- **Frame Drops**: Skips video frames (10-60% drop rate)
- **Bandwidth Limiting**: Caps total throughput

五种尖峰类型模拟真实世界的网络条件：
- **丢包**：在应用层丢弃RTP包（1-100%）
- **网络抖动**：增加延迟变化（基础+高斯抖动）
- **码率降低**：限制视频编码（降低30-80%）
- **帧丢弃**：跳过视频帧（丢弃率10-60%）
- **带宽限制**：限制总吞吐量

### Distribution Strategies

分发策略

Spikes are distributed across test duration using configurable strategies:
- **Even**: Uniform spacing with jitter (predictable load)
- **Random**: Unpredictable timing (realistic chaos)
- **Front-loaded**: Dense spikes early (recovery testing)
- **Back-loaded**: Baseline then chaos (comparison testing)
- **Legacy**: Fixed interval ticker (runtime injection)

尖峰使用可配置策略分布在测试持续时间内：
- **均匀**：带抖动的均匀间隔（可预测的负载）
- **随机**：不可预测的时序（真实的混沌）
- **前加载**：早期密集尖峰（恢复测试）
- **后加载**：基线后混沌（对比测试）
- **传统**：固定间隔计时器（运行时注入）

### Partitioning

分区

Kubernetes deployments use participant partitioning for horizontal scaling:
- Each pod handles `participant_id % total_partitions == partition_id`
- Port allocation: `base_port + (partition_id * 10000) + participant_index`
- Automatic load distribution across 1-10 pods
- Scales to 1500+ participants (150 per pod)

Kubernetes部署使用参与者分区进行水平扩展：
- 每个Pod处理`participant_id % total_partitions == partition_id`
- 端口分配：`base_port + (partition_id * 10000) + participant_index`
- 在1-10个Pod之间自动分配负载
- 可扩展到1500+参与者（每个Pod 150个）

## Running the System

运行系统

### 1. Local Development (Native Go)

本地开发（原生Go）

**Best for**: Development, debugging, small-scale tests (1-100 participants)

**最适合**：开发、调试、小规模测试（1-100个参与者）

```bash
# Start orchestrator
go run cmd/main.go

# In another terminal: Start UDP receiver
go run examples/go/udp_receiver.go 5002

# Edit config/config.json to set num_participants: 10
# Run chaos test
go run tools/chaos-test/main.go -config config/config.json
```

```bash
# 启动编排器
go run cmd/main.go

# 在另一个终端：启动UDP接收器
go run examples/go/udp_receiver.go 5002

# 编辑config/config.json设置num_participants: 10
# 运行混沌测试
go run tools/chaos-test/main.go -config config/config.json
```

**What happens:**
- Single orchestrator process on `:8080`
- Participants send UDP to `127.0.0.1:5002`
- Chaos spikes injected via HTTP API
- Real-time metrics displayed every 2s

**会发生什么：**
- 单个编排器进程运行在`:8080`
- 参与者发送UDP到`127.0.0.1:5002`
- 通过HTTP API注入混沌尖峰
- 每2秒显示实时指标

**Configuration** (`config/config.json`):

**配置**（`config/config.json`）：

```json
{
  "base_url": "http://localhost:8080",
  "media_path": "public/rick-roll.mp4",
  "num_participants": 10,
  "duration_seconds": 300,
  "spikes": {
    "count": 20,
    "interval_seconds": 5,
    "types": { "rtp_packet_loss": {...}, "network_jitter": {...} }
  },
  "spike_distribution": {
    "strategy": "random",
    "min_spacing_seconds": 5,
    "jitter_percent": 15
  }
}
```

---

---

### 2. Docker Compose (Containerized)

Docker Compose（容器化）

**Best for**: Isolated testing, CI/CD, medium-scale tests (100-500 participants)

**最适合**：隔离测试、CI/CD、中规模测试（100-500个参与者）

**Prerequisites:**
- Docker Desktop with 8-16GB memory allocation
- `docker-compose` installed

**先决条件：**
- 分配8-16GB内存的Docker Desktop
- 已安装`docker-compose`

```bash
# Build and start orchestrator container
./scripts/start_everything.sh build

# In another terminal: Start UDP receiver
go run examples/go/udp_receiver.go 5002

# Edit config/config.json to set num_participants: 100
# Run chaos test (targets container)
go run tools/chaos-test/main.go -config config/config.json
```

```bash
# 构建并启动编排器容器
./scripts/start_everything.sh build

# 在另一个终端：启动UDP接收器
go run examples/go/udp_receiver.go 5002

# 编辑config/config.json设置num_participants: 100
# 运行混沌测试（针对容器）
go run tools/chaos-test/main.go -config config/config.json
```

**Resource Limits** (edit `docker-compose.yaml`):

**资源限制**（编辑`docker-compose.yaml`）：

```yaml
services:
  orchestrator:
    deploy:
      resources:
        limits:
          cpus: "14.0"
          memory: 6G  # Increase for more participants
```

```yaml
services:
  orchestrator:
    deploy:
      resources:
        limits:
          cpus: "14.0"
          memory: 6G  # 增加以支持更多参与者
```

**Scaling Guide:**

**扩展指南：**

| Docker Memory | Max Participants | CPU Cores |
|--------------|------------------|-----------|
| 8 GB | ~100 | 4 |
| 16 GB | ~250 | 8 |
| 24 GB | ~400 | 12 |
| 32 GB | ~500 | 14 |

| Docker内存 | 最大参与者数 | CPU核心数 |
|--------------|------------------|-----------|
| 8 GB | ~100 | 4 |
| 16 GB | ~250 | 8 |
| 24 GB | ~400 | 12 |
| 32 GB | ~500 | 14 |

---

---

### 3. Kubernetes with Nix (Production Scale)

使用Nix的Kubernetes（生产规模）

**Best for**: Large-scale tests (500-1500 participants), horizontal scaling, production validation

**最适合**：大规模测试（500-1500个参与者）、水平扩展、生产验证

**Prerequisites:**
- Nix with flakes enabled
- Docker Desktop or kind cluster
- kubectl configured

**先决条件：**
- 启用flakes的Nix
- Docker Desktop或kind集群
- 已配置kubectl

#### Step 1: Enter Nix Environment

步骤1：进入Nix环境

```bash
# Nix provides: Go, Docker, kubectl, kind, ffmpeg
nix develop

# Or use direnv for auto-activation
echo "use flake" > .envrc
direnv allow
```

```bash
# Nix提供：Go、Docker、kubectl、kind、ffmpeg
nix develop

# 或使用direnv自动激活
echo "use flake" > .envrc
direnv allow
```

#### Step 2: Deploy to Kubernetes

步骤2：部署到Kubernetes

```bash
# Auto-deploy with optimal settings (detects system resources)
./scripts/start_everything.sh run -config config/config.json

# Or specify custom media files
./scripts/start_everything.sh run --media=path/to/video.mp4 -config config/config.json
```

```bash
# 使用最佳设置自动部署（检测系统资源）
./scripts/start_everything.sh run -config config/config.json

# 或指定自定义媒体文件
./scripts/start_everything.sh run --media=path/to/video.mp4 -config config/config.json
```

**What happens:**
1. Builds Docker image with Nix-provided Go toolchain
2. Creates/uses kind cluster
3. Deploys StatefulSet with 10 orchestrator pods
4. Deploys UDP relay pod
5. Sets up `kubectl port-forward` for UDP relay
6. Starts local TCP→UDP relay
7. Runs chaos test across all pods

**会发生什么：**
1. 使用Nix提供的Go工具链构建Docker镜像
2. 创建/使用kind集群
3. 部署带10个编排器Pod的StatefulSet
4. 部署UDP中继Pod
5. 为UDP中继设置`kubectl port-forward`
6. 启动本地TCP→UDP中继
7. 在所有Pod上运行混沌测试

#### Step 3: Receive Aggregated UDP Stream

步骤3：接收聚合的UDP流

**Option A: UDP Receiver (Recommended for Kubernetes)**

**选项A：UDP接收器（Kubernetes推荐）**

```bash
# Receives aggregated stream from all 1500 participants
go run ./examples/go/udp_receiver.go 5002
```

```bash
# 接收来自所有1500个参与者的聚合流
go run ./examples/go/udp_receiver.go 5002
```

**Option B: WebRTC Receiver (Multiple Participants)**

**选项B：WebRTC接收器（多个参与者）**

```bash
# Connect to up to 150 participants via WebRTC
go run ./examples/go/webrtc_receiver.go http://localhost:8080 <test_id> 150
```

```bash
# 通过WebRTC连接多达150个参与者
go run ./examples/go/webrtc_receiver.go http://localhost:8080 <test_id> 150
```

**Architecture Flow:**

**架构流程：**

```
1500 Participants across 10 pods
  → Each pod: 150 participants
  → Partition by participant_id % 10
  → All send UDP to udp-relay:5000
  → UDP relay aggregates → TCP :5001
  → kubectl port-forward 15001:5001
  → Local relay converts TCP → UDP :5002
  → Your receiver gets all 1500 streams
```

```
跨10个Pod的1500个参与者
  → 每个Pod：150个参与者
  → 通过participant_id % 10分区
  → 所有参与者发送UDP到udp-relay:5000
  → UDP中继聚合 → TCP :5001
  → kubectl port-forward 15001:5001
  → 本地中继将TCP转换 → UDP :5002
  → 您的接收器获取所有1500个流
```

**Note**: The `start_everything.sh` script automatically sets up:
- kubectl port-forward (udp-relay 15001:5001)
- Local TCP→UDP relay (tools/udp-relay)
- You only need to run the receiver

**注意**：`start_everything.sh`脚本自动设置：
- kubectl port-forward（udp-relay 15001:5001）
- 本地TCP→UDP中继（tools/udp-relay）
- 您只需要运行接收器

#### Manual Kubernetes Setup

手动Kubernetes设置

```bash
# Build and load image
docker build -t chaos-monkey-orchestrator:latest .
kind load docker-image chaos-monkey-orchestrator:latest

# Deploy
kubectl apply -f k8s/orchestrator/orchestrator.yaml
kubectl apply -f k8s/udp-relay/udp-relay.yaml

# Wait for pods
kubectl wait --for=condition=ready pod -l app=orchestrator --timeout=300s

# Port-forward UDP relay
kubectl port-forward udp-relay 15001:5001 &

# Start local TCP→UDP relay
go run tools/udp-relay/main.go &

# In another terminal: Start receiver
go run ./examples/go/udp_receiver.go 5002

# In another terminal: Run chaos test
go run tools/chaos-test/main.go -config config/config.json
```

```bash
# 构建并加载镜像
docker build -t chaos-monkey-orchestrator:latest .
kind load docker-image chaos-monkey-orchestrator:latest

# 部署
kubectl apply -f k8s/orchestrator/orchestrator.yaml
kubectl apply -f k8s/udp-relay/udp-relay.yaml

# 等待Pod就绪
kubectl wait --for=condition=ready pod -l app=orchestrator --timeout=300s

# 端口转发UDP中继
kubectl port-forward udp-relay 15001:5001 &

# 启动本地TCP→UDP中继
go run tools/udp-relay/main.go &

# 在另一个终端：启动接收器
go run ./examples/go/udp_receiver.go 5002

# 在另一个终端：运行混沌测试
go run tools/chaos-test/main.go -config config/config.json
```

#### Cleanup

清理

```bash
# Delete Kubernetes resources
./scripts/cleanup.sh

# Or delete entire cluster
kind delete cluster --name av-chaos-monkey
```

```bash
# 删除Kubernetes资源
./scripts/cleanup.sh

# 或删除整个集群
kind delete cluster --name av-chaos-monkey
```

---

---

### Cross-Platform Builds with Nix

使用Nix进行跨平台构建

```bash
# Build for Linux x86_64 (most common)
nix build .#packages.x86_64-linux.av-chaos-monkey

# Build for ARM64 (Raspberry Pi, AWS Graviton)
nix build .#packages.aarch64-linux.av-chaos-monkey

# Build for macOS Intel
nix build .#packages.x86_64-darwin.av-chaos-monkey

# Build for macOS Apple Silicon
nix build .#packages.aarch64-darwin.av-chaos-monkey

# Binary location
./result/bin/main
```

```bash
# 为Linux x86_64构建（最常见）
nix build .#packages.x86_64-linux.av-chaos-monkey

# 为ARM64构建（树莓派、AWS Graviton）
nix build .#packages.aarch64-linux.av-chaos-monkey

# 为macOS Intel构建
nix build .#packages.x86_64-darwin.av-chaos-monkey

# 为macOS Apple Silicon构建
nix build .#packages.aarch64-darwin.av-chaos-monkey

# 二进制文件位置
./result/bin/main
```

## API Reference

API参考

### Test Lifecycle

测试生命周期

```bash
# Create test
POST /api/v1/test/create
{
  "test_id": "optional_id",
  "num_participants": 100,
  "video": {...},
  "audio": {...},
  "duration_seconds": 600,
  "spikes": [...],
  "spike_distribution": {
    "strategy": "even",
    "min_spacing_seconds": 5,
    "jitter_percent": 15
  }
}

# Start test
POST /api/v1/test/{test_id}/start

# Get metrics
GET /api/v1/test/{test_id}/metrics

# Stop test
POST /api/v1/test/{test_id}/stop
```

```bash
# 创建测试
POST /api/v1/test/create
{
  "test_id": "optional_id",
  "num_participants": 100,
  "video": {...},
  "audio": {...},
  "duration_seconds": 600,
  "spikes": [...],
  "spike_distribution": {
    "strategy": "even",
    "min_spacing_seconds": 5,
    "jitter_percent": 15
  }
}

# 启动测试
POST /api/v1/test/{test_id}/start

# 获取指标
GET /api/v1/test/{test_id}/metrics

# 停止测试
POST /api/v1/test/{test_id}/stop
```

### WebRTC Signaling

WebRTC信令

```bash
# Get SDP offer
GET /api/v1/test/{test_id}/sdp/{participant_id}

# Set SDP answer
POST /api/v1/test/{test_id}/sdp/{participant_id}
{"sdp_answer": "v=0..."}
```

```bash
# 获取SDP offer
GET /api/v1/test/{test_id}/sdp/{participant_id}

# 设置SDP answer
POST /api/v1/test/{test_id}/sdp/{participant_id}
{"sdp_answer": "v=0..."}
```

### Chaos Injection

混沌注入

```bash
# Inject spike
POST /api/v1/test/{test_id}/spike
{
  "spike_id": "unique_id",
  "type": "rtp_packet_loss",
  "duration_seconds": 30,
  "participant_ids": [1001, 1002],
  "params": {"loss_percentage": "15"}
}
```

```bash
# 注入尖峰
POST /api/v1/test/{test_id}/spike
{
  "spike_id": "unique_id",
  "type": "rtp_packet_loss",
  "duration_seconds": 30,
  "participant_ids": [1001, 1002],
  "params": {"loss_percentage": "15"}
}
```

## Configuration

配置

### Spike Types

尖峰类型

| Type | Parameters | Effect |
|------|-----------|--------|
| `rtp_packet_loss` | `loss_percentage` (0-100) | Drops packets at RTP layer |
| `network_jitter` | `base_latency_ms`, `jitter_std_dev_ms` | Adds delay variation |
| `bitrate_reduce` | `new_bitrate_kbps` | Throttles video encoding |
| `frame_drop` | `drop_percentage` (0-100) | Skips video frames |
| `bandwidth_limit` | `bandwidth_kbps` | Caps total throughput |

| 类型 | 参数 | 效果 |
|------|-----------|--------|
| `rtp_packet_loss` | `loss_percentage` (0-100) | 在RTP层丢弃数据包 |
| `network_jitter` | `base_latency_ms`, `jitter_std_dev_ms` | 增加延迟变化 |
| `bitrate_reduce` | `new_bitrate_kbps` | 限制视频编码 |
| `frame_drop` | `drop_percentage` (0-100) | 跳过视频帧 |
| `bandwidth_limit` | `bandwidth_kbps` | 限制总吞吐量 |

### Distribution Config

分发配置

```json
{
  "spike_distribution": {
    "strategy": "even",
    "min_spacing_seconds": 5,
    "jitter_percent": 15,
    "respect_min_offset": true
  }
}
```

```json
{
  "spike_distribution": {
    "strategy": "even",
    "min_spacing_seconds": 5,
    "jitter_percent": 15,
    "respect_min_offset": true
  }
}
```

## Client Integration

客户端集成

### UDP Receiver (Go)

UDP接收器（Go）

```bash
# Provided receiver with RTP parsing
go run examples/go/udp_receiver.go 5002
```

```bash
# 提供的带有RTP解析的接收器
go run examples/go/udp_receiver.go 5002
```

**Output:**

**输出：**

```
Listening for RTP packets on UDP port 0.0.0.0:5002
Packet #100 from 127.0.0.1:xxxxx:
  Participant ID: 1001
  Payload Type: 96 (H.264 video)
  Sequence: 1234
  Timestamp: 90000
  SSRC: 1001000
  Payload Size: 1200 bytes

═══════════════════════════════════════════════════════════
                    PACKET STATISTICS                        
═══════════════════════════════════════════════════════════
Duration: 60s
Total Packets: 180000 (3000 pkt/s)
Total Bytes: 450 MB (60 Mbps)

Media Type Breakdown:
  Video (H.264): 120000 packets (66.7%)
  Audio (Opus):  60000 packets (33.3%)

Unique Streams (SSRCs): 1500
Unique Participants: 1500
```

```
在UDP端口0.0.0.0:5002上监听RTP数据包
来自127.0.0.1:xxxxx的数据包#100：
  参与者ID：1001
  负载类型：96（H.264视频）
  序列号：1234
  时间戳：90000
  SSRC：1001000
  负载大小：1200字节

═══════════════════════════════════════════════════════════
                    数据包统计                       
═══════════════════════════════════════════════════════════
持续时间：60秒
总数据包数：180000（3000包/秒）
总字节数：450 MB（60 Mbps）

媒体类型细分：
  视频（H.264）：120000包（66.7%）
  音频（Opus）：60000包（33.3%）

唯一流（SSRC）：1500
唯一参与者：1500
```

### WebRTC Receiver (Go)

WebRTC接收器（Go）

```bash
# Single participant
go run ./examples/go/webrtc_receiver.go http://localhost:8080 <test_id>

# Multiple participants (up to 150)
go run ./examples/go/webrtc_receiver.go http://localhost:8080 <test_id> 150

# Example with actual test ID
go run ./examples/go/webrtc_receiver.go http://localhost:8080 chaos_test_1770831684 150
```

```bash
# 单个参与者
go run ./examples/go/webrtc_receiver.go http://localhost:8080 <test_id>

# 多个参与者（最多150个）
go run ./examples/go/webrtc_receiver.go http://localhost:8080 <test_id> 150

# 使用实际测试ID的示例
go run ./examples/go/webrtc_receiver.go http://localhost:8080 chaos_test_1770831684 150
```

**Note**: WebRTC requires 1:1 connections. For Kubernetes, use UDP receiver which aggregates all participants automatically.

**注意**：WebRTC需要1:1连接。对于Kubernetes，使用自动聚合所有参与者的UDP接收器。

### Custom Integration

自定义集成

**RTP Packet Format:**

**RTP包格式：**

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|V=2|P|X|  CC   |M|     PT      |       sequence number         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                           timestamp                           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|           synchronization source (SSRC) identifier            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Extension ID=1 | Length=4    |    Participant ID (uint32)    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                         H.264/Opus Payload                    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|V=2|P|X|  CC   |M|     PT      |       序列号         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                           时间戳                           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|           同步源（SSRC）标识符            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  扩展ID=1 | 长度=4    |    参与者ID（uint32）    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                         H.264/Opus负载                    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

**Payload Types:**

**负载类型：**

- `96`: H.264 video (RFC 6184)
- `111`: Opus audio (RFC 7587)

- `96`：H.264视频（RFC 6184）
- `111`：Opus音频（RFC 7587）

**Participant ID Extraction:**

**参与者ID提取：**

```go
// Extension bit set?
if (packet[0] & 0x10) != 0 {
    offset := 12 + int(packet[0]&0x0F)*4  // Skip CSRC
    extID := binary.BigEndian.Uint16(packet[offset:])
    if extID == 1 {
        participantID := binary.LittleEndian.Uint32(packet[offset+4:])
    }
}
```

```go
// 扩展位是否设置？
if (packet[0] & 0x10) != 0 {
    offset := 12 + int(packet[0]&0x0F)*4  // 跳过CSRC
    extID := binary.BigEndian.Uint16(packet[offset:])
    if extID == 1 {
        participantID := binary.LittleEndian.Uint32(packet[offset+4:])
    }
}
```

## Performance

性能

### Resource Requirements

资源需求

| Participants | Memory | CPU | Bandwidth |
|-------------|--------|-----|-----------|
| 100 | 2GB | 2 cores | 250 Mbps |
| 500 | 6GB | 8 cores | 1.2 Gbps |
| 1000 | 12GB | 16 cores | 2.5 Gbps |
| 1500 | 18GB | 24 cores | 3.7 Gbps |

| 参与者数 | 内存 | CPU | 带宽 |
|-------------|--------|-----|-----------|
| 100 | 2GB | 2核 | 250 Mbps |
| 500 | 6GB | 8核 | 1.2 Gbps |
| 1000 | 12GB | 16核 | 2.5 Gbps |
| 1500 | 18GB | 24核 | 3.7 Gbps |

### Kubernetes Scaling

Kubernetes扩展

- **Auto-scaling**: Calculates optimal pod count based on participant count
- **Pod capacity**: 150 participants per pod (configurable)
- **Max pods**: 10 (StatefulSet limit)
- **Port range**: 10,000 ports per partition

- **自动扩展**：根据参与者数量计算最佳Pod数量
- **Pod容量**：每个Pod 150个参与者（可配置）
- **最大Pod数**：10（StatefulSet限制）
- **端口范围**：每个分区10,000个端口

### Throughput

吞吐量

Per participant (1280x720@30fps + Opus):
- Video: ~2.5 Mbps (H.264)
- Audio: ~128 Kbps (Opus)
- Total: ~2.6 Mbps
- Packets: ~90 video + 50 audio = 140 pkt/s

每个参与者（1280x720@30fps + Opus）：
- 视频：~2.5 Mbps（H.264）
- 音频：~128 Kbps（Opus）
- 总计：~2.6 Mbps
- 数据包：~90视频 + 50音频 = 140包/秒

## Monitoring

监控

### Prometheus Metrics

Prometheus指标

```bash
# Exposed on /metrics endpoint
av_chaos_monkey_participants_total
av_chaos_monkey_packets_sent_total
av_chaos_monkey_bytes_sent_total
av_chaos_monkey_spikes_active
av_chaos_monkey_packet_loss_percent
av_chaos_monkey_jitter_ms
```

```bash
# 在/metrics端点公开
av_chaos_monkey_participants_total
av_chaos_monkey_packets_sent_total
av_chaos_monkey_bytes_sent_total
av_chaos_monkey_spikes_active
av_chaos_monkey_packet_loss_percent
av_chaos_monkey_jitter_ms
```

### Grafana Dashboard

Grafana仪表板

```bash
# Docker Mode: Start monitoring stack
docker-compose --profile monitoring up

# Kubernetes Mode: Deploy monitoring
kubectl apply -f k8s/monitoring/prometheus-rbac.yaml
kubectl apply -f k8s/monitoring/prometheus.yaml
kubectl apply -f k8s/monitoring/grafana.yaml

# Access Grafana
# Docker: http://localhost:3000
# Kubernetes: http://localhost:30030 (NodePort)
# Default credentials: admin/admin

# Access Prometheus
# Docker: http://localhost:9091
# Kubernetes: http://localhost:30090 (NodePort)
```

```bash
# Docker模式：启动监控堆栈
docker-compose --profile monitoring up

# Kubernetes模式：部署监控
kubectl apply -f k8s/monitoring/prometheus-rbac.yaml
kubectl apply -f k8s/monitoring/prometheus.yaml
kubectl apply -f k8s/monitoring/grafana.yaml

# 访问Grafana
# Docker：http://localhost:3000
# Kubernetes：http://localhost:30030（NodePort）
# 默认凭证：admin/admin

# 访问Prometheus
# Docker：http://localhost:9091
# Kubernetes：http://localhost:30090（NodePort）
```

**Kubernetes Auto-Discovery:**

**Kubernetes自动发现：**

- Orchestrator pods annotated with `prometheus.io/scrape: "true"`
- Prometheus scrapes `/metrics` from all pods every 5s
- Grafana pre-configured with Prometheus datasource
- Dashboard auto-provisioned on startup

- 编排器Pod带有`prometheus.io/scrape: "true"`注释
- Prometheus每5秒从所有Pod抓取`/metrics`
- Grafana预配置了Prometheus数据源
- 仪表板在启动时自动配置

### Real-time Stats

实时统计

```bash
# Get test metrics
curl http://localhost:8080/api/v1/test/{test_id}/metrics | jq

# Output
{
  "aggregate": {
    "total_frames_sent": 45000,
    "total_packets_sent": 180000,
    "total_bitrate_kbps": 250000,
    "avg_jitter_ms": 12.5,
    "avg_packet_loss": 2.3,
    "avg_mos_score": 4.1
  }
}
```

```bash
# 获取测试指标
curl http://localhost:8080/api/v1/test/{test_id}/metrics | jq

# 输出
{
  "aggregate": {
    "total_frames_sent": 45000,
    "total_packets_sent": 180000,
    "total_bitrate_kbps": 250000,
    "avg_jitter_ms": 12.5,
    "avg_packet_loss": 2.3,
    "avg_mos_score": 4.1
  }
}
```

## Troubleshooting

故障排除

### No UDP Packets Received

未接收到UDP数据包

```bash
# Check UDP target configuration
kubectl logs orchestrator-0 | grep "UDP transmission enabled"

# Verify UDP relay is running
kubectl get pod udp-relay

# Check port-forward
ps aux | grep "kubectl port-forward"

# Test UDP connectivity
nc -u -z localhost 5002
```

```bash
# 检查UDP目标配置
kubectl logs orchestrator-0 | grep "UDP transmission enabled"

# 验证UDP中继是否正在运行
kubectl get pod udp-relay

# 检查端口转发
ps aux | grep "kubectl port-forward"

# 测试UDP连接
nc -u -z localhost 5002
```

### WebRTC Connection Fails

WebRTC连接失败

```bash
# Check TURN server
kubectl get svc coturn-lb

# Verify ICE candidates
kubectl logs orchestrator-0 | grep "ICE"

# Test TURN connectivity
turnutils_uclient -v -u webrtc -w webrtc123 <turn-server>:3478
```

```bash
# 检查TURN服务器
kubectl get svc coturn-lb

# 验证ICE候选
kubectl logs orchestrator-0 | grep "ICE"

# 测试TURN连接
turnutils_uclient -v -u webrtc -w webrtc123 <turn-server>:3478
```

### High Memory Usage

高内存使用

```bash
# Check participant count per pod
kubectl exec orchestrator-0 -- curl -s http://localhost:8080/api/v1/test/{test_id}/metrics | jq '.participants | length'

# Scale down participants or increase pod count
go run tools/k8s-start/main.go -replicas 10 -participants 1000

# Increase Docker memory (Docker Desktop)
# Settings → Resources → Memory → 16GB
```

```bash
# 检查每个Pod的参与者数量
kubectl exec orchestrator-0 -- curl -s http://localhost:8080/api/v1/test/{test_id}/metrics | jq '.participants | length'

# 减少参与者数量或增加Pod数量
go run tools/k8s-start/main.go -replicas 10 -participants 1000

# 增加Docker内存（Docker Desktop）
# 设置 → 资源 → 内存 → 16GB
```

### Packet Loss in UDP Receiver

UDP接收器中的丢包

Single UDP socket cannot handle 3000+ concurrent streams without kernel buffer overflow. Solutions:
- Use UDP relay (aggregates before forwarding)
- Increase socket buffer: `setsockopt(SO_RCVBUF, 8MB)`
- Accept baseline loss as measurement artifact

单个UDP套接字无法在不发生内核缓冲区溢出的情况下处理3000+并发流。解决方案：
- 使用UDP中继（在转发前聚合）
- 增加套接字缓冲区：`setsockopt(SO_RCVBUF, 8MB)`
- 将基线丢包作为测量伪影接受

## License

许可证

BSD 3-Clause License

BSD 3条款许可证

## Contributing

贡献

Contributions welcome! Key areas:
- Additional spike types (CPU throttling, memory pressure)
- More distribution strategies (wave, burst)
- Enhanced metrics (MOS calculation, RTCP feedback)
- Client libraries (Python, Rust, TypeScript)

欢迎贡献！重点领域：
- 额外的尖峰类型（CPU限制、内存压力）
- 更多分发策略（波浪、突发）
- 增强的指标（MOS计算、RTCP反馈）
- 客户端库（Python、Rust、TypeScript）

## References

参考

- [RFC 3550](https://tools.ietf.org/html/rfc3550) - RTP: A Transport Protocol for Real-Time Applications
- [RFC 6184](https://tools.ietf.org/html/rfc6184) - RTP Payload Format for H.264 Video
- [RFC 7587](https://tools.ietf.org/html/rfc7587) - RTP Payload Format for Opus
- [WebRTC Specification](https://www.w3.org/TR/webrtc/)

- [RFC 3550](https://tools.ietf.org/html/rfc3550) - RTP：实时应用的传输协议
- [RFC 6184](https://tools.ietf.org/html/rfc6184) - H.264视频的RTP负载格式
- [RFC 7587](https://tools.ietf.org/html/rfc7587) - Opus的RTP负载格式
- [WebRTC规范](https://www.w3.org/TR/webrtc/)

---

## 批判性思考评论

### 1. 技术创新点

AV Chaos Monkey是一个非常有价值的开源项目，它填补了视频会议领域混沌工程测试的空白。传统的Chaos Monkey主要用于HTTP服务，而该项目专门针对WebRTC和音视频流的特性进行了深度定制。其技术创新点包括：

- **零拷贝媒体处理**：通过FFmpeg预转码并在内存中缓存帧数据，实现90%的CPU节省，这是大规模模拟的关键优化
- **智能分区策略**：使用取模运算实现参与者的自动分区，支持水平扩展到1500+参与者
- **UDP中继链设计**：巧妙解决了kubectl port-forward不支持UDP的问题，体现了对Kubernetes网络限制的深刻理解

### 2. 架构设计的权衡

该项目在架构上做出了一些值得思考的权衡：

**优势：**
- 分层架构清晰，控制平面、媒体处理、参与者池职责分离
- 支持多种部署模式（本地、Docker、Kubernetes），适应不同测试场景
- 完整的可观测性支持（Prometheus + Grafana）

**潜在改进空间：**
- UDP中继链增加了复杂性，引入了额外的延迟和故障点
- 1500参与者的上限可能无法满足超大规模测试需求（如万人会议场景）
- 缺少对SIMULCAST（联播）和SVC（可伸缩视频编码）的支持

### 3. 实际应用价值

对于视频会议系统的开发者而言，这个工具的价值在于：

1. **真实的压力测试**：相比传统的虚拟参与者，该项目模拟的是真实的RTP/Opus流，更接近生产环境
2. **可控的混沌注入**：可以精确控制丢包率、抖动等参数，便于定位系统的临界点
3. **成本效益**：用软件模拟替代真人测试，大幅降低测试成本

### 4. 局限性与建议

- **单一媒体源**：所有参与者使用相同的视频文件，可能无法测试编码器对不同内容的适应性
- **缺乏交互性**：模拟的参与者是单向推流，无法测试双向通信场景
- **WebRTC复杂度**：项目中提到的WebRTC连接器标注为"optional proxy layer"，暗示WebRTC支持可能不如UDP成熟

总体而言，AV Chaos Monkey是一个专业且实用的工具，适合用于SFU/MCU服务器的容量规划和稳定性验证。对于需要构建高可用视频会议系统的团队来说，这是一个值得研究和使用的开源项目。
