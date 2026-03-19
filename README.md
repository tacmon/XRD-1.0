# XRD-AutoAnalyzer-PyTorch 脚本使用说明

本文档介绍了 `Novel-Space-CST` 目录下 8 个 Python 脚本的功能和运行方法。

## 1. `download_mp.py`
**功能**：连接到 Materials Project 数据库，为指定的材料下载 CIF 结构文件。
**用法**：
```bash
python Novel-Space-CST/download_mp.py
```
- 运行脚本后会有一个交互式提示 `输入ID：`，在此处输入 Materials Project ID（不需要输入 "mp-" 前缀，例如输入 `1234` 代表 `mp-1234`）。
- 默认情况下，脚本会将结构 CIF 文件保存到 `./All_CIFS/mp-[ID].cif`。
- **注意**：如果需要使用您自己的特定 Materials Project API 密钥，请直接在脚本中修改 `api_key` 变量。

## 2. `get-entries.py`
**功能**：扫描包含大量 CIF 文件的 `ICSD/` 目录，筛选并将仅包含指定元素子集的材料的 CIF 文件复制到 `../All_CIFs/` 目录。
**用法**：
```bash
python Novel-Space-CST/get-entries.py
```
- **使用前提**：在运行之前，打开该脚本并修改 `inc_elems` 集合（当前为 `{'Li', 'Sn', 'In', 'O'}`）以定义您要筛选的元素组成空间。此外，当前工作目录下必须有一个名为 `ICSD/` 的文件夹，其中包含大量的原始 CIF 文件。

## 3. `construct_xrd_model.py`
**功能**：从参考 CIF 文件生成虚拟的、扩增的 XRD 训练集，并训练一个基于 PyTorch 的卷积神经网络（CNN）来对 XRD 图谱进行分类。
**用法**：
```bash
python Novel-Space-CST/construct_xrd_model.py [选项]
```
**重要选项**：
- `--skip_filter`：跳过最初将 CIF 从 `All_CIFs` 过滤到 `References` 的步骤（如果 `References` 目录已准备好，请使用此选项）。
- `--num_spectra=N`：每个物相模拟生成的扩增图谱数量（默认为 50）。
- `--num_epochs=N`：CNN 训练的轮数（默认为 50）。
- `--min_angle=N` / `--max_angle=N`：2-theta 角度的范围（默认值：20.0 到 60.0）。
- `--save`：将生成的 XRD 图谱数据保存到 `XRD.npy`。
- 最终会输出一个训练好的模型文件 `Model.pth`。

## 4. `construct_pdf_model.py`
**功能**：与 XRD 模型构建类似，生成模拟的对分布函数（PDF）图谱，并训练一个独立的 PyTorch CNN 模型。
**用法**：
```bash
python Novel-Space-CST/construct_pdf_model.py [选项]
```
- **要求**：运行此脚本时，工作目录中必须已经有一个训练好的 `Model.pth`（由 `construct_xrd_model.py` 生成）。脚本会自动将 `Model.pth` 移至 `Models/` 目录，并将其自己新训练的模型命名为 `PDF_Model.pth` 放在同一目录下。
- 支持与 XRD 生成脚本类似的生成参数（例如 `--num_spectra`, `--num_epochs`）。

## 5. `generate_theoretical_spectra.py`
**功能**：根据 `References/` 目录下的结构 CIF 文件，生成精确的理论（无噪声）平滑 XRD 图谱。应用简单的展宽方案（高斯展宽），使其显示为连续曲线而不是离散的线条。
**用法**：
```bash
python Novel-Space-CST/generate_theoretical_spectra.py
```
- 脚本会将包含两列（2-theta 角度和强度）的 `.txt` 数据文件输出到 `Spectra/` 目录，文件名以 `_Theoretical.txt` 结尾。

## 6. `extract_ranges.py`
**功能**：扫描 `Spectra/` 目录中的实验图谱 `.txt` 文件，提取并记录每个图谱的最小和最大 2-theta 角度。
**用法**：
```bash
python Novel-Space-CST/extract_ranges.py
```
- 扫描 `Spectra/` 目录，并生成一个 `angle_ranges.csv` 文件，该文件将每个提取的文件名映射回其经验最小/最大角度范围。

## 7. `run_CNN.py`
**功能**：使用训练好的 PyTorch 模型进行预测/推断，以识别和量化 `Spectra/` 目录下测试图谱中的晶相。
**用法**：
```bash
python Novel-Space-CST/run_CNN.py [选项]
```
**重要选项**：
- `--max_phases=N`：混合物中预测的最大不同物相数量（默认为 3）。
- `--min_conf=N`：敲定物相预测所需的最低置信度分数（默认为 40.0）。
- `--inc_pdf`：利用结合了 XRD 和 PDF 模型的集成方法扩展预测能力（要求 `Models/XRD_Model.pth` 和 `Models/PDF_Model.pth` 同时存在）。
- `--plot`：显示将识别出的峰值匹配叠加在实验曲线上的图表。
- `--weights`：使用半定量方法输出预测物相的近似质量分数。
- 结果将自动保存到 `result.csv`。

## 8. `visualize.py`
**功能**：为单个图谱创建可视化分析图表，将预测的物相叠加在目标测量图谱上。
**用法**：
```bash
python Novel-Space-CST/visualize.py --spectrum=[文件名.txt] --ph=[物相名1] --ph=[物相名2] [选项]
```
**示例**：
```bash
python Novel-Space-CST/visualize.py --spectrum=test_sample.txt --ph=TiO2 --ph=ZnO --weights --plot
```
- `--spectrum`：`Spectra/` 目录中的目标观测文件。
- `--ph`：提供匹配的物相名称，不需要带 `.cif` 后缀（添加更多 `--ph` 标志可进行多重物相叠加）。
- `--weights`：通过标准的参考强度比（RIR）半定量法打印质量分数。
- `--save`：将可视化结果保存为图像文件。
