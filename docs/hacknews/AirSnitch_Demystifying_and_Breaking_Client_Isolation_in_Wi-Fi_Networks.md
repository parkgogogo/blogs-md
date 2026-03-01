---
title: "AirSnitch: Demystifying and Breaking Client Isolation in Wi-Fi Networks"
url: "https://www.ndss-symposium.org/wp-content/uploads/2026-f1282-paper.pdf"
rating: 9
category: "Security Research"
date: "2026-02-28"
---

# AirSnitch: Demystifying and Breaking Client Isolation in Wi-Fi Networks

**Authors:** Xin'an Zhou, Juefei Pu, Zhutian Liu, Zhiyun Qian, Zhaowei Tan, Srikanth V. Krishnamurthy (University of California, Riverside), Mathy Vanhoef (DistriNet, KU Leuven)

**Conference:** NDSS Symposium 2026, San Diego

## Abstract

Client isolation is a fundamental security feature in Wi-Fi networks, designed to prevent connected devices from communicating with each other. It is widely deployed in enterprise networks, guest Wi-Fi hotspots, and increasingly in home routers. However, our research reveals that client isolation is often implemented in inconsistent and insecure ways across the Wi-Fi stack.

We present AirSnitch, a comprehensive framework for analyzing and testing Wi-Fi client isolation. Our analysis uncovers new attack classes that bypass client isolation in practical scenarios, affecting both home routers and enterprise deployments. The attacks exploit weak synchronization of a client's identity across the network stack—spanning Wi-Fi encryption, routing, and switching layers—allowing determined insiders to obtain full machine-in-the-middle (MitM) capabilities even in modern WPA2/3 networks with isolation enabled.

Every tested router and network was vulnerable to at least one attack variant, demonstrating that client isolation is not delivering the security most defenders expect.

## Key Findings

### 1. Inconsistent Enforcement Across Layers

Our analysis reveals that client isolation enforcement is fragmented across multiple layers of the network stack:

- **Wi-Fi encryption layer**: Relies on per-client encryption keys
- **Routing layer**: Depends on correct address binding
- **Switching layer**: Uses MAC address filtering

The lack of coordination between these layers creates security gaps that attackers can exploit.

### 2. Identity Synchronization Weaknesses

Weak synchronization of a client's identity across the network stack allows attackers to bypass Wi-Fi client isolation at the network layer. This enables:

- Interception of uplink traffic from other clients
- Interception of downlink traffic to other clients  
- Access to internal backend devices in enterprise networks
- Full machine-in-the-middle attacks in guest network scenarios

### 3. Universal Vulnerability

Our testing covered a wide range of devices and network configurations:

- Consumer home routers (multiple brands)
- Enterprise access points
- WPA2 and WPA3 networks
- Guest SSID configurations
- Multi-AP enterprise deployments

**Result:** Every tested router and network was vulnerable to at least one attack variant.

## Attack Vectors

### Attack 1: Encryption Layer Bypass

Exploits inconsistencies in how encryption keys are managed for broadcast/multicast traffic. The attack demonstrates that group keys are often shared across isolated clients, allowing traffic injection and interception.

### Attack 2: Routing Layer Bypass

Targets weak binding between client identity and IP/MAC addresses. By manipulating address resolution protocols, an attacker can redirect traffic intended for other clients through their own device.

### Attack 3: Switching Layer Bypass

Exploits MAC address table poisoning in Wi-Fi access points. The attack causes the AP to misdirect frames intended for one client to the attacker's client instead.

## Impact

The AirSnitch attacks have significant security implications:

1. **Guest Networks**: Attackers on guest networks can intercept traffic from other guests and potentially access internal corporate resources.

2. **Enterprise Networks**: Client isolation between departments or security zones can be bypassed, violating network segmentation policies.

3. **IoT Networks**: Isolated IoT devices can be reached by compromised devices on the same network, undermining isolation-based security architectures.

4. **Eduroam/University Networks**: Attackers without valid credentials can potentially intercept traffic from authenticated users.

## AirSnitch Testing Tool

We have released the AirSnitch testing framework to help network administrators and security researchers test their own networks:

- **GitHub**: https://github.com/vanhoefm/airsnitch
- **Zenodo**: Archived version with full paper replication materials

The tool enables:
- Automated testing of client isolation implementations
- Detection of known vulnerability patterns
- Verification of mitigation effectiveness

## Recommended Mitigations

Based on our analysis, we recommend the following countermeasures:

1. **Standardized Definitions**: The Wi-Fi industry needs clear, standardized definitions of what "client isolation" means and which threats it should mitigate.

2. **Multi-Layer Enforcement**: Client isolation must be enforced consistently across all layers—encryption, routing, and switching—not just at a single point.

3. **Per-Client Group Keys**: Implement unique group keys for each client to prevent broadcast/multicast traffic from being decrypted by other isolated clients.

4. **VLAN-Based Segregation**: Use VLANs to provide stronger isolation guarantees than software-based client isolation alone.

5. **Stronger Spoofing Prevention**: Implement stricter validation of MAC and IP address bindings to prevent address spoofing attacks.

## Conclusion

Our research demonstrates that Wi-Fi client isolation, a security feature relied upon by millions of networks worldwide, is fundamentally broken in its current implementation. The inconsistent enforcement across network layers creates exploitable gaps that attackers can leverage to bypass isolation entirely.

The universal vulnerability across tested devices indicates this is not merely a implementation bug in specific products, but a systemic problem in how client isolation is designed and standardized. We call on the Wi-Fi industry to adopt our recommended mitigations and work toward a more robust security model for client isolation.

---

# 中文翻译

**作者：** 周新安、浦觉飞、刘朱天、钱志云、谭昭威、Srikanth V. Krishnamurthy（加州大学河滨分校），Mathy Vanhoef（鲁汶大学DistriNet研究组）

**会议：** NDSS 2026 Symposium，圣地亚哥

## 摘要

客户端隔离（Client Isolation）是Wi-Fi网络中的一项基础安全功能，旨在防止连接的设备之间相互通信。它广泛应用于企业网络、访客Wi-Fi热点，以及越来越多的家用路由器中。然而，我们的研究揭示，客户端隔离在Wi-Fi协议栈中的实现往往存在不一致和不安全的问题。

我们推出了AirSnitch，一个用于分析和测试Wi-Fi客户端隔离的综合性框架。我们的分析发现了在实际场景中可以绕过客户端隔离的新型攻击类别，影响家用路由器和企业级部署。这些攻击利用了客户端身份在网络栈各层之间的弱同步问题——涵盖Wi-Fi加密层、路由层和交换层——使得有决心的攻击者即使在启用了隔离功能的现代WPA2/3网络中也能获得完整的中间人（MitM）攻击能力。

我们测试的每一台路由器和网络都至少易受一种攻击变体的影响，这表明客户端隔离并未提供大多数防御者所期望的安全性。

## 核心发现

### 1. 跨层执行不一致

我们的分析显示，客户端隔离的执行在网络栈的多个层之间是碎片化的：

- **Wi-Fi加密层**：依赖每个客户端的加密密钥
- **路由层**：依赖正确的地址绑定
- **交换层**：使用MAC地址过滤

这些层之间缺乏协调，造成了攻击者可以利用的安全漏洞。

### 2. 身份同步弱点

客户端身份在网络栈各层之间的弱同步允许攻击者在网络层绕过Wi-Fi客户端隔离。这使得攻击者能够：

- 拦截其他客户端的上行流量
- 拦截其他客户端的下行流量
- 访问企业网络中的内部后端设备
- 在访客网络场景中实施完整的中间人攻击

### 3. 普遍性漏洞

我们的测试涵盖了广泛的设备和网络配置：

- 消费级家用路由器（多个品牌）
- 企业级接入点
- WPA2和WPA3网络
- 访客SSID配置
- 多AP企业部署

**结果：** 我们测试的每一台路由器和网络都至少易受一种攻击变体的影响。

## 攻击向量

### 攻击1：加密层绕过

利用广播/组播流量的加密密钥管理不一致性。该攻击表明，组密钥通常在隔离的客户端之间共享，允许流量注入和拦截。

### 攻击2：路由层绕过

针对客户端身份与IP/MAC地址之间的弱绑定。通过操纵地址解析协议，攻击者可以将原本发往其他客户端的流量重定向到自己的设备。

### 攻击3：交换层绕过

利用Wi-Fi接入点中的MAC地址表中毒攻击。该攻击导致AP将原本发往一个客户端的帧错误地发送到攻击者的客户端。

## 影响

AirSnitch攻击具有重大的安全影响：

1. **访客网络**：访客网络上的攻击者可以拦截其他访客的流量，并可能访问内部企业资源。

2. **企业网络**：部门之间或安全区域之间的客户端隔离可以被绕过，违反网络分段策略。

3. **物联网网络**：被入侵的设备可以访问隔离的物联网设备，破坏基于隔离的安全架构。

4. **Eduroam/大学网络**：没有有效凭证的攻击者可能拦截已认证用户的流量。

## AirSnitch测试工具

我们发布了AirSnitch测试框架，帮助网络管理员和安全研究人员测试他们自己的网络：

- **GitHub**: https://github.com/vanhoefm/airsnitch
- **Zenodo**: 包含完整论文复现材料的存档版本

该工具支持：
- 客户端隔离实现的自动化测试
- 已知漏洞模式的检测
- 缓解措施有效性的验证

## 建议的缓解措施

基于我们的分析，我们建议以下对策：

1. **标准化定义**：Wi-Fi行业需要明确定义"客户端隔离"的含义，以及它应该缓解哪些威胁。

2. **多层强制执行**：客户端隔离必须在所有层——加密、路由和交换——一致地执行，而不仅仅在单个点上。

3. **每客户端组密钥**：为每个客户端实现唯一的组密钥，防止其他隔离客户端解密广播/组播流量。

4. **基于VLAN的隔离**：使用VLAN提供比纯软件客户端隔离更强的隔离保证。

5. **更强的欺骗防护**：实施更严格的MAC和IP地址绑定验证，防止地址欺骗攻击。

## 结论

我们的研究表明，Wi-Fi客户端隔离——一项被全球数百万网络所依赖的安全功能——在其当前实现中是根本性的损坏。跨网络层的不一致执行造成了可利用的漏洞，攻击者可以利用这些漏洞完全绕过隔离。

测试设备中的普遍性漏洞表明，这不是特定产品的实现错误，而是客户端隔离设计和标准化中的系统性问题。我们呼吁Wi-Fi行业采纳我们建议的缓解措施，并致力于建立更强大的客户端隔离安全模型。
