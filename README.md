# XRD-AutoAnalyzer-PyTorch 脚本使用说明

本文档介绍了 `Novel-Space` 目录下 Python 脚本的功能和运行方法，该系统利用卷积神经网络（CNN）对 X 射线衍射（XRD）图谱进行自动化物相识别和量化分析。

## 1. 结构与安装

建议在环境根目录下运行以下命令以安装依赖库（如果尚未安装）：
```bash
pip install -e .
```

所有的主要脚本均位于 `Novel-Space/` 目录下。

## 2. 核心脚本介绍

### (1) `download_mp.py`
**功能**：从 Materials Project 数据库下载指定材料的 CIF 晶体结构文件。
**用法**：
```bash
python Novel-Space/download_mp.py
```
- 运行后会有交互式提示 `输入ID：`，输入 MP ID（如 `1234` 代表 `mp-1234`）。
- 默认保存到 `./All_CIFS/` 目录。

### (2) `get-entries.py`
**功能**：从 `ICSD/` 库中根据元素组成空间过滤并提取 CIF 文件。
**用法**：
```bash
python Novel-Space/get-entries.py
```
- 需要先在脚本中修改 `inc_elems`（例如 `{'Li', 'Sn', 'In', 'O'}`）。

### (3) `construct_xrd_model.py`
**功能**：生成扩增的虚拟 XRD 图谱训练集，并训练一个基于 PyTorch 的 CNN 模型。
**用法**：
```bash
python Novel-Space/construct_xrd_model.py [选项]
```
- **重要选项**：
  - `--num_spectra=N`：每个物相生成的模拟图谱数（默认 50）。
  - `--num_epochs=N`：训练轮数（默认 50）。
  - `--min_angle=N` / `--max_angle=N`：2-theta 范围（默认 20.0 - 60.0）。
- **输出**：训练好的模型文件 `Model.pth`。

### (4) `construct_pdf_model.py`
**功能**：生成模拟的对分布函数（PDF）图谱，并训练独立的 PDF-CNN 模型。
**用法**：
```bash
python Novel-Space/construct_pdf_model.py [选项]
```
- **前提**：目录下需已存在 `Model.pth`，脚本会将其重命名并存放到 `Models/` 目录。

### (5) `run_CNN.py`
**功能**：使用训练好的 PyTorch 模型，对 `Spectra/` 目录下的测试图谱进行晶相识别和推断。
**用法**：
```bash
python Novel-Space/run_CNN.py [选项]
```
- **重要选项**：
  - `--max_phases=N`：最大识别物相数（默认 3）。
  - `--min_conf=N`：最低置信度阈值（默认 40.0）。
  - `--inc_pdf`：结合 PDF 模型进行集成预测。
  - `--plot`：显示物相匹配的可视化图表。
  - `--weights`：输出预测物相的质量分数。
- **输出**：预测结果保存至 `result.csv`。

## 3. 辅助与工具脚本

### (6) `generate_theoretical_spectra.py`
**功能**：基于 `References/` 中的 CIF 生成平滑的理论 XRD 参考图谱。
**用法**：
```bash
python Novel-Space/generate_theoretical_spectra.py
```

### (7) `extract_ranges.py`
**功能**：扫描 `Spectra/` 实验图谱，提取其 2-theta 角度范围并记录在 `angle_ranges.csv` 中。
**用法**：
```bash
python Novel-Space/extract_ranges.py
```

### (8) `visualize.py`
**功能**：对单个图谱进行可视化分析，将特定物相叠加在测量曲线上展示。
**用法**：
```bash
python Novel-Space/visualize.py --spectrum=[文件名.txt] --ph=[物相1] --ph=[物相2] --plot --save
```

### (9) `plot_real_spectra.py`
**功能**：读取 `Spectra/` 下的所有实验数据，按模型基准（如 20-60°, 4501点）进行插值对齐和归一化，并输出可视化曲线。
**用法**：
```bash
python Novel-Space/plot_real_spectra.py
```
- **输出**：图像保存在 `figure/real_data/` 目录下。

### (10) `process_results.py`
**功能**：对 `result.csv` 进行后处理，例如筛选特定物相或处理低置信度的“未知”标记（用于特定项目，如 CST 识别）。
**用法**：
```bash
python Novel-Space/process_results.py
```
- **输出**：保存到 `result_processed.csv`。

---
> [!NOTE]
> 运行过程中如果遇到路径问题，请确保在 `/root/xrd/XRD-1.0/` 或 `Novel-Space/` 目录下执行脚本，部分脚本会自动切换工作目录。
