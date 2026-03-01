---
title: "Let's discuss sandbox isolation"
url: "https://www.shayon.dev/post/2026/52/lets-discuss-sandbox-isolation/"
rating: 9
category: "Security / Infrastructure"
date: "2026-02-28"
---

# Let's discuss sandbox isolation

There is a lot of energy right now around sandboxing untrusted code. AI agents generating and executing code, multi-tenant platforms running customer scripts, RL training pipelines evaluating model outputs—basically, you have code you did not write, and you need to run it without letting it compromise the host, other tenants, or itself in unexpected ways.

The word "isolation" gets used loosely. A Docker container is "isolated." A microVM is "isolated." A WebAssembly module is "isolated." But these are fundamentally different things, with different boundaries, different attack surfaces, and different failure modes. I wanted to write down my learnings on what each layer actually provides, because I think the distinctions matter and allow you to make informed decisions for the problems you are looking to solve.

## The kernel is the shared surface

When any code runs on Linux, it interacts with the hardware through the kernel via system calls. The Linux kernel exposes roughly 340 syscalls, and the kernel implementation is tens of millions of lines of C code. Every syscall is an entry point into that codebase.

```
Untrusted Code ─( Syscall )─→ Host Kernel ─( Hardware API )─→ Hardware
                              [ 40M LOC C ]
```

Every isolation technique is answering the same question of how to reduce or eliminate the untrusted code's access to that massive attack surface.

A useful mental model here is shared state versus dedicated state. Because standard containers share the host kernel, they also share its internal data structures like the TCP/IP stack, the Virtual File System caches, and the memory allocators. A vulnerability in parsing a malformed TCP packet in the kernel affects every container on that host. Stronger isolation models push this complex state up into the sandbox, exposing only simple, low-level interfaces to the host, like raw block I/O or a handful of syscalls.

The approaches differ in where they draw the boundary. Namespaces use the same kernel but restrict visibility. Seccomp uses the same kernel but restricts the allowed syscall set. Projects like gVisor use a completely separate user-space kernel and make minimal host syscalls. MicroVMs provide a dedicated guest kernel and a hardware-enforced boundary. Finally, WebAssembly provides no kernel access at all, relying instead on explicit capability imports. Each step is a qualitatively different boundary, not just a stronger version of the same thing.

## Namespaces as visibility walls

Linux namespaces wrap global system resources so that processes appear to have their own isolated instance. There are eight types, and each isolates a specific resource.

| Namespace | What it isolates | What the process sees |
|-----------|-----------------|----------------------|
| PID | Process IDs | Own process tree, starts at PID 1 |
| Mount | Filesystem mount points | Own mount table, can have different root |
| Network | Network interfaces, routing | Own interfaces, IP addresses, ports |
| User | UID/GID mapping | Can be root inside, nobody outside |
| UTS | Hostname | Own hostname |
| IPC | SysV IPC, POSIX message queues | Own shared memory, semaphores |
| Cgroup | Cgroup root directory | Own cgroup hierarchy |
| Time | System clocks (monotonic, boot) | Own system uptime and clock offsets |

Namespaces are what Docker containers use. When you run a container, it gets its own PID namespace (cannot see host processes), its own mount namespace (own filesystem view), its own network namespace (own interfaces), and so on.

The critical thing to understand is **namespaces are visibility walls, not security boundaries**. They prevent a process from *seeing* things outside its namespace. They do not prevent a process from *exploiting the kernel* that implements the namespace. The process still makes syscalls to the same host kernel. If there is a bug in the kernel's handling of any syscall, the namespace boundary does not help.

In January 2024, [CVE-2024-21626](https://seclists.org/oss-sec/2024/q1/78) showed that a file descriptor leak in `runc` (the standard container runtime) allowed containers to access the host filesystem. The container's mount namespace was intact — the escape happened through a leaked fd that `runc` failed to close before handing control to the container. In 2025, three more `runc` CVEs (CVE-2025-31133, CVE-2025-52565, CVE-2025-52881) demonstrated mount race conditions that allowed writing to protected host paths from inside containers.

## Cgroups: accounting is not security

Cgroups (control groups) limit and account for resource usage: CPU, memory, disk I/O, number of processes. They prevent a container from consuming all available memory or spinning up thousands of processes.

Cgroups are important for stability, but they are not a security boundary. They prevent denial-of-service, not escape. A process constrained by cgroups still makes syscalls to the same kernel with the same attack surface.

## Seccomp-BPF as a filter

Seccomp-BPF lets you attach a Berkeley Packet Filter program that decides which syscalls a process is allowed to make. You can deny dangerous syscalls like process tracing, filesystem manipulation, kernel extension loading, and performance monitoring.

Docker applies a default seccomp profile that blocks around 40 to 50 syscalls. This meaningfully reduces the attack surface. But the key limitation is that seccomp is a filter on the same kernel. The syscalls you allow still enter the host kernel's code paths. If there is a vulnerability in the write implementation, or in the network stack, or in any allowed syscall path, seccomp does not help.

```
Without Seccomp:
  Untrusted Code ─( ~340 syscalls )─→ Host Kernel

With Seccomp:
  Untrusted Code ─( ~300 syscalls )─→ Host Kernel
```

The attack surface is smaller. The boundary is the same.

### Running a container in privileged mode

This is worth calling out because it comes up surprisingly often. Some isolation approaches require Docker's privileged flag. For example, building a custom sandbox that uses nested PID namespaces inside a container often leads developers to use privileged mode, because mounting a new `/proc` filesystem for the nested sandbox requires the `CAP_SYS_ADMIN` capability (unless you also use user namespaces).

If you enable `--privileged` just to get `CAP_SYS_ADMIN` for nested process isolation, you have added one layer (nested process visibility) while removing several others (seccomp, all capability restrictions, device isolation). The net effect is arguably weaker isolation than a standard unprivileged container. This is a real trade-off that shows up in production. The ideal solutions are either to grant only the specific capability needed instead of all of them, or to use a different isolation approach entirely that does not require host-level privileges.

## gVisor and user-space kernels

gVisor is where the isolation model changes qualitatively. To understand the difference, it helps to look at the attack surface of a standard container.

```
Standard Container (Docker)
┌───────────────────────┐
│ Untrusted Code        │
└──────────┬────────────┘
           │ ~340 syscalls
           ▼
   [ Seccomp Filter ]
           │ ~300 allowed syscalls
           ▼
┌───────────────────────┐
│ Host Kernel (Ring 0)  │ ◄── FULL ATTACK SURFACE
└───────────────────────┘
```

The code runs as a standard Linux process. Seccomp acts as a strict allowlist filter, reducing the set of permitted system calls. However, any allowed syscall still executes directly against the shared host kernel. Once a syscall is permitted, the kernel code processing that request is the exact same code used by the host and every other container. The failure mode here is that a vulnerability in an allowed syscall lets the code compromise the host kernel, bypassing the namespace boundaries.

Instead of filtering syscalls to the host kernel, gVisor interposes a completely separate kernel implementation called the Sentry between the untrusted code and the host. The Sentry does not access the host filesystem directly; instead, a separate process called the Gofer handles file operations on the Sentry's behalf, communicating over a restricted protocol. This means even the Sentry's own file access is mediated.

```
gVisor
┌───────────────────────┐
│ Untrusted Code        │
└──────────┬────────────┘
           │ ~340 syscalls
           ▼
┌───────────────────────┐
│ gVisor Sentry (Ring 3)│ ◄── USER-SPACE KERNEL
└──────┬────────┬───────┘
       │        │ 9P / LISAFS
       │        ▼
       │  ┌───────────┐
       │  │   Gofer   │ ◄── FILE I/O PROXY
       │  └─────┬─────┘
       │        │
       ▼        ▼
┌───────────────────────┐
│ Host Kernel (Ring 0)  │ ◄── REDUCED ATTACK SURFACE
└───────────────────────┘
  (~70 host syscalls from Sentry)
```

The Sentry intercepts the untrusted code's syscalls and handles them in user-space. It reimplements around 200 Linux syscalls in Go, which is enough to run most applications. When the Sentry actually needs to interact with the host to read a file, it makes its own highly restricted set of roughly 70 host syscalls. This is not just a smaller filter on the same surface; it is a completely different surface. The failure mode changes significantly. An attacker must first find a bug in gVisor's Go implementation of a syscall to compromise the Sentry process, and then find a way to escape from the Sentry to the host using only those limited host syscalls.

The Sentry intercepts syscalls using one of several mechanisms, such as seccomp traps or KVM, with the default since 2023 being the seccomp-trap approach known as systrap.

What this means in practice is that if someone discovers a bug in the Linux kernel's I/O implementation, containers using Docker are directly exposed. A gVisor sandbox is not, because those syscalls are handled by the Sentry, and the Sentry does not expose them to the host kernel.

The trade-off is performance. Every syscall goes through user-space interception, which adds overhead. I/O-heavy workloads feel this the most. For short-lived code execution like scripts and tests, it is usually fine, but for sustained high-throughput I/O, it can matter.

Also, by adopting gVisor, you are betting that it's easier to audit and maintain a smaller footprint of code (the Sentry and its limited host interactions) than to secure the entire massive Linux kernel surface against untrusted execution. That bet is not free of risk, gVisor itself has had security vulnerabilities in the Sentry but the surface area you need to worry about is drastically smaller and written in a memory-safe language.

## Defense in depth on top of gVisor

gVisor gives you the user-space kernel boundary. What it does not give you automatically is multi-job isolation within a single gVisor sandbox. If you are running multiple untrusted executions inside one `runsc` container, you still need to layer additional controls. Here is one pattern for doing that:

- **Per-job PID + mount + IPC namespaces** via `clone3` — so each execution is isolated from other executions inside the same gVisor sandbox
- **Seccomp-BPF inside the namespace** — blocking syscalls like `clone3` (preventing nested namespace escape), `io_uring` (force fallback to `epoll`), `ptrace`, kernel module loading
- **Privilege drop** — run as `nobody` (UID 65534) with `PR_SET_NO_NEW_PRIVS`
- **Ephemeral tmpfs** for all writable paths — cleanup is a single `umount2` syscall, not a recursive directory walk
- **Read-only root filesystem** — the container itself is immutable
- **Capability-based file APIs** — use `openat2` or similar to confine file writes to the work directory, preventing path traversal via `../../etc/passwd`
- **Network egress control** — compute isolation means nothing if the sandbox can freely phone home. Options range from disabling networking entirely, to running an allowlist proxy (like Squid) that blocks DNS resolution inside the sandbox and forces all traffic through a domain-level allowlist, to dropping `CAP_NET_RAW` so the sandbox cannot bypass DNS with raw sockets.

```
gVisor Container (runsc)
 └─ Per-job PID + Mount Namespace
     └─ Seccomp BPF Filter
         └─ Privilege Drop
             └─ Network Egress Control
                 └─ Ephemeral tmpfs
                     └─ Capability-confined File Writes
```

Each layer catches different attack classes. A namespace escape inside gVisor reaches the Sentry, not the host kernel. A seccomp bypass hits the Sentry's syscall implementation, which is itself sandboxed. Privilege escalation is blocked by dropping privileges. Persistent state leakage between jobs is prevented by ephemeral tmpfs with atomic unmount cleanup.

### A note on forking

A practical detail that matters is the process that creates child sandboxes must itself be fork-safe. If you are running an async runtime, forking from a multithreaded process is inherently unsafe because child processes inherit locked mutexes and can corrupt state. The solution is a fork server pattern where you fork a single-threaded launcher process before starting the async runtime, then have the async runtime communicate with the launcher over a Unix socket. The launcher creates children, entirely avoiding the multithreaded fork problem.

```
Startup
  fork() → Launcher (Single-threaded, Poll Loop)
               │
               ├─ clone3(NEWPID | NEWNS | NEWIPC)
               │
               └─ Child (Mount, Privdrop, Seccomp, Execve)

Main Server (Async Runtime)
  │
  └─ AF_UNIX SEQPACKET ─→ Launcher
```

## MicroVMs for hardware boundaries

MicroVMs use hardware virtualization backed by the CPU's extensions to run each workload in its own virtual machine with its own kernel.

```
MicroVM Architecture
┌───────────────────────┐
│ Untrusted Code        │
└──────────┬────────────┘
           │ Syscalls
           ▼
┌───────────────────────┐
│ Guest Kernel (Ring 0) │ ◄── DEDICATED KERNEL
└──────────┬────────────┘
           │ VirtIO / MMIO
           ▼
┌───────────────────────┐
│ KVM Hypervisor (Host) │ ◄── HARDWARE BOUNDARY
└──────────┬────────────┘
           │ Secure API
           ▼
┌───────────────────────┐
│ VMM (User-Space)      │ ◄── DEVICE EMULATION
└───────────────────────┘
```

Code runs in a completely separate, hardware-backed environment with its own guest kernel. It is important to separate the concepts here. The hypervisor is the capability built into the Linux kernel that manages the CPU's hardware virtualization extensions. The Virtual Machine Monitor is a user-space process that configures the VM, allocates memory, and emulates minimal hardware devices. The microVM itself is a VM that has been stripped of legacy PC cruft so it boots in milliseconds and uses minimal memory.

Escaping the guest kernel requires finding a vulnerability in the Virtual Machine Monitor's device emulation or the CPU's virtualization features, which are rare and highly prized.

The guest runs in a separate virtual address space enforced by the CPU hardware. A bug in the guest kernel cannot access host memory because the hardware prevents it. The host kernel only sees the user-space process. The attack surface is the hypervisor and the Virtual Machine Monitor, both of which are orders of magnitude smaller than the full kernel surface that containers share.

You generally see two different approaches to Virtual Machine Monitor design depending on the workload. The first is strict minimalism, seen in projects like Firecracker. Built specifically for running thousands of tiny, short-lived functions on a single server, it intentionally leaves out complex features like hot-plugging CPUs or passing through physical GPUs. The goal is simply the smallest possible attack surface and memory footprint.

The second approach offers broader feature support, seen in projects like Cloud Hypervisor or QEMU microvm. Built for heavier and more dynamic workloads, it supports hot-plugging memory and CPUs, which is useful for dynamic build runners that need to scale up during compilation. It also supports GPU passthrough, which is essential for AI workloads, while still maintaining the fast boot times of a microVM.

### Trade-off

The trade-off versus gVisor is that microVMs have higher per-instance overhead but stronger, hardware-enforced isolation. For CI systems and sandbox platforms where you create thousands of short-lived environments, the boot time and memory overhead add up. For long-lived, high-security workloads, the hardware boundary is worth it.

Snapshotting is a feature worth noting. You can capture a running VM's state including CPU registers, memory, and devices, and restore it later. This enables warm pools where you boot a VM once, install dependencies, snapshot it, and restore clones in milliseconds instead of booting fresh each time. This is how some platforms achieve incredibly fast cold starts even with full VM isolation.

## WebAssembly with no kernel at all

WebAssembly takes a fundamentally different approach. Instead of running native code and filtering its kernel access, WASM runs code in a memory-safe virtual machine that has no syscall interface at all. All interaction with the host happens through explicitly imported host functions.

```
WebAssembly (WASM)
┌───────────────────────┐
│ Untrusted Code        │
└──────────┬────────────┘
           │ Function Calls
           ▼
┌───────────────────────┐
│ WASM Runtime (Host)   │ ◄── MEMORY-SAFE VM
└──────────┬────────────┘
           │ Imported Host Functions
           ▼
┌───────────────────────┐
│ Allowed Host APIs     │ ◄── EXPLICIT CAPABILITIES
└───────────────────────┘
```

Code runs in a strict sandbox where the only allowed operations are calling functions provided by the host. If the host doesn't provide a file reading function, the WASM module simply cannot read files. The failure mode here requires a vulnerability in the WASM runtime itself, like an out-of-bounds memory read that bypasses the linear memory checks.

There is no syscall surface to attack because the code never makes syscalls. Memory safety is enforced by the runtime. The linear memory is bounds-checked, the call stack is inaccessible, and control flow is type-checked. Modern runtimes add guard pages and memory zeroing between instances.

The performance characteristics are attractive with incredibly fast cold starts and minimal memory overhead. But the practical limitation is language support. You cannot run arbitrary Python scripts in WASM today without compiling the Python interpreter itself to WASM along with all its C extensions. For sandboxing arbitrary code in arbitrary languages, WASM is not yet viable. For sandboxing code you control the toolchain for, it is excellent. I am, however, quite curious if there is a future for WASM in general-purpose sandboxing. Browsers have spent decades solving a similar problem of executing untrusted code safely, and porting those architectural learnings to backend infrastructure feels like a natural evolution.

**Update (Feb 27, 2026):** [Simon Willison pointed out](https://news.ycombinator.com/item?id=47185105) that WASM support for interpreted languages is further along than I what I thought. `wasm32-unknown-wasip1` is a [Tier 2 supported target for CPython](https://peps.python.org/pep-0011/#tier-2) (meaning failures block releases), with [unofficial WASI builds](https://github.com/brettcannon/cpython-wasi-build/releases) available. [Pyodide](https://pyodide.org/) ports CPython to WASM via Emscripten with support for packages like NumPy, pandas, and SciPy. On the JavaScript side, [QuickJS compiled to WASM](https://tools.simonwillison.net/quickjs) works well for sandboxed JS execution. [Wasmer](https://wasmer.io/posts/python-on-the-edge-powered-by-webassembly) can run Python server-side on WASM including native modules like gevent and SQLAlchemy. I haven't tried these yet, but I am looking forward to.

## The spectrum

Putting it all together, the landscape spans from fast and weak isolation to slower and highly secure isolation.

```
                     Isolation strength →
                     Attack surface     ↓

Namespaces      Seccomp       gVisor         MicroVM         WASM
   │               │             │              │              │
   │  visibility   │  syscall    │  separate    │  hardware    │  no kernel
   │  walls only   │  filter on  │  kernel in   │  boundary    │  access at
   │               │  same       │  user-space  │  via KVM     │  all
   │               │  kernel     │              │              │
   ▼               ▼             ▼              ▼              ▼
  Fast            Fast         Moderate       Slower        Fastest
  Weakest         Weak         Strong         Strongest     Strong*
                                                           (*limited scope)
```

For running trusted code that you wrote and reviewed, Docker with a seccomp profile is probably fine. The isolation is against accidental interference, not adversarial escape.

For running untrusted code in a multi-tenant environment, like short-lived scripts, AI-generated code, or customer-provided functions, you need a real boundary. gVisor gives you a user-space kernel boundary with good compatibility, while a microVM gives you a hardware boundary with the strongest guarantees. Either is defensible depending on your threat model and performance requirements.

For reinforcement learning training pipelines where AI-generated code is evaluated in sandboxes across potentially untrusted workers, the threat model is both the code and the worker. You need isolation in both directions, which pushes toward microVMs or gVisor with defense-in-depth layering.

What I've learned is that the common mistake is treating isolation as binary. It's easy to assume that if you use Docker, you are isolated. The reality is that standard Docker gives you namespace isolation, which is just visibility walls on a shared kernel. Whether that is sufficient depends entirely on what you are protecting against.

It is also worth remembering that compute isolation is only half the problem. You can put code inside a gVisor sandbox or a Firecracker microVM with a hardware boundary, and none of it matters if the sandbox has unrestricted network egress for your "agentic workload". An attacker who cannot escape the kernel can still exfiltrate every secret it can read over an outbound HTTP connection. Network policy where it is a stripped network namespace with no external route, a proxy-based domain allowlist, or explicit capability grants for specific destinations is the other half of the isolation story that is easy to overlook. The apply case here can range from disabling full network access to using a proxy for redaction, credential injection or simply just allow listing a specific set of DNS records.

## Local sandboxing on developer machines

Everything above is about server-side multi-tenant isolation, where the threat is adversarial code escaping a sandbox to compromise a shared host. There is a related but different problem on developer machines: AI coding agents that execute commands locally on your laptop. The threat model shifts. There is no multi-tenancy. The concern is not kernel exploitation but rather preventing an agent from reading your `~/.ssh` keys, exfiltrating secrets over the network, or writing to paths outside the project. Or you know if you are running Clawdbot locally, then everything is fair game.

The approaches here use OS-level permission scoping rather than kernel boundary isolation.

[Cursor](https://cursor.com/blog/agent-sandboxing) uses Apple's Seatbelt (`sandbox-exec`) on macOS and Landlock plus seccomp on Linux. It generates a dynamic policy at runtime based on the workspace: the agent can read and write the open workspace and `/tmp`, read the broader filesystem, but cannot write elsewhere or make network requests without explicit approval. This reduced agent interruptions by roughly 40% compared to requiring approval for every command, because the agent runs freely within the fence and only asks when it needs to step outside.

OpenAI's [Codex CLI](https://developers.openai.com/codex/security/) takes a similar approach with explicit modes: `read-only`, `workspace-write` (the default), and `danger-full-access`. Network access is disabled by default. Claude Code and Gemini CLI both support sandboxing but ship with it off by default.

The common pattern across all of these seems to be filesystem and network ACLs enforced by the OS, not a separate kernel or hardware boundary. A determined attacker who already has code execution on your machine could potentially bypass Seatbelt or Landlock restrictions through privilege escalation. But that is not the threat model. The threat is an AI agent that is mostly helpful but occasionally careless or confused, and you want guardrails that catch the common failure modes - reading credentials it should not see, making network calls it should not make, writing to paths outside the project.

Apple's new [Containerization framework](https://developer.apple.com/videos/play/wwdc2025/346/) (announced at WWDC 2025) is interesting here. Unlike Docker on Mac, which runs all containers inside a single shared Linux VM, Apple gives each container its own lightweight VM via the [Virtualization framework](https://github.com/apple/containerization) on Apple Silicon. Each container gets its own kernel, its own ext4 filesystem, and its own IP address. It is essentially the microVM model applied to local development, with OCI image compatibility. It is still early, but it collapses the gap between "local development containers" and "properly isolated sandboxes" in a way that Docker Desktop never did.

## Parting notes

The landscape is moving in a clear direction. There is a lot of exciting new tech out there, with people constantly pushing the limits of cold starts toward faster, securely isolated workloads using Python decorators and other novel approaches to make microvms feel like containers. I am excited to see what comes next in this space. It is definitely an area to watch.

---

# 中文翻译

# 让我们聊聊沙箱隔离

当前，围绕不可信代码的沙箱化有着大量的关注热点。AI 代理生成并执行代码、多租户平台运行客户脚本、RL 训练管道评估模型输出——基本上，你面临的是你未编写的代码，你需要运行它，同时防止它损害宿主机、其他租户或以意外方式破坏自身。

"隔离"这个词被随意使用。Docker 容器是"隔离的"。微虚拟机（microVM）是"隔离的"。WebAssembly 模块是"隔离的"。但这些根本是不同的东西，有着不同的边界、不同的攻击面和不同的失效模式。我想记录下关于每一层实际提供什么的学习心得，因为我认为这些区别很重要，能让你为要解决的问题做出明智决策。

## 内核是共享表面

当任何代码在 Linux 上运行时，它通过系统调用与硬件交互。Linux 内核暴露大约 340 个系统调用，内核实现是数千万行 C 代码。每个系统调用都是进入该代码库的入口点。

```
不可信代码 ─( 系统调用 )─→ 宿主机内核 ─( 硬件 API )─→ 硬件
                              [ 4000 万行 C 代码 ]
```

每种隔离技术都在回答同一个问题：如何减少或消除不可信代码对如此庞大攻击面的访问。

这里一个有用的思维模型是共享状态与专用状态。因为标准容器共享宿主机内核，它们也共享其内部数据结构，如 TCP/IP 协议栈、虚拟文件系统缓存和内存分配器。内核中解析畸形 TCP 数据包的漏洞会影响该宿主机上的每个容器。更强的隔离模型将这些复杂状态推入沙箱，仅向宿主机暴露简单的底层接口，如原始块 I/O 或少量系统调用。

不同方法的区别在于它们在何处划定边界。命名空间（Namespaces）使用相同的内核但限制可见性。Seccomp 使用相同的内核但限制允许的系统调用集。gVisor 等项目使用完全独立的用户空间内核并进行最少的宿主机系统调用。微虚拟机提供专用的客户内核和硬件强制边界。最后，WebAssembly 完全不提供内核访问，而是依赖显式的能力导入。每一步都是质的不同边界，而不仅仅是同一事物的更强版本。

## 命名空间作为可见性墙

Linux 命名空间包装全局系统资源，使进程看起来拥有自己的隔离实例。有八种类型，每种隔离特定资源。

| 命名空间 | 隔离内容 | 进程看到什么 |
|---------|---------|-------------|
| PID | 进程 ID | 自己的进程树，从 PID 1 开始 |
| Mount | 文件系统挂载点 | 自己的挂载表，可以有不同根目录 |
| Network | 网络接口、路由 | 自己的接口、IP 地址、端口 |
| User | UID/GID 映射 | 内部可以是 root，外部是 nobody |
| UTS | 主机名 | 自己的主机名 |
| IPC | SysV IPC、POSIX 消息队列 | 自己的共享内存、信号量 |
| Cgroup | Cgroup 根目录 | 自己的 cgroup 层级 |
| Time | 系统时钟（单调时钟、启动时钟） | 自己的系统运行时间和时钟偏移 |

命名空间是 Docker 容器使用的技术。运行容器时，它会获得自己的 PID 命名空间（看不到宿主机进程）、自己的挂载命名空间（自己的文件系统视图）、自己的网络命名空间（自己的接口）等。

关键要理解的是**命名空间是可见性墙，而非安全边界**。它们阻止进程*看到*命名空间外的东西，但不阻止进程*利用实现命名空间的内核*。进程仍然向同一个宿主机内核发起系统调用。如果内核处理任何系统调用存在漏洞，命名空间边界无济于事。

2024 年 1 月，[CVE-2024-21626](https://seclists.org/oss-sec/2024/q1/78) 显示 `runc`（标准容器运行时）中的文件描述符泄漏允许容器访问宿主机文件系统。容器的挂载命名空间是完整的——逃逸是通过 `runc` 在将控制权交给容器之前未能关闭的泄漏 fd 发生的。2025 年，另外三个 `runc` CVE（CVE-2025-31133、CVE-2025-52565、CVE-2025-52881）展示了允许从容器内部写入受保护宿主机路径的挂载竞争条件。

## Cgroups：记账不等于安全

Cgroups（控制组）限制和统计资源使用：CPU、内存、磁盘 I/O、进程数。它们防止容器消耗所有可用内存或启动数千个进程。

Cgroups 对稳定性很重要，但不是安全边界。它们防止拒绝服务，而非逃逸。受 Cgroups 约束的进程仍然向具有相同攻击面的内核发起系统调用。

## Seccomp-BPF 作为过滤器

Seccomp-BPF 允许你附加一个 Berkeley 数据包过滤器程序，决定允许进程进行哪些系统调用。你可以拒绝危险的系统调用，如进程跟踪、文件系统操作、内核扩展加载和性能监控。

Docker 应用默认的 seccomp 配置文件，阻止约 40 到 50 个系统调用。这有意义地减少了攻击面。但关键限制是 seccomp 是对同一内核的过滤器。你允许的系统调用仍然进入宿主机内核的代码路径。如果写入实现、网络协议栈或任何允许的系统调用路径存在漏洞，seccomp 无济于事。

```
无 Seccomp：
  不可信代码 ─( ~340 个系统调用 )─→ 宿主机内核

有 Seccomp：
  不可信代码 ─( ~300 个系统调用 )─→ 宿主机内核
```

攻击面更小，但边界相同。

### 以特权模式运行容器

这值得特别指出，因为它出乎意料地常见。某些隔离方法需要 Docker 的特权标志。例如，构建使用嵌套 PID 命名空间的自定义沙箱通常会导致开发者使用特权模式，因为为嵌套沙箱挂载新的 `/proc` 文件系统需要 `CAP_SYS_ADMIN` 能力（除非你也使用用户命名空间）。

如果你启用 `--privileged` 只是为了获得 `CAP_SYS_ADMIN` 来进行嵌套进程隔离，你添加了一层（嵌套进程可见性），同时移除了其他几层（seccomp、所有能力限制、设备隔离）。净效果可以说是比标准非特权容器更弱的隔离。这是生产中出现的真实权衡。理想的解决方案是只授予所需的特定能力，而不是全部，或者使用完全不需要宿主机级权限的不同隔离方法。

## gVisor 与用户空间内核

gVisor 是隔离模型发生质的变化的地方。要理解差异，有助于查看标准容器的攻击面。

```
标准容器 (Docker)
┌───────────────────────┐
│ 不可信代码            │
└──────────┬────────────┘
           │ ~340 个系统调用
           ▼
   [ Seccomp 过滤器 ]
           │ ~300 个允许的系统调用
           ▼
┌───────────────────────┐
│ 宿主机内核 (Ring 0)   │ ◄── 完整攻击面
└───────────────────────┘
```

代码作为标准 Linux 进程运行。Seccomp 充当严格的允许列表过滤器，减少允许的系统调用集。然而，任何允许的系统调用仍然直接针对共享的宿主机内核执行。一旦系统调用被允许，处理该请求的内核代码就是宿主机和其他每个容器使用的完全相同的代码。这里的失效模式是：允许的系统调用中的漏洞让代码能够破坏宿主机内核，绕过命名空间边界。

gVisor 不是在宿主机内核上过滤系统调用，而是在不可信代码和宿主机之间插入一个完全独立的内核实现，称为 Sentry。Sentry 不直接访问宿主机文件系统；相反，一个名为 Gofer 的独立进程代表 Sentry 处理文件操作，通过受限协议通信。这意味着即使是 Sentry 自己的文件访问也是受中介的。

```
gVisor
┌───────────────────────┐
│ 不可信代码            │
└──────────┬────────────┘
           │ ~340 个系统调用
           ▼
┌───────────────────────┐
│ gVisor Sentry (Ring 3)│ ◄── 用户空间内核
└──────┬────────┬───────┘
       │        │ 9P / LISAFS
       │        ▼
       │  ┌───────────┐
       │  │   Gofer   │ ◄── 文件 I/O 代理
       │  └─────┬─────┘
       │        │
       ▼        ▼
┌───────────────────────┐
│ 宿主机内核 (Ring 0)   │ ◄── 减少的攻击面
└───────────────────────┘
  (来自 Sentry 的约 70 个宿主机系统调用)
```

Sentry 拦截不可信代码的系统调用并在用户空间处理。它用 Go 重新实现了约 200 个 Linux 系统调用，足以运行大多数应用程序。当 Sentry 实际需要与宿主机交互以读取文件时，它只发出自己高度受限的约 70 个宿主机系统调用。这不仅是对同一表面的更小过滤器；而是完全不同的表面。失效模式显著改变。攻击者必须首先在 gVisor 的系统调用 Go 实现中找到漏洞才能破坏 Sentry 进程，然后找到仅使用这些有限宿主机系统调用从 Sentry 逃逸到宿主机的方法。

Sentry 使用多种机制之一拦截系统调用，如 seccomp 陷阱或 KVM，自 2023 年以来的默认方式是称为 systrap 的 seccomp-trap 方法。

这在实践中意味着，如果有人发现 Linux 内核 I/O 实现中的漏洞，使用 Docker 的容器直接暴露。gVisor 沙箱不会，因为这些系统调用由 Sentry 处理，而 Sentry 不会将它们暴露给宿主机内核。

权衡是性能。每个系统调用都经过用户空间拦截，这增加了开销。I/O 密集型工作负载感受最深。对于短暂代码执行如脚本和测试，通常没问题，但对于持续的高吞吐 I/O，可能有影响。

此外，采用 gVisor，你在赌审计和维护更小代码足迹（Sentry 及其有限的宿主机交互）比保护整个庞大的 Linux 内核表面免受不可信执行更容易。这个赌注并非没有风险，gVisor 本身的 Sentry 也有安全漏洞，但你需要担心的表面积要小得多，而且是用内存安全语言编写的。

## gVisor 之上的纵深防御

gVisor 给你用户空间内核边界。它不会自动提供的是单个 gVisor 沙箱内的多任务隔离。如果你在一个 `runsc` 容器内运行多个不可信执行，你仍需要叠加额外的控制。这里有一种模式：

- **每个任务的 PID + 挂载 + IPC 命名空间**通过 `clone3`——使每个执行与同一 gVisor 沙箱内的其他执行隔离
- **命名空间内的 Seccomp-BPF**——阻止 `clone3`（防止嵌套命名空间逃逸）、`io_uring`（强制回退到 `epoll`）、`ptrace`、内核模块加载等系统调用
- **权限降级**——以 `nobody`（UID 65534）运行，设置 `PR_SET_NO_NEW_PRIVS`
- **临时 tmpfs**用于所有可写路径——清理是单个 `umount2` 系统调用，而非递归目录遍历
- **只读根文件系统**——容器本身不可变
- **基于能力的文件 API**——使用 `openat2` 等将文件写入限制在工作目录，防止通过 `../../etc/passwd` 的路径遍历
- **网络出口控制**——如果沙箱可以自由地"打电话回家"，计算隔离毫无意义。选项范围从完全禁用网络，到运行允许列表代理（如 Squid）阻止沙箱内的 DNS 解析并强制所有流量通过域级允许列表，再到丢弃 `CAP_NET_RAW` 使沙箱无法用原始套接字绕过 DNS。

```
gVisor 容器 (runsc)
 └─ 每个任务的 PID + 挂载命名空间
     └─ Seccomp BPF 过滤器
         └─ 权限降级
             └─ 网络出口控制
                 └─ 临时 tmpfs
                     └─ 能力限制的文件写入
```

每一层捕获不同的攻击类别。gVisor 内的命名空间逃逸到达 Sentry，而非宿主机内核。Seccomp 绕过击中 Sentry 的系统调用实现，而它本身也是沙箱化的。权限提升被降级阻止。任务之间的持久状态泄漏被具有原子卸载清理的临时 tmpfs 阻止。

### 关于 fork 的说明

一个重要的实际细节是，创建子沙箱的进程本身必须是 fork 安全的。如果你运行的是异步运行时，从多线程进程 fork 本质上是不安全的，因为子进程继承锁定的互斥锁并可能损坏状态。解决方案是 fork 服务器模式：在启动异步运行时之前 fork 一个单线程启动器进程，然后让异步运行时通过 Unix 套接字与启动器通信。启动器创建子进程，完全避免多线程 fork 问题。

```
启动
  fork() → 启动器 (单线程，轮询循环)
               │
               ├─ clone3(NEWPID | NEWNS | NEWIPC)
               │
               └─ 子进程 (挂载、权限降级、Seccomp、Execve)

主服务器 (异步运行时)
  │
  └─ AF_UNIX SEQPACKET ─→ 启动器
```

## 用于硬件边界的微虚拟机

微虚拟机使用 CPU 扩展支持的硬件虚拟化，在每个虚拟机中运行每个工作负载及其自己的内核。

```
微虚拟机架构
┌───────────────────────┐
│ 不可信代码            │
└──────────┬────────────┘
           │ 系统调用
           ▼
┌───────────────────────┐
│ 客户内核 (Ring 0)     │ ◄── 专用内核
└──────────┬────────────┘
           │ VirtIO / MMIO
           ▼
┌───────────────────────┐
│ KVM 管理程序 (宿主机) │ ◄── 硬件边界
└──────────┬────────────┘
           │ 安全 API
           ▼
┌───────────────────────┐
│ VMM (用户空间)        │ ◄── 设备模拟
└───────────────────────┘
```

代码在完全独立、硬件支持的环境中运行，有自己的客户内核。这里重要的是区分概念。管理程序是内置在 Linux 内核中的能力，管理 CPU 的硬件虚拟化扩展。虚拟机监视器（VMM）是一个用户空间进程，配置虚拟机、分配内存并模拟最小硬件设备。微虚拟机本身是剥离了传统 PC 遗留物的虚拟机，因此可以在毫秒内启动并使用最少内存。

逃逸客户内核需要在虚拟机监视器的设备模拟或 CPU 的虚拟化功能中找到漏洞，这些漏洞稀有且极具价值。

客户机在 CPU 硬件强制执行的独立虚拟地址空间中运行。客户内核中的漏洞无法访问宿主机内存，因为硬件阻止了这一点。宿主机内核只看到这个用户空间进程。攻击面是管理程序和虚拟机监视器，两者都比容器共享的完整内核表面小几个数量级。

根据工作负载，你通常会看到虚拟机监视器设计的两种不同方法。第一种是严格极简主义，如 Firecracker 项目。专为在单台服务器上运行数千个微小的短时函数而构建，它故意省略热插拔 CPU 或透传物理 GPU 等复杂功能。目标只是尽可能小的攻击面和内存占用。

第二种方法提供更广泛的功能支持，如 Cloud Hypervisor 或 QEMU microvm 项目。为更重、更动态的工作负载构建，它支持热插拔内存和 CPU，这对需要在编译期间扩容的动态构建运行器很有用。它还支持 GPU 透传，这对 AI 工作负载至关重要，同时仍保持微虚拟机的快速启动时间。

### 权衡

与 gVisor 相比，微虚拟机的权衡是每个实例开销更高，但隔离性更强、由硬件强制执行。对于 CI 系统和沙箱平台，你需要创建数千个短时环境，启动时间和内存开销会累积。对于长时、高安全性工作负载，硬件边界是值得的。

快照是一个值得注意的功能。你可以捕获运行中虚拟机的状态，包括 CPU 寄存器、内存和设备，并在以后恢复。这实现了热池：你启动一次虚拟机，安装依赖，快照它，然后恢复克隆，只需毫秒而非每次重新启动。这就是一些平台即使使用完整虚拟机隔离也能实现极快冷启动的方式。

## 完全没有内核的 WebAssembly

WebAssembly 采取了根本不同的方法。不是运行原生代码并过滤其内核访问，WASM 在内存安全的虚拟机中运行代码，该虚拟机根本没有系统调用接口。与宿主机的所有交互都通过显式导入的宿主函数进行。

```
WebAssembly (WASM)
┌───────────────────────┐
│ 不可信代码            │
└──────────┬────────────┘
           │ 函数调用
           ▼
┌───────────────────────┐
│ WASM 运行时 (宿主)    │ ◄── 内存安全虚拟机
└──────────┬────────────┘
           │ 导入的宿主函数
           ▼
┌───────────────────────┐
│ 允许的宿主 API        │ ◄── 显式能力
└───────────────────────┘
```

代码在严格的沙箱中运行，唯一允许的操作是调用宿主提供的函数。如果宿主不提供文件读取函数，WASM 模块根本不能读取文件。这里的失效模式需要 WASM 运行时本身的漏洞，如绕过线性内存检查的越界内存读取。

没有可攻击的系统调用表面，因为代码从不发起系统调用。内存安全由运行时强制执行。线性内存是边界检查的，调用栈不可访问，控制流是类型检查的。现代运行时在实例之间添加保护页和内存清零。

性能特性很吸引人，具有极快的冷启动和最小的内存开销。但实际限制是语言支持。你今天无法在 WASM 中运行任意 Python 脚本，除非将 Python 解释器本身编译到 WASM 及其所有 C 扩展。对于任意语言中的任意代码沙箱化，WASM 尚不可行。对于你控制工具链的代码沙箱化，它很出色。然而，我很好奇 WASM 在通用沙箱化方面是否有未来。浏览器花了数十年解决类似的安全执行不可信代码问题，将这些架构经验移植到后端基础设施感觉是自然演进。

**更新（2026年2月27日）：**[Simon Willison 指出](https://news.ycombinator.com/item?id=47185105)，解释型语言的 WASM 支持比我想象的更成熟。`wasm32-unknown-wasip1` 是 [CPython 的 Tier 2 支持目标](https://peps.python.org/pep-0011/#tier-2)（意味着失败会阻塞发布），有[非官方 WASI 构建](https://github.com/brettcannon/cpython-wasi-build/releases)可用。[Pyodide](https://pyodide.org/) 通过 Emscripten 将 CPython 移植到 WASM，支持 NumPy、pandas 和 SciPy 等包。在 JavaScript 方面，[编译到 WASM 的 QuickJS](https://tools.simonwillison.net/quickjs) 适用于沙箱化 JS 执行。[Wasmer](https://wasmer.io/posts/python-on-the-edge-powered-by-webassembly) 可以在 WASM 上服务器端运行 Python，包括 gevent 和 SQLAlchemy 等原生模块。我还没试过这些，但很期待。

## 光谱

综合起来，领域跨度从快速且弱隔离到较慢但高度安全隔离。

```
                     隔离强度 →
                     攻击面     ↓

命名空间      Seccomp       gVisor         微虚拟机      WASM
   │               │             │              │              │
   │  仅可见性墙   │  同一内核   │  用户空间    │  通过 KVM    │  完全无
   │               │  系统调用   │  独立内核    │  硬件边界    │  内核访问
   │               │  过滤器     │              │              │
   ▼               ▼             ▼              ▼              ▼
  快速            快速          中等           较慢          最快
  最弱            弱            强             最强          强*
                                                           (*范围有限)
```

对于运行你编写和审查过的可信代码，带有 seccomp 配置文件的 Docker 可能没问题。隔离是针对意外干扰，而非对抗性逃逸。

对于在多租户环境中运行不可信代码，如短时脚本、AI 生成的代码或客户提供的函数，你需要真正的边界。gVisor 给你用户空间内核边界和良好的兼容性，而微虚拟机给你具有最强保证的硬件边界。根据你的威胁模型和性能要求，两者都是可辩护的选择。

对于强化学习训练管道，其中 AI 生成的代码在潜在不可信工作器上的沙箱中评估，威胁模型既是代码也是工作器。你需要双向隔离，这推动向微虚拟机或带纵深防御分层的 gVisor。

我学到的教训是，常见错误是将隔离视为二元的。很容易假设如果你使用 Docker，你就是隔离的。现实是，标准 Docker 给你命名空间隔离，这只是共享内核上的可见性墙。这是否足够完全取决于你要保护什么。

还值得记住的是，计算隔离只是问题的一半。你可以将代码放入 gVisor 沙箱或 Firecracker 微虚拟机中，具有硬件边界，但如果沙箱对你的"代理工作负载"有不受限制的网络出口，这些都毫无意义。无法逃逸内核的攻击者仍然可以通过出站 HTTP 连接外泄它能读取的每个秘密。网络策略——无论是剥离的网络命名空间没有外部路由、基于代理的域允许列表，还是特定目的地的显式能力授予——是容易忽视的隔离故事的另一半。这里的应用场景范围可以从禁用完整网络访问到使用代理进行编辑、凭证注入，或简单地将特定 DNS 记录列入允许列表。

## 开发者机器上的本地沙箱化

以上所有内容都是关于服务器端多租户隔离，威胁是对抗性代码逃逸沙箱破坏共享宿主机。开发者机器上有一个相关但不同的问题：在本地笔记本电脑上执行命令的 AI 编码代理。威胁模型转变。没有多租户。关注的不是内核利用，而是防止代理读取你的 `~/.ssh` 密钥、通过网络外泄秘密，或写入项目外的路径。或者你知道如果你在本地运行 Clawdbot，那么一切都是公平的。

这里的方法使用操作系统级权限范围而非内核边界隔离。

[Cursor](https://cursor.com/blog/agent-sandboxing) 在 macOS 上使用 Apple 的 Seatbelt (`sandbox-exec`)，在 Linux 上使用 Landlock 加 seccomp。它基于工作空间在运行时生成动态策略：代理可以读写打开的工作空间和 `/tmp`，读取更广泛的文件系统，但不能在其他地方写入或发出网络请求而不经显式批准。与要求批准每个命令相比，这将代理中断减少了约 40%，因为代理在围栏内自由运行，只在需要跨出时才询问。

OpenAI 的 [Codex CLI](https://developers.openai.com/codex/security/) 采取类似方法，有显式模式：`read-only`、`workspace-write`（默认）和 `danger-full-access`。默认禁用网络访问。Claude Code 和 Gemini CLI 都支持沙箱化，但默认关闭。

所有这些的共同模式似乎是文件系统和网络 ACL 由操作系统强制执行，而非独立内核或硬件边界。已经在你机器上拥有代码执行权限的坚定攻击者可能通过权限提升绕过 Seatbelt 或 Landlock 限制。但这不是威胁模型。威胁是大部分时间有帮助但偶尔粗心或困惑的 AI 代理，你想要能捕获常见失效模式的护栏——读取它不该看的凭证、发出它不该发出的网络调用、写入项目外的路径。

Apple 新的[容器化框架](https://developer.apple.com/videos/play/wwdc2025/346/)（在 WWDC 2025 上宣布）在这里很有趣。与 Mac 上的 Docker 不同，后者在单个共享 Linux 虚拟机中运行所有容器，Apple 通过 Apple Silicon 上的[虚拟化框架](https://github.com/apple/containerization)给每个容器自己的轻量级虚拟机。每个容器有自己的内核、自己的 ext4 文件系统和自己的 IP 地址。它本质上是应用于本地开发的微虚拟机模型，具有 OCI 镜像兼容性。它还在早期阶段，但它以 Docker Desktop 从未做到的方式弥合了"本地开发容器"和"正确隔离的沙箱"之间的差距。

## 临别笔记

领域正朝明确方向前进。有很多令人兴奋的新技术，人们不断推动冷启动极限，使用 Python 装饰器和其他新颖方法实现更快、安全隔离的工作负载，使微虚拟机感觉像容器。我很期待看到这一领域接下来会发生什么。这绝对是一个值得关注的领域。
