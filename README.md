# 高光谱像素分割

## 当前实现

光谱角映射逐像素分割，输出类别图；未接入 Specim SDK。

这是可运行的数值基线原型，不等同于网站介绍中的完整系统。

## 输入契约

H×W×B 光谱立方体与 K×B 端元矩阵。核心函数位于 `src/prototype.py` 的 `process`，可直接导入调用。默认命令运行固定种子合成样例，并在代码中断言预期效果；真实数据需由调用者按照函数形状约束传入。

## 快速运行

Python 3.11+。

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/prototype.py --output artifacts
python -m unittest discover -s tests -v
```

## 输出与验证

- `artifacts/result.png`：当前代码生成的结果可视化。
- `artifacts/metrics.json`：样例指标。
- `artifacts/results.npz`：结果数组，按图例顺序编号。

![实际运行结果（合成样例）](artifacts/result.png)

```json
{
  "synthetic_foreground_IoU": 1.0,
  "pixels": 9600
}
```

固定种子回归检查与异常数据检查已运行。图中数据均为合成，不是硬件实测，也不是应用界面截图。

## 需求、架构与边界

[PRD](docs/PRD.md) · [当前原型范围](docs/IMPLEMENTATION.md) · [验证记录](docs/VALIDATION.md)

批量 NumPy 原型，没有实时性保证，端元需用真实标定数据替换。

## 后续里程碑

1. 使用真实输入建立基准数据及明确误差界限。
2. 补充数据导入和交互界面，按需求接入 SDK、设备或模型。
3. 记录独立测试集、资源消耗和失败案例，再评估部署条件。
