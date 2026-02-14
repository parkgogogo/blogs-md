# StoreBridge（bridge-store）架构设计（当前代码版本）

这篇文档用于解释当前仓库里 **StoreBridge** 的架构：它由哪些组件构成、各组件之间如何通信、以及 page/store 的分组模型。

> 场景：浏览器内的 zustand store 作为权威状态；Node/Agent 通过 WebSocket + JSON-RPC 去读取/更新/dispatch/订阅；并支持按 `pageId` 分组、多 store。

---

## 1. 组件拆分（四个概念）

- **StoreBridge Server（Node）**：WebSocket 服务端；负责路由、转发、索引、广播。
- **StoreBridge Browser（Browser）**：运行在页面里的桥接层；把 zustand store “接入桥”，并接收远程 set/dispatch。
- **StoreBridge SDK（Node）**：给 Agent/CLI 用的易用对象；把 JSON-RPC methods 封装成像 DB client 一样的 API。
- **Zustand Store（Browser）**：真实状态所在；Browser 沙箱内存中的 store 是权威状态源。

---

## 2. 架构总览（Mermaid）

```mermaid
flowchart LR
  subgraph Browser[Browser / Web Sandbox]
    UI[Page UI]
    ZS[Zustand Store\n(权威状态)]
    BB[StoreBridge Browser\n(桥接层)]
    UI -->|read/subscribe| ZS
    UI -->|dispatch (local)| ZS
    BB <-->|get/set/dispatch hooks| ZS
  end

  subgraph Node[Node / Local Machine]
    S[StoreBridge Server\n(WS + JSON-RPC Router)]
    SDK[StoreBridge SDK\n(Agent/CLI client)]
    Agent[Agent / CLI / Script]
    Agent -->|call SDK| SDK
    SDK <-->|WS JSON-RPC| S
  end

  BB <-->|WS JSON-RPC| S

  S -.->|indexes| IDX[(Registry\nstoreId->conn\npageId->stores\npageId+storeKey->storeId)]
```

关键点：
- **zustand store 在浏览器里，是权威状态**。
- Node 侧无法直接访问浏览器内存，必须通过 Bridge（WS JSON-RPC）进行。
- Server 不保存“真实 store”，只做 registry/路由，并缓存最近 snapshot 以便订阅者立即拿到。

---

## 3. 分组模型（pageId / storeKey / storeId）

为支持“多 page、多 store”，并避免冲突：

- **storeId**：路由用的唯一 ID（随机生成，连接级唯一）
- **pageId**：语义分组（例如 `subagents-monitor` / `gobang`）
- **storeKey**：同一个 page 下不同 store 的角色名（例如 `main` / `ui` / `log`）

Server 侧维护索引：
- `storeId -> hostConnection`
- `pageId -> Set<storeId>`
- `pageId + storeKey -> storeId`

因此 Agent/CLI 的常见流程是：
1) `page.resolve(pageId, storeKey)` 找到 storeId
2) `store.getState / store.dispatch / store.subscribe` 操作该 storeId

---

## 4. 协议与消息流（JSON-RPC 2.0 over WebSocket）

### 4.1 为什么用 JSON-RPC 2.0
主要是为了：
- 并发请求/响应对应（`id`）
- 统一错误结构（`error`）
- 支持通知（notification：不带 `id`）

### 4.2 关键消息流（Mermaid Sequence）

```mermaid
sequenceDiagram
  participant B as StoreBridge Browser
  participant S as StoreBridge Server
  participant N as StoreBridge SDK (Node)

  Note over B: 浏览器侧启动，拥有 zustand store
  B->>S: notif host.register {storeId,pageId,storeKey,meta,initialState,version}

  Note over N: Agent/CLI 通过 SDK 调用
  N->>S: req page.resolve {pageId,storeKey}
  S-->>N: res {storeId}

  N->>S: req store.subscribe {storeId}
  S-->>N: notif store.stateChanged {storeId,state,version,source="bridge.snapshot"}
  S-->>N: res {ok:true}

  N->>S: req store.dispatch {storeId,action}
  S->>B: req client.dispatch {action,expectedVersion,...}
  B-->>S: res {ok:true,version}
  S-->>N: res {ok:true,version}

  Note over B,S,N: 浏览器 store 变化时主动推送
  B->>S: notif host.stateChanged {storeId,state,version,source}
  S-->>N: notif store.stateChanged {storeId,state,version,source}
```

---

## 5. Meta / Schema（zod -> JSON Schema + description）

Browser 侧允许用 **zod** 来描述：
- state 的结构（stateSchema）
- action payload 的结构（payloadSchema）
- 描述信息（zod `.describe()` + action 的 `description` 字段）

注册时，Browser 会把 zod 转为 JSON Schema，并放在 meta 中：
- `meta.store.stateSchema`
- `meta.store.actions[].payloadSchema`

Server 缓存 meta，Node/Agent 可以通过：
- `store.getMeta(storeId)`
- `page.getStoresMeta(pageId)`
获取“语义化可理解”的 store 结构信息。

---

## 6. 语义化错误（SemanticError）

为了让 Agent 能稳定分支处理异常，错误被标准化为 JSON-RPC error，并在 `error.data.kind` 中提供语义码，例如：
- `STORE_OFFLINE`
- `VERSION_CONFLICT`
- `STORE_NOT_FOUND`
- `INVALID_STATE`
- `INVALID_ACTION_PAYLOAD`

---

## 7. 当前代码位置（仓库结构）

```
packages/bridge-store/
  src/
    server/   # StoreBridge Server
    browser/  # StoreBridge Browser
    node/     # StoreBridge SDK
    shared/   # protocol/types/errors
  test/       # vitest 单元测试
  examples/   # demo（browser + node）
```
