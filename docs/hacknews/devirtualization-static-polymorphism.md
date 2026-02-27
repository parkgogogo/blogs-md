# Devirtualization and Static Polymorphism

**原文链接 / Original URL:** https://david.alvarezrosa.com/posts/devirtualization-and-static-polymorphism/  
**作者 / Author:** David Álvarez Rosa  
**发布日期 / Published:** February 25, 2026

---

## 摘要 / Summary

**EN:** This article explores the performance overhead of virtual dispatch in C++ and presents techniques for devirtualization and static polymorphism. It covers how vtables work, compiler optimizations like LTO and the `final` keyword, and the Curiously Recurring Template Pattern (CRTP) as a zero-cost alternative to runtime polymorphism.

**CN:** 本文探讨了 C++ 中虚函数调用的性能开销，并介绍了去虚拟化（devirtualization）和静态多态（static polymorphism）技术。文章涵盖了虚表（vtable）的工作原理、LTO 等编译器优化手段、`final` 关键字的使用，以及奇异递归模板模式（CRTP）作为运行时多态零开销替代方案的原理。

---

Ever wondered why your "clean" polymorphic design underperforms in benchmarks? Virtual dispatch enables polymorphism, but it comes with hidden overhead: pointer indirection, larger object layouts, and fewer inlining opportunities.

> **CN:** 有没有想过为什么你那个"优雅整洁"的多态设计在基准测试中表现不佳？虚函数调度（virtual dispatch）虽然实现了多态性，但它带来了隐藏的性能开销：指针间接寻址、更大的对象内存布局，以及更少的内联优化机会。

Compilers do their best to *devirtualize* these calls, but it isn't always possible. On latency-sensitive paths, it's beneficial to manually replace dynamic dispatch with *static polymorphism*, so calls are resolved at compile time and the abstraction has effectively zero runtime cost.

> **CN:** 编译器会尽其所能对这些调用进行*去虚拟化（devirtualize）*，但这并非总是可行。在对延迟敏感的路径上，手动将动态调度替换为*静态多态（static polymorphism）*是更有利的，这样调用可以在编译时解析，抽象层实际上没有运行时开销。

---

## Virtual Dispatch / 虚函数调度

Runtime polymorphism occurs when a base interface exposes a virtual method that derived classes override. Calls made through a `Base&` are then dispatched to the appropriate override at runtime. Under the hood, a virtual table (`vtable`) is created *for each class*, and a pointer (`vptr`) to the `vtable` is added *to each instance*.

> **CN:** 运行时多态发生在基类接口暴露虚方法、而派生类重写该方法时。通过 `Base&` 进行的调用会在运行时派发到适当的重写方法。在底层，编译器为*每个类*创建一个虚表（`vtable`），并向*每个实例*添加一个指向该虚表的指针（`vptr`）。

![Virtual dispatch diagram](./images/diagram.png)
**Figure 1: Virtual dispatch diagram.** The method `foo` is declared virtual in `Base` and overridden in `Derived`. Both classes get a `vtable`, and each object gets a `vptr` pointing to the corresponding `vtable`.

> **CN:** **图 1：虚函数调度示意图。** 方法 `foo` 在 `Base` 中声明为虚函数，在 `Derived` 中被重写。两个类都有自己的 `vtable`，每个对象都有一个 `vptr` 指向对应的 `vtable`。

On a virtual call, the compiler loads the `vptr`, selects the right slot in the `vtable`, and performs an indirect call through that function pointer. The drawback is that the extra `vptr` increases object size, and the indirection through the `vtable` makes the call hard to predict. This prevents inlining, increases branch mispredictions, and reduces cache efficiency.

> **CN:** 在虚函数调用时，编译器加载 `vptr`，在 `vtable` 中选择正确的槽位，然后通过该函数指针进行间接调用。缺点在于额外的 `vptr` 增加了对象大小，而通过 `vtable` 的间接寻址使调用难以预测。这阻止了内联优化、增加了分支预测失败的几率，并降低了缓存效率。

The best way to observe this phenomenon is by inspecting the assembly code emitted by the compiler for a minimal example:

> **CN:** 观察这一现象的最佳方式是检查编译器为最小示例生成的汇编代码：

```cpp
class Base {
public:
  auto foo() -> int;
};

auto bar(Base* base) -> int {
  return base->foo() + 77;
}
```

For a non-virtual member function `foo` like in the example above, the free function `bar` issues a direct call:

> **CN:** 对于像上面示例中的非虚成员函数 `foo`，自由函数 `bar` 会发出直接调用：

```asm
bar(Base*):
        sub     rsp, 8
        call    Base::foo()  // Direct call (直接调用)
        add     rsp, 8
        add     eax, 77
        ret
```

However, declaring `foo` as `virtual` changes `bar`'s assembly into an indirect, vtable-based call:

> **CN:** 然而，将 `foo` 声明为 `virtual` 会将 `bar` 的汇编代码改变为间接的、基于虚表的调用：

```asm
bar(Base*):
        sub     rsp, 8
        mov     rax, QWORD PTR [rdi]  // vptr (pointer to vtable) - 虚表指针
        call    [QWORD PTR [rax]]     // Virtual call (虚调用)
        add     rsp, 8
        add     eax, 77
        ret
```

---

## Devirtualization / 去虚拟化

Sometimes the compiler can statically deduce which override a virtual call will hit. In those cases, it *devirtualizes* the call and emits a direct call instead (skipping the `vtable`). For example, devirtualization is straightforward when the runtime type is clearly fixed:

> **CN:** 有时编译器可以静态推断虚函数调用将命中哪个重写方法。在这些情况下，它会*去虚拟化*该调用，改为发出直接调用（跳过 `vtable`）。例如，当运行时类型明显固定时，去虚拟化很简单：

```cpp
struct Base {
  virtual auto foo() -> int = 0;
};

struct Derived : Base {
  auto foo() -> int override { return 77; }
};

auto bar() -> int {
  Derived derived;
  return derived.foo();  // compiler knows this is Derived::foo
                         // 编译器知道这是 Derived::foo
}
```

The compiler is able to devirtualize even through a base pointer, as long as it can track the allocation and prove there is only one possible concrete type. The problem is that with traditional compilation, object files are created per translation unit (TU)—compiled and optimized in isolation. The linker simply stitches those objects together, so cross-TU optimizations are inherently limited. That's where compiler flags are useful.

> **CN:** 即使通过基类指针，编译器也能够进行去虚拟化，只要它能追踪分配并证明只有一种可能的具象类型。问题在于，在传统编译中，目标文件是按翻译单元（TU）创建的——被独立编译和优化。链接器只是将这些目标文件缝合在一起，因此跨 TU 的优化本质上是有限的。这就是编译器标志派上用场的地方。

**`-fwhole-program`**
: tells the compiler "this translation unit is the entire program." If no class derives from `Base` in this TU, the compiler is free to assume nothing ever does, and can devirtualize calls on `Base`.

> **CN:** 告诉编译器"这个翻译单元就是整个程序"。如果在这个 TU 中没有类继承自 `Base`，编译器可以自由假设永远不会有，并可以对 `Base` 的调用进行去虚拟化。

**`-flto`**
: link-time optimization. Keeps an intermediate representation in the object files and optimizes across all of them at link time, effectively treating multiple source files as a single TU.

> **CN:** 链接时优化。在目标文件中保留中间表示，并在链接时跨所有文件进行优化，有效地将多个源文件视为单个 TU。

On the language side, `final` is a lightweight way to give the compiler the same guarantee for specific methods:

> **CN:** 在语言层面，`final` 是一种轻量级方式，可以为特定方法向编译器提供相同的保证：

```cpp
class Base {
public:
  virtual auto foo() -> int;
  virtual auto bar() -> int;
};

class Derived : public Base {
public:
  auto foo() -> int override;  // override (可重写)
  auto bar() -> int final;     // final (不可重写)
};

auto test(Derived* derived) -> int {
  return derived->foo() + derived->bar();
}
```

Here, `foo()` can still be overridden, so `derived->foo()` remains a virtual call. However, `bar()` is marked as `final`, so the compiler emits a direct call even though it's declared `virtual` in the base:

> **CN:** 这里，`foo()` 仍然可以被重写，所以 `derived->foo()` 保持为虚调用。然而，`bar()` 被标记为 `final`，因此编译器发出直接调用，即使它在基类中被声明为 `virtual`：

```asm
test(Derived*):
        push    rbx
        sub     rsp, 16
        mov     rax, QWORD PTR [rdi]
        mov     QWORD PTR [rsp+8], rdi
        call    [QWORD PTR [rax]]       // Virtual call (虚调用)
        mov     rdi, QWORD PTR [rsp+8]
        mov     ebx, eax
        call    Derived::bar()          // Direct call (直接调用)
        add     rsp, 16
        add     eax, ebx
        pop     rbx
        ret
```

---

## Static Polymorphism / 静态多态

When the compiler can't devirtualize, one option is to use static polymorphism instead. The canonical tool for this is the Curiously Recurring Template Pattern (CRTP). With CRTP, the base class is templated on the derived class, and invokes methods on it via `static_cast`—no virtual keyword involved:

> **CN:** 当编译器无法去虚拟化时，一个选择是使用静态多态。实现这一点的经典工具是奇异递归模板模式（CRTP）。使用 CRTP，基类以派生类为模板参数，并通过 `static_cast` 调用其方法——不涉及 virtual 关键字：

```cpp
template <typename Derived>
class Base {
public:
  auto foo() -> int {
    return 77 + static_cast<Derived*>(this)->bar();
  }
};

class Derived : public Base<Derived> {
public:
  auto bar() -> int {
    return 88;
  }
};

auto test() -> int {
  Derived derived;
  return derived.foo();
}
```

With `-O3` optimization, the compiler inlines everything and constant-folds the result. No `vtable`, no `vptr`, no indirection. Fully optimized call.

> **CN:** 使用 `-O3` 优化时，编译器会内联所有内容并常量折叠结果。没有 `vtable`，没有 `vptr`，没有间接寻址。完全优化的调用。

```asm
test():
        mov     eax, 165  // 77 + 88
        ret
```

**Trade-off:** The trade-off is that each `Base<Derived>` instantiation is a distinct, unrelated type, so there's no common runtime base to upcast to. Any shared functionality that operates across different derived types must itself be templated.

> **CN:** **权衡：** 每个 `Base<Derived>` 实例化都是一个独立的、不相关的类型，因此没有共同的运行时基类可以向上转型。任何跨不同派生类型操作的共享功能本身也必须是模板化的。

### Deducing this (C++23) / 推导 this（C++23）

C++23's *deducing this* keeps the same static-dispatch model but makes it easier to write. Instead of templating the entire class (and writing `Base<Derived>` everywhere), you template only the member function that needs access to the derived type, and let the compiler deduce `self` from `*this`:

> **CN:** C++23 的*推导 this*保持了相同的静态调度模型，但使其更易于编写。不需要模板化整个类（并在各处写 `Base<Derived>`），你只需要模板化需要访问派生类型的成员函数，并让编译器从 `*this` 推导 `self`：

```cpp
class Base {
public:
  auto foo(this auto&& self) -> int { return 77 + self.bar(); }
};

class Derived : public Base {
public:
  auto bar() -> int { return 88; }
};
```

This yields identical optimized code: `foo` is instantiated as `foo<Derived>`, and the call to `bar` is resolved statically and inlined.

> **CN:** 这产生了相同的优化代码：`foo` 被实例化为 `foo<Derived>`，对 `bar` 的调用被静态解析并内联。

---

## Key Takeaways / 核心要点

**EN:**
1. **Virtual dispatch** enables runtime polymorphism but incurs overhead: vtable lookups, larger objects (vptr), and missed inlining opportunities.
2. **Devirtualization** is when the compiler optimizes virtual calls into direct calls. Enable with `-flto`, `-fwhole-program`, or the `final` keyword.
3. **Static polymorphism** (CRTP, deducing this) eliminates runtime overhead entirely by resolving calls at compile time.
4. **Trade-off:** Static polymorphism loses runtime flexibility—no common base type for heterogeneous collections.

**CN:**
1. **虚函数调度**实现了运行时多态，但带来开销：虚表查找、更大的对象（虚表指针），以及错过的内联机会。
2. **去虚拟化**是编译器将虚调用优化为直接调用的过程。可通过 `-flto`、`-fwhole-program` 或 `final` 关键字启用。
3. **静态多态**（CRTP、推导 this）通过在编译时解析调用，完全消除了运行时开销。
4. **权衡：** 静态多态失去了运行时灵活性——没有共同的基类类型用于异构集合。

---

*Translated for AI/Frontend developers. Original article by David Álvarez Rosa.*
