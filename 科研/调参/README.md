# 机器学习与深度学习自动调参（Optuna）

科研实验超参数自动搜索与优化主力工具：**[Optuna](https://github.com/optuna/optuna)** —— 轻量、框架无关、支持动态构建参数空间的自动超参数优化（HPO）框架。

- **GitHub 仓库**：[https://github.com/optuna/optuna](https://github.com/optuna/optuna)
- **官方文档**：[https://optuna.readthedocs.io/](https://optuna.readthedocs.io/)

---

## 为什么科研调参首选 Optuna？

- **Define-by-Run 动态参数空间**：直接用常规 Python `if`/`for` 语法按运行条件定义超参数（例如根据所选网络骨干动态决定层数与正则系数），代码侵入性极低。
- **先进的智能采样器**：默认采用 **TPE（Tree-structured Parzen Estimator）** 贝叶斯优化算法，比盲目网格搜索（Grid Search）收敛更快，同时支持多目标优化（如兼顾精度与推理延迟）。
- **自动早停剪枝（Pruning）**：在训练前几个 Epoch 识别出表现显著落后的试验（Trial）并提前终止，大幅节省 GPU 实验时间。
- **断点续跑与可视化分析**：只需指定 SQLite/MySQL 存储路径即可支持多卡多进程并发搜索与中断恢复，并可通过 `optuna-dashboard` 生成超参数重要性分析图（可直接辅助论文超参敏感性分析）。

---

## 极简接入示例

```bash
pip install optuna optuna-dashboard
```

```python
import optuna

def objective(trial: optuna.Trial) -> float:
    lr = trial.suggest_float("lr", 1e-5, 1e-2, log=True)
    weight_decay = trial.suggest_float("weight_decay", 1e-6, 1e-2, log=True)
    batch_size = trial.suggest_categorical("batch_size", [32, 64, 128])

    # 调用实验训练与验证函数，返回验证集指标
    val_acc = run_experiment(lr=lr, weight_decay=weight_decay, batch_size=batch_size, trial=trial)
    return val_acc

# 使用 SQLite 持久化记录，便于随时恢复或打开看板查看
study = optuna.create_study(
    study_name="baseline_hpo",
    storage="sqlite:///optuna_study.db",
    direction="maximize",
    load_if_exists=True,
)
study.optimize(objective, n_trials=40)

print("最佳验证集指标:", study.best_value)
print("最佳超参数配置:", study.best_params)
```
