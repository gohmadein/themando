# 学术论文同行评审（审稿）指南与英文范例

整理自真实国际英文学术期刊审稿场景的**同行评审（Peer Review）结构指南与完整英文范本**，既适合作为审稿人撰写规范审稿意见的句式参考，也适合作为作者投稿前检视论文论证闭环的自查清单。

---

## 规范英文审稿报告四要素

1. **Recommendation（审稿结论）**：清晰给出 `Accept`、`Minor Revision`、`Major Revision` 或 `Reject`。
2. **Confidential Comments to the Editor（致编辑保密评语）**：面向主编提炼论文的核心选题价值、关键缺陷（如标题过度承诺、核心模型缺乏实证检验）以及给出修改/拒稿建议的决定性理由。
3. **Brief Summary（致作者：论文概述）**：用一段客观精炼的英文概括论文的研究对象、方法流水线与主要结论，展现审稿人对稿件的准确把握。
4. **Major & Minor Comments（分条修改意见）**：
   - **Major Comments（核心问题）**：围绕**贡献定位与标题一致性、问题形式化定义、方法可复现细节、评价指标合理性、基线对比（Baselines）与统计显著性检验**逐条编号阐述，并给出可操作的改进方向。
   - **Minor Comments（细节修订）**：指出拼写错误、术语混用、图表规范及讨论严谨性问题。

---

## 英文审稿意见完整范例

以下为一篇融合文献计量、主题建模与趋势预测论文的完整审稿示例：

### Recommendation

Major Revision

### Confidential Comments to the Editor

The topic is both timely and relevant. It sits at the intersection of big data analytics, AI agents, blockchain technology, digital twins and sustainable supply chain management in megaprojects. However, the paper overpromises. While the title promises 'trustworthy AI agents', the paper is actually a bibliometric and topic-modelling study of 802 Web of Science records. It neither defines nor builds any AI agent system, nor does it evaluate or validate any such system.

As a knowledge-mapping study, however, the paper could be useful. However, the current evidence is too weak to support its claims. The BERTopic results report no topic coherence, diversity, or stability. The authors provide no expert validation or comparison with other topic models. The AKLLS trend prediction model remains at a conceptual level. It comes with no baselines, training/testing protocol, significance tests or solid performance figures. Several extracted topics appear to be only loosely tied to the megaproject SSCM, which suggests that the search and screening process is noisy.

I suggest a major revision. The topic is worth pursuing and the paper has the potential to become a substantial literature-mining study. To achieve this, the authors should narrow their claims, clearly state their real contribution, strengthen their validation and align their title and conclusions with the evidence.

### Comments to the Author

#### Brief Summary

This paper proposes a framework called KS-SSCM to support the sustainable management of supply chains in megaprojects. The framework analyses the existing literature to determine the current state of knowledge in this field. Using BERTopic, it analyses 802 Web of Science publications. Knowledge elements are then ranked by topic attention, influence, activity and theme heat. Finally, it uses an AKLLS trend prediction model to forecast future research directions. The paper concludes that the important knowledge elements in big-data-enabled SSCM for megaprojects are blockchain security, intelligent logistics, business data chain optimisation, industrial sustainability, energy economics and intelligent manufacturing.

#### Major Comments

1. The title and contribution make too many claims about 'trustworthy AI agents'. The paper never defines the task of the agent, its architecture, its inputs and outputs, its decision-making process, the criteria for trustworthiness, or the evaluation metrics. The work is primarily a literature mining and trend analysis study. Either the title and claims should be toned down, or a proper AI agent framework with empirical validation should be added.

2. The problem definition is too broad. The paper covers many themes, including megaproject management, SSCM, big data analytics, AI agents, blockchain technology, digital twins and knowledge mining. However, it never clearly states what computational or decision-support task it actually solves. The authors should specify whether the task is topic discovery, knowledge system construction, trend prediction or AI agent decision support.

3. Section 3.1 reads more like background information than a proper methodology section. It mostly explains why BERTopic, LSTM and KAN are useful by citing earlier work. It does not explain how the present study works in practice. There are no clear definitions of inputs and outputs, no validation protocol and no details of reproducibility.

4. The BERTopic analysis needs stronger validation. The paper reports 14 topics but never validates them. It does not report topic coherence, topic diversity, stability across random seeds, sensitivity to parameters, or expert validation. It also does not compare BERTopic with baselines such as LDA, NMF, or Top2Vec.

5. The Theme Heat metric requires clearer justification. The paper combines Topic Attention, Topic Influence and Topic Activity with entropy weights. The paper does not explain the normalisation or the choice of threshold well enough.

6. There is not enough evidence to support the AKLLS trend prediction. The authors should report the training and testing splits, the temporal validation protocol, the hyperparameters, the model architecture, the number of repeated runs and the RMSE and MAE values with confidence intervals. They should also compare AKLLS with baselines such as ARIMA, Prophet, the moving average model, the LSTM model and the KAN model.

7. The paper overclaims its practical and decision-support value. It makes claims about autonomous decision-making, trustworthy AI-agent adoption, better decision quality, transparency, and resilient supply chain execution. None of these are backed by real-world megaproject data, deployment evidence, simulation, a user study, or an industrial case study. The authors should either soften these claims or support them with evidence.

#### Minor Comments

- Correct typos such as 'Multi-gent System Simulation Technology'.

- Explain the difference between popularity, novelty and future importance. Some topics are in decline yet are still presented as future frontiers.

- Distinguish between trends in academic literature and validated trends in real megaproject practice.
