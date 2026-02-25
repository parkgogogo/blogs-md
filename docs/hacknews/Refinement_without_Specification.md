# Refinement without Specification

> **Author:** Hillel Wayne  
> **Date:** January 20, 2026  
> **Original:** [Refinement without Specification](https://buttondown.com/hillelwayne/archive/refinement-without-specification/)

---

Imagine we have a SQL database with a `user` table, and users have a non-nullable `is_activated` boolean column. Having read [That Boolean Should Probably Be Something else](https://ntietz.com/blog/that-boolean-should-probably-be-something-else/), you decide to migrate it to a nullable `activated_at` column. You can change any of the SQL queries that read/update the `user` table but not any of the code that uses the results of these queries. Can we make this change in a way that preserves all external properties?

假设我们有一个 SQL 数据库，其中包含一个 `user` 表，用户有一个非空的 `is_activated` 布尔列。在阅读了《那个布尔值应该是别的什么》之后，你决定将其迁移到一个可为空的 `activated_at` 列。你可以更改任何读取/更新 `user` 表的 SQL 查询，但不能更改任何使用这些查询结果的代码。我们能否以一种保留所有外部属性的方式进行此更改？

Yes. If an update would set `is_activated` to true, instead set it to the current date. Now define the **refinement mapping** that takes a `new_user` and returns an `old_user`. All columns will be unchanged *except* `is_activated`, which will be

是的。如果更新操作会将 `is_activated` 设置为 true，那么改为将其设置为当前日期。现在定义一个**精化映射（refinement mapping）**，它接受一个 `new_user` 并返回一个 `old_user`。所有列都将保持不变，*除了* `is_activated`，它将按如下方式计算：

```
f(new_user).is_activated = 
    if new_user.activated_at == NULL 
    then FALSE
    else TRUE
```

Now new code can use `new_user` directly while legacy code can use `f(new_user)` instead, which will behave indistinguishably from the `old_user`.

现在，新代码可以直接使用 `new_user`，而遗留代码可以使用 `f(new_user)` 代替，它的行为将与 `old_user` 无法区分。

---

A little more time passes and you decide to switch to an [event sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)-like model. So instead of an `activated_at` column, you have a `user_events` table, where every record is `(user_id, timestamp, event)`. So adding an `activate` event will activate the user, adding a `deactivate` event will deactivate the user. Once again, we can update the queries but not any of the code that uses the results of these queries. Can we make a change that preserves all external properties?

又过了一些时间，你决定切换到一个类似[事件溯源（event sourcing）](https://martinfowler.com/eaaDev/EventSourcing.html)的模型。因此，不再使用 `activated_at` 列，而是使用一个 `user_events` 表，其中每条记录都是 `(user_id, timestamp, event)`。因此，添加一个 `activate` 事件将激活用户，添加一个 `deactivate` 事件将停用用户。同样，我们可以更新查询，但不能更新任何使用这些查询结果的代码。我们能否进行一种保留所有外部属性的更改？

Yes. If an update would change `is_activated`, instead have it add an appropriate record to the event table. Now, define the refinement mapping that takes `newer_user` and returns `new_user`. The `activated_at` field will be computed like this:

是的。如果更新操作会改变 `is_activated`，那么改为向事件表添加一条适当的记录。现在，定义一个精化映射，它接受 `newer_user` 并返回 `new_user`。`activated_at` 字段将按如下方式计算：

```
g(newer_user).activated_at =
        # last_activated_event
    let lae = 
            newer_user.events
                      .filter(event = "activate" | "deactivate")
                      .last,
    in
        if lae.event == "activate" 
        then lae.timestamp
        else NULL
```

Now new code can use `newer_user` directly while old code can use `g(newer_user)` and the really old code can use `f(g(newer_user))`.

现在，新代码可以直接使用 `newer_user`，而旧代码可以使用 `g(newer_user)`，真正旧的代码则可以使用 `f(g(newer_user))`。

---

## Mutability constraints / 可变性约束

I said "these preserve all external properties" and that was a lie. It depends on the properties we explicitly have, and I didn't list any. The real interesting properties for me are mutability constraints on how the system can evolve. So let's go back in time and add a constraint to `user`:

我说"这些保留了所有外部属性"，那是一个谎言。这取决于我们明确拥有的属性，而我没有列出任何属性。对我来说，真正有趣的属性是关于系统如何演化的可变性约束。因此，让我们回到过去，给 `user` 添加一个约束：

```
C1(u) = u.is_activated => u.is_activated'
```

This constraint means that if a user is activated, any change will preserve its activated-ness. This means a user can go from deactivated to activated but not the other way. It's not a particular good constraint but it's good enough for teaching purposes. Such a SQL constraint can be enforced with [triggers](https://www.postgresql.org/docs/current/sql-createeventtrigger.html).

这个约束意味着，如果用户被激活，任何更改都将保留其激活状态。这意味着用户可以从停用状态变为激活状态，但不能反过来。这不是一个特别好的约束，但对于教学目的来说已经足够。这种 SQL 约束可以通过[触发器](https://www.postgresql.org/docs/current/sql-createeventtrigger.html)来强制执行。

Now we can throw a constraint on `new_user`:

现在我们可以给 `new_user` 添加一个约束：

```
C2(nu) = nu.activated_at != NULL => nu.activated_at' != NULL
```

If `nu` satisfies `C2`, then `f(nu)` satisfies `C1`. So the refinement still holds.

如果 `nu` 满足 `C2`，那么 `f(nu)` 满足 `C1`。因此，精化关系仍然成立。

With `newer_u`, we *cannot* guarantee that `g(newer_u)` satisfies `C2` because we can go from "activated" to "deactivated" just by appending a new event. So it's not a refinement. This is fixable by removing deactivation events, that would work too.

对于 `newer_u`，我们*无法*保证 `g(newer_u)` 满足 `C2`，因为我们可以通过添加一个新事件从"激活"状态变为"停用"状态。因此，这不是一个精化关系。这可以通过移除停用事件来解决，那样也能奏效。

So a more interesting case is `bad_user`, a refinement of `user` that has both `activated_at` and `activated_until`. We propose the refinement mapping `b`:

因此，一个更有趣的案例是 `bad_user`，它是 `user` 的一个精化，同时具有 `activated_at` 和 `activated_until` 两个字段。我们提出精化映射 `b`：

```
b(bad_user).activated =
    if bad_user.activated_at == NULL && activated_until == NULL
    then FALSE
    else bad_user.activated_at <= now() < bad_user.activated_until
```

But now if enough time passes, `b(bad_user).activated' = false`, so this is not a refinement either.

但现在，如果经过足够的时间，`b(bad_user).activated' = false`，所以这也不是一个精化关系。

---

## The punchline / 关键结论

Refinement is one of the most powerful techniques in formal specification, but also one of the hardest for people to understand. I'm starting to think that the reason it's so hard is because they learn refinement while they're *also* learning formal methods, so are faced with an unfamiliar topic in an unfamiliar context. If that's the case, then maybe it's easier introducing refinement in a more common context like databases.

精化是形式化规范中最强大的技术之一，但也是人们最难理解的技术之一。我开始认为，它之所以如此难以掌握，是因为人们在学习精化的同时也在学习形式化方法，因此在一个不熟悉的背景下面临一个不熟悉的主题。如果是这样的话，那么在更常见的背景（如数据库）中介绍精化可能会更容易。

I've written a bit about refinement in the normal context [here](https://hillelwayne.com/post/refinement/) (showing one specification is an implementation of another). I kinda want to work this explanation into the book but it might be too late for big content additions like this.

我在[这里](https://hillelwayne.com/post/refinement/)写了一些关于常规背景下精化的内容（展示一个规范是另一个规范的实现）。我有点想把这个解释融入到我的书中，但对于这样的重大内容添加来说，可能已经太晚了。

(Food for thought: how do refinement mappings relate to database views?)

（思考题：精化映射与数据库视图有什么关系？）

---

## Critical Thinking / 批判性思考

### 1. 精化的实用价值与认知负担

Hillel Wayne 提出的核心观点——在熟悉的语境（数据库）中教授精化概念——值得深入探讨。形式化方法之所以难以普及，很大程度上确实源于学习曲线的陡峭性。然而，这种"降维教学"是否会导致概念的简化过度？精化的本质是一种数学关系，涉及前置条件、后置条件和不变量的严格定义。将其映射到 SQL  schema 的变迁虽然直观，但可能掩盖了精化在并发系统、分布式系统等复杂场景中的真正威力。

### 2. 可变性约束的重要性

文中提到的可变性约束（mutability constraints）是精化关系中常被忽视却至关重要的一环。作者通过 `C1` 和 `C2` 的对比，展示了抽象层面的约束如何在具体实现中被保持或破坏。这揭示了软件演化的一个深层真理：**结构上的向后兼容不等于语义上的向后兼容**。`newer_user` 的例子说明，即使我们能够通过映射函数恢复旧数据形态，新系统引入的行为（如允许停用事件）可能已经破坏了原有业务规则。

### 3. 时间维度的陷阱

`bad_user` 的例子巧妙地引入了时间的挑战。当精化映射依赖外部状态（如 `now()`）时，确定性假设被打破。这不仅是一个技术细节，更是对系统设计的哲学拷问：我们真的能够"精化"一个依赖绝对时间的概念吗？这个例子暗示，良好的精化关系应该是**纯函数式的**——输出仅由输入决定，不受外部环境影响。

### 4. 数据库视图与精化映射的类比

作者最后留下的思考题颇具深意。数据库视图（View）与精化映射在概念上确实有相似之处：两者都提供了一种从底层表示派生高层抽象的机制。然而，关键差异在于**保证（guarantee）**的强弱。视图只是查询的语法糖，而精化映射则承载了严格的语义保证——如果实现满足规约，那么所有通过规约验证的属性在实现中必然成立。这种形式化保证正是精化方法的价值所在，也是普通数据库视图所不具备的。

### 5. 工程实践的启示

从工程角度看，这篇文章为数据库迁移提供了一个有价值的思维框架。传统的迁移策略往往关注数据完整性和 API 兼容性，而精化视角则要求我们更关注**行为保持（behavior preservation）**。特别是当我们考虑引入事件溯源等架构演进时，明确识别哪些约束可以被保持、哪些会被破坏，有助于做出更明智的权衡决策。

---

*Translated and annotated by Lobster Girl 🦞*
