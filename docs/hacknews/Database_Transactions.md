URL: https://planetscale.com/blog/database-transactions

## Database Transactions

数据库事务

By Ben Dicken | January 14, 2026

作者：Ben Dicken | 2026 年 1 月 14 日

Transactions are fundamental to how SQL databases work. Trillions of transactions execute every single day, across the thousands of applications that rely on SQL databases.

事务是 SQL 数据库工作原理的基础。每天数万亿次事务在数千个依赖 SQL 数据库的应用程序中执行。

## What is a database transaction?

什么是数据库事务？

A transaction is a sequence of actions that we want to perform on a database as a single, atomic operation. An individual transaction can include a combination of reading, creating, updating, and removing data.

事务是我们希望作为单个原子操作在数据库上执行的一系列动作。单个事务可以包括读取、创建、更新和删除数据的组合。

In MySQL and Postgres, we begin a new transaction with `begin;` and end it with `commit;`. Between these two commands, any number of SQL queries that search and manipulate data can be executed.

在 MySQL 和 Postgres 中，我们用 `begin;` 开始一个新事务，用 `commit;` 结束它。在这两个命令之间，可以执行任意数量的搜索和操作数据的 SQL 查询。

The act of committing is what atomically applies all of the changes made by those SQL statements.

提交的行为是原子性地应用这些 SQL 语句所做的所有更改。

There are also times when we want to intentionally undo a partially-executed transaction. This happens when midway through a transaction, we encounter missing / unexpected data or get a cancellation request from a client. For this, databases support the `rollback;` command.

也有时候我们想要有意撤销部分执行的事务。这发生在事务进行到一半时，我们遇到缺失/意外的数据或收到客户端的取消请求。为此，数据库支持 `rollback;` 命令。

In the example above, the transaction made several modifications to the database, but those changes were isolated from all other ongoing queries and transactions. Before the transaction committed, we decided to `rollback`, undoing all changes and leaving the database unaltered by this transaction.

在上面的例子中，事务对数据库做了几次修改，但这些更改与所有其他正在进行的查询和事务隔离。在事务提交之前，我们决定 `rollback`，撤销所有更改，使数据库不受此事务的影响。

## Consistent Reads

一致性读取

During a transaction's execution, we would like it to have a consistent view of the database. This means that even if another transaction simultaneously adds, removes, or updates information, our transaction should get its own isolated view of the data, unaffected by these external changes, until the transaction commits.

在事务执行期间，我们希望它对数据库有一致的视图。这意味着即使另一个事务同时添加、删除或更新信息，我们的事务也应该获得自己隔离的数据视图，不受这些外部变化的影响，直到事务提交。

MySQL and Postgres both support this capability when operating in `REPEATABLE READ` mode (plus all stricter modes, too). However, they each take different approaches to achieving this same goal.

MySQL 和 Postgres 在 `REPEATABLE READ` 模式下（以及所有更严格的模式）都支持这种能力。然而，它们各自采取不同的方法来实现这个相同的目标。

## Multi-row versioning in Postgres

Postgres 中的多行版本控制

Postgres handles this with multi-versioning of rows. Every time a row is inserted or updated, it creates a new row along with metadata to keep track of which transactions can access the new version.

Postgres 通过行的多版本控制来处理这个问题。每次插入或更新行时，它都会创建一个新行以及元数据，以跟踪哪些事务可以访问新版本。

MySQL handles this with an undo log. Changes to rows immediately overwrite old versions, but a record of modifications is maintained in a log file, in case they need to be reconstructed.

MySQL 使用 undo 日志来处理这个问题。对行的更改立即覆盖旧版本，但修改的记录保存在日志文件中，以防需要重构。

---

**批判性思考评论：**

这是一篇关于数据库事务基础知识的扎实文章，通过交互式可视化解释了 ACID 属性中的原子性、一致性、隔离性和持久性。

几个值得注意的技术细节：

1. **一致性读取的实现差异**：Postgres 使用多版本并发控制 (MVCC) 创建行的新版本，而 MySQL（InnoDB）使用 undo 日志来重构旧版本。这两种方法各有优劣：
   - Postgres 的 MVCC 读取不阻塞写入，但会产生垃圾回收开销（VACUUM）
   - MySQL 的 undo 日志在写入时需要更多工作，但旧版本可以更快地被回收

2. **隔离级别的微妙之处**：文章提到 `REPEATABLE READ` 模式，但没有深入解释不同隔离级别（Read Committed、Repeatable Read、Serializable）之间的权衡。在高压场景下，隔离级别的选择会显著影响并发性能。

3. **现实世界的复杂性**：虽然文章将事务呈现为干净的原子操作，但现实中的分布式事务（两阶段提交、Saga 模式）要复杂得多。对于跨多个服务的事务，传统的 BEGIN/COMMIT 模型往往不够用。

这篇文章适合作为数据库事务的入门材料，但对于有经验的工程师，可能需要更深入的资源来理解生产环境中的复杂场景。
