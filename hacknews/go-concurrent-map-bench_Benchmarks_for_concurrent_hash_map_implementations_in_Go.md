URL: https://github.com/puzpuzpuz/go-concurrent-map-bench

## go-concurrent-map-bench

## go-concurrent-map-bench（Go 并发哈希表基准测试）

Benchmarks for concurrent hash map implementations in Go.

Go 并发哈希表实现的基准测试。

Disclaimer: I'm the author of [xsync](https://github.com/puzpuzpuz/xsync), one of the libraries benchmarked here. I did my best to keep this benchmark neutral and fair to all implementations. If you spot any issues or have suggestions for improvements, please open an issue.

免责声明：我是 [xsync](https://github.com/puzpuzpuz/xsync) 的作者，这是本次基准测试的其中一个库。我已尽力保持基准测试的中立性，对所有实现都公平公正。如果您发现任何问题或有改进建议，请提交 issue。

## Participants

## 参与者

### [sync.Map](https://pkg.go.dev/sync#Map) (stdlib)

### [sync.Map](https://pkg.go.dev/sync#Map)（标准库）

Since Go 1.24, sync.Map is backed by a HashTrieMap — a concurrent hash trie with 16-way branching at each level. Reads are lock-free via atomic pointer traversal through the trie nodes. Writes acquire a per-node mutex, affecting only a small subtree. The trie grows lazily as entries are inserted.

从 Go 1.24 开始，sync.Map 底层使用 HashTrieMap 实现——这是一个每层有 16 路分支的并发哈希字典树。读取操作通过原子指针遍历字典树节点实现无锁；写入操作则获取每个节点的互斥锁，仅影响一小部分子树。随着条目的插入，字典树会惰性增长。

### [xsync.Map](https://github.com/puzpuzpuz/xsync)

### [xsync.Map](https://github.com/puzpuzpuz/xsync)

A hash table organized into cache-line-sized buckets, each holding up to 5 entries. Each bucket has its own mutex for writes, while reads are fully lock-free using atomic loads. Lookups use SWAR (SIMD Within A Register) techniques on per-entry metadata bytes for快速键过滤. Table resizing is cooperative: all goroutines help migrate buckets during growth.

哈希表被组织成缓存行大小的桶，每个桶最多容纳 5 个条目。每个桶有自己的互斥锁用于写入，而读取则完全通过原子加载实现无锁。查找操作在每个条目的元数据字节上使用 SWAR（寄存器内 SIMD）技术进行快速键过滤。表扩容是协作式的：所有 goroutine 在扩容期间帮助迁移桶。

### [cornelk/hashmap](https://github.com/cornelk/hashmap)

### [cornelk/hashmap](https://github.com/cornelk/hashmap)

A lock-free hash map combining a hash table index with sorted linked lists for collision resolution. All mutations (insert, update, delete) use atomic CAS operations. A background goroutine triggers table resize when the fill factor exceeds 50%. The sorted list ordering enables efficient concurrent traversal.

一种无锁哈希表，结合哈希表索引和有序链表来解决冲突。所有变更操作（插入、更新、删除）都使用原子 CAS 操作。当填充因子超过 50% 时，后台 goroutine 触发表扩容。有序链表的顺序使得高效的并发遍历成为可能。

### [alphadose/haxmap](https://github.com/alphadose/haxmap)

### [alphadose/haxmap](https://github.com/alphadose/haxmap)

Based on Harris's lock-free linked list algorithm with a hash table index layer. Uses xxHash for hashing and atomic CAS for all mutations. Deletions are lazy (nodes are logically marked before physical removal). Auto-resizes when the load factor exceeds 50%.

基于 Harris 的无锁链表算法，并带有哈希表索引层。使用 xxHash 进行哈希计算，所有变更操作都使用原子 CAS。删除是惰性的（节点在物理移除前会被逻辑标记）。当负载因子超过 50% 时自动扩容。

### [orcaman/concurrent-map](https://github.com/orcaman/concurrent-map)

### [orcaman/concurrent-map](https://github.com/orcaman/concurrent-map)

A straightforward sharded design with 32 fixed shards. Each shard is a regular Go map protected by a sync.RWMutex. Keys are assigned to shards using FNV-32 hashing. The fixed shard count makes it simple and predictable, but limits scalability under high并行度.

一种简单的分片设计，有 32 个固定分片。每个分片是一个受 sync.RWMutex 保护的标准 Go map。键使用 FNV-32 哈希分配到分片。固定的分片数量使其简单且可预测，但在高并行度下限制了可扩展性。

## Workloads

## 工作负载

Each benchmark uses permille-based random operation selection:

每个基准测试使用基于千分比的随机操作选择：

- 100% reads — all loads (warm-up only)

- 100% 读取——全是加载操作（仅用于预热）

- 99% reads — 99% loads, 0.5% stores, 0.5% deletes

- 99% 读取——99% 加载，0.5% 存储，0.5% 删除

- 90% reads — 90% loads, 5% stores, 5% deletes

- 90% 读取——90% 加载，5% 存储，5% 删除

- 75% reads — 75% loads, 12.5% stores, 12.5% deletes

- 75% 读取——75% 加载，12.5% 存储，12.5% 删除

- Range under contention — all goroutines iterate the map while a single background goroutine continuously updates random keys

- 竞争下的遍历——所有 goroutine 遍历映射表，同时单个后台 goroutine 持续更新随机键

## Key Types

## 键类型

- string keys (with a long prefix to stress hashing)

- 字符串键（带有长前缀以压力测试哈希计算）

- int keys

- 整数键

## Map Sizes

## 映射表大小

Size
Approx Footprint
Target

大小
近似内存占用
目标

100
~15 KB
Fits in L1

100
~15 KB
适合 L1 缓存

1,000
~150 KB
Fits in L2

1,000
~150 KB
适合 L2 缓存

100,000
~15 MB
Fits in L3

100,000
~15 MB
适合 L3 缓存

1,000,000
~150 MB
Spills to RAM

1,000,000
~150 MB
溢出到内存

## Warm-up Variants

## 预热变体

- WarmUp — map is pre-populated before the benchmark starts (all workloads)

- 预热——基准测试开始前映射表已预填充（所有工作负载）

- NoWarmUp — map starts empty (mixed workloads only, 100% reads is skipped)

- 无预热——映射表从空开始（仅混合工作负载，跳过 100% 读取）

## How to Run

## 如何运行

# Run all benchmarks
go test -bench . -benchtime 5s

# 运行所有基准测试
go test -bench . -benchtime 5s

# Run a specific library
go test -bench BenchmarkXsyncMapOf -benchtime 5s

# 运行特定库
go test -bench BenchmarkXsyncMapOf -benchtime 5s

# Run only string key benchmarks
go test -bench 'StringKeys' -benchtime 5s

# 仅运行字符串键基准测试
go test -bench 'StringKeys' -benchtime 5s

# Run only warm-up benchmarks at size=1000
go test -bench 'WarmUp.*size=1000' -benchtime 5s

# 仅运行 size=1000 的预热基准测试
go test -bench 'WarmUp.*size=1000' -benchtime 5s

## Environment

## 环境

The benchmark results in this repository were collected on the following setup:

本仓库中的基准测试结果在以下环境下收集：

- CPU: AMD Ryzen 9 7900 12-Core Processor (24 threads)

- CPU：AMD Ryzen 9 7900 12 核处理器（24 线程）

- OS: Linux (amd64)

- 操作系统：Linux (amd64)

- Go: go1.26.0

- Go：go1.26.0

- GOMAXPROCS: 1, 4, 8, 12

- GOMAXPROCS：1, 4, 8, 12

Each benchmark was run with -benchtime 3s -count 3 and results were collected for each GOMAXPROCS value separately.

每个基准测试使用 -benchtime 3s -count 3 运行，并分别为每个 GOMAXPROCS 值收集结果。

## Results

## 结果

Each plot shows ops/s (Y axis) vs GOMAXPROCS (X axis) for all libraries. For read/write workloads, rows correspond to read percentages and columns to map sizes. Range plots have a single row with columns for map sizes.

每个图表显示所有库的 ops/s（Y 轴）与 GOMAXPROCS（X 轴）。对于读写工作负载，行对应读取百分比，列对应映射表大小。遍历图表只有一行，列对应映射表大小。

cornelk/hashmap was benchmarked at sizes 100 and 1,000 only due to significant performance degradation at larger sizes.

cornelk/hashmap 仅在大小为 100 和 1,000 时进行基准测试，因为在更大尺寸下性能显著下降。

### Warm-up, string keys

### 预热，字符串键

/puzpuzpuz/go-concurrent-map-bench/blob/main/results/warmup_stringkeys.png

/puzpuzpuz/go-concurrent-map-bench/blob/main/results/warmup_stringkeys.png

### Warm-up, int keys

### 预热，整数键

/puzpuzpuz/go-concurrent-map-bench/blob/main/results/warmup_intkeys.png

/puzpuzpuz/go-concurrent-map-bench/blob/main/results/warmup_intkeys.png

### No warm-up, string keys

### 无预热，字符串键

/puzpuzpuz/go-concurrent-map-bench/blob/main/results/nowarmup_stringkeys.png

/puzpuzpuz/go-concurrent-map-bench/blob/main/results/nowarmup_stringkeys.png

### No warm-up, int keys

### 无预热，整数键

/puzpuzpuz/go-concurrent-map-bench/blob/main/results/nowarmup_intkeys.png

/puzpuzpuz/go-concurrent-map-bench/blob/main/results/nowarmup_intkeys.png

### Range under contention, string keys

### 竞争下的遍历，字符串键

/puzpuzpuz/go-concurrent-map-bench/blob/main/results/range_stringkeys.png

/puzpuzpuz/go-concurrent-map-bench/blob/main/results/range_stringkeys.png

### Range under contention, int keys

### 竞争下的遍历，整数键

/puzpuzpuz/go-concurrent-map-bench/blob/main/results/range_intkeys.png

/puzpuzpuz/go-concurrent-map-bench/blob/main/results/range_intkeys.png

## Allocation Rates

## 分配率

All libraries report 0 allocs/op across every read/write benchmark. The tables below show B/op (bytes allocated per operation, amortized) for the WarmUp variant. Values are consistent across map sizes and GOMAXPROCS values. Range benchmarks are excluded as they allocate due to iteration overhead (closures, internal snapshots, channel buffers).

所有库在每个读写基准测试中都是 0 allocs/op。下表显示 WarmUp 变体的 B/op（每次操作分配的字节数，均摊）。这些值在不同映射表大小和 GOMAXPROCS 值下保持一致。遍历基准测试被排除在外，因为它们会因迭代开销（闭包、内部快照、通道缓冲区）而分配内存。

String keys:

字符串键：

Library
100% reads
99% reads
90% reads
75% reads

库
100% 读取
99% 读取
90% 读取
75% 读取

sync.Map
0
0
3
9

sync.Map
0
0
3
9

xsync.Map
0
0
1
2

xsync.Map
0
0
1
2

cornelk/hashmap*
0
0
1
4

cornelk/hashmap*
0
0
1
4

alphadose/haxmap
0
0
1
3

alphadose/haxmap
0
0
1
3

orcaman/concurrent-map
0
0
0
0

orcaman/concurrent-map
0
0
0
0

Int keys:

整数键：

Library
100% reads
99% reads
90% reads
75% reads

库
100% 读取
99% 读取
90% 读取
75% 读取

sync.Map
0
0
3
8

sync.Map
0
0
3
8

xsync.Map
0
0
0
2

xsync.Map
0
0
0
2

cornelk/hashmap*
0
0
1
4

cornelk/hashmap*
0
0
1
4

alphadose/haxmap
0
0
1
3

alphadose/haxmap
0
0
1
3

orcaman/concurrent-map
0
0
0
0

orcaman/concurrent-map
0
0
0
0

* cornelk/hashmap was benchmarked at sizes 100 and 1,000 only due to significant performance degradation at larger sizes.

* cornelk/hashmap 仅在大小为 100 和 1,000 时进行基准测试，因为在更大尺寸下性能显著下降。

orcaman/concurrent-map shows zero allocations because its shards use regular Go maps, which don't allocate when overwriting existing keys. Other libraries allocate small amounts during writes due to their internal data structure overhead. sync.Map has the highest per-write allocation cost, while xsync.Map has the lowest among the non-sharded implementations.

orcaman/concurrent-map 显示零分配，因为其分片使用常规 Go map，在覆盖现有键时不会分配。其他库在写入期间会因内部数据结构开销而分配少量内存。sync.Map 的每次写入分配成本最高，而 xsync.Map 在非分片实现中最低。

### Summary

### 总结

Library
Strengths
Weaknesses

库
优点
缺点

sync.Map
Stdlib, no dependencies; excellent read scaling; solid all-round since Go 1.24
Highest per-write allocation cost; slower than xsync.Map under all workloads

sync.Map
标准库，无依赖；出色的读取扩展性；从 Go 1.24 起全面稳健
每次写入分配成本最高；在所有工作负载下都比 xsync.Map 慢

xsync.Map
Fastest in nearly every scenario; best read, write, and iteration scaling; lowest allocations among non-sharded designs
External dependency; writes allocate

xsync.Map
几乎在所有场景下都是最快的；最佳的读取、写入和遍历扩展性；非分片设计中分配最低
外部依赖；写入会分配内存

cornelk/hashmap
Competitive at small sizes with read-heavy workloads
Significant performance degradation at sizes ≥100K with writes; limited to small maps in practice

cornelk/hashmap
在小尺寸和读密集型工作负载下有竞争力
在写入时大小 ≥100K 性能显著下降；实际中仅限于小映射表

alphadose/haxmap
Good read-only performance at small sizes; lock-free design
Poor write scaling under contention; falls behind at higher并行度

alphadose/haxmap
在小尺寸下有不错的只读性能；无锁设计
在竞争下写入扩展性差；在更高并行度下落后

orcaman/concurrent-map
Zero allocations (read/write); simple and predictable; decent single-threaded performance
Fixed 32 shards limit scalability; worst read-only throughput due to mutex overhead; write scaling plateaus early; slowest iteration due to channel-based API

orcaman/concurrent-map
零分配（读/写）；简单可预测；单线程性能尚可
固定 32 分片限制可扩展性；由于互斥锁开销，只读吞吐量最差；写入扩展性早期就达到瓶颈；由于基于通道的 API，遍历最慢

---

## 批判性思考（Critical Thinking）

这份基准测试报告为我们提供了 Go 语言并发哈希表实现的全面对比。以下是一些值得思考的观察：

**1. 作者利益相关性问题**
尽管作者声明自己是 xsync 的作者并声称保持中立，但我们仍应保持批判性眼光。有趣的是，xsync.Map 在几乎所有测试场景中都表现最佳，这确实令人印象深刻，但也提醒我们要独立验证这些结果。

**2. Go 1.24 的 sync.Map 改进**
Go 1.24 将 sync.Map 的底层实现改为 HashTrieMap，这是一个重大改进。标准库选择这种实现说明其设计经过了深思熟虑，具有良好的通用性。对于不想引入外部依赖的项目，sync.Map 现在是一个非常有竞争力的选择。

**3. 分片 vs 无锁设计**
orcaman/concurrent-map 采用简单的分片设计，虽然实现简单且零分配，但固定 32 个分片在高并发场景下明显受限。这说明在并发数据结构中，"简单"往往意味着性能上限较低。相比之下，无锁设计（如 xsync、cornelk/hashmap、haxmap）虽然实现复杂，但能提供更好的扩展性。

**4. 内存分配的双刃剑**
虽然零分配听起来很理想（如 orcaman/concurrent-map），但这并不意味着它就是最佳选择。cornelk/hashmap 在小数据量时表现不错，但在大数据量时性能急剧下降，这说明架构设计比单纯的零分配指标更重要。

**5. 实际应用建议**
- 如果追求极致性能且不介意外部依赖 → xsync.Map
- 如果希望零依赖且性能要求适中 → sync.Map (Go 1.24+)
- 如果需要简单的并发安全映射且并发度不高 → orcaman/concurrent-map
- 避免在生产环境使用 cornelk/hashmap 处理大数据量

**6. 测试方法的合理性**
该基准测试设计相当全面，覆盖了不同的读写比例、键类型、数据大小和预热场景。这种多维度的测试方法值得学习。但值得注意的是，真实生产环境的访问模式可能更加复杂，建议在实际使用前进行应用级别的压力测试。
