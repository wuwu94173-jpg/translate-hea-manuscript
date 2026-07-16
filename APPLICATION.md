# 应用说明

## 1. Skill用途

`translate-hea-manuscript` 用于将已有的高熵合金中文论文翻译为符合材料科学SCI期刊表达习惯的英文稿，并通过本地论文及开放获取文献建立可追溯的术语和表达语料库。

它不是自动撰写综述的工具，也不会为了语言效果改变原稿中的实验数据、计算参数、科学含义或结论强度。

主要适用研究内容包括：

- NbTaMoW、NbMoTaW及NbTaMoWRe_x难熔高熵合金；
- SQS、ATAT、CASTEP及密度泛函理论计算；
- 相结构、XRD、SEM和EDS；
- 弹性常数、弹性模量、硬度及纳米压痕；
- 总态密度、分态密度、赝能隙和d轨道杂化；
- XPS价带谱及理论计算与实验结果对照。

## 2. 安装

将仓库中的以下目录复制到Codex Skills目录：

```text
skills/translate-hea-manuscript
```

Windows PowerShell：

```powershell
Copy-Item -Recurse -Force `
  .\skills\translate-hea-manuscript `
  "$env:USERPROFILE\.codex\skills\translate-hea-manuscript"
```

macOS或Linux：

```bash
cp -R skills/translate-hea-manuscript ~/.codex/skills/translate-hea-manuscript
```

安装后使用以下名称调用：

```text
$translate-hea-manuscript
```

## 3. 推荐项目结构

执行整篇论文翻译时，Skill会根据实际任务建立或使用类似结构：

```text
HEA_translation_project/
├── 01_source_chinese/
├── 02_reference_papers/
│   ├── pdf/
│   ├── markdown/
│   ├── literature_index.md
│   ├── local_literature_index.md
│   └── download_manifest.json
├── 03_translation_resources/
│   ├── terminology_glossary.md
│   ├── standard_expressions.md
│   ├── sentence_patterns.md
│   └── corpus_learning_report.md
├── 04_translation/
│   └── full_english_manuscript.md
└── 05_quality_control/
    ├── terminology_consistency_report.md
    ├── scientific_accuracy_report.md
    ├── grammar_style_report.md
    └── final_translation_report.md
```

不会为了保持目录形式而创建无用空文件夹。

## 4. 读取本地论文

Skill可以读取单个论文文件或整个本地论文目录，支持：

- PDF；
- Markdown；
- TXT；
- DOCX。

示例提示词：

```text
$translate-hea-manuscript

读取 D:\papers\HEA 目录中的本地论文，递归扫描子目录，
建立本地文献索引，去除重复论文，并构建术语和表达库。
```

本地处理规则：

1. 原始文件默认只读，不移动、不改名、不覆盖、不删除。
2. 使用SHA-256识别完全相同的文件。
3. 使用DOI辅助识别不同文件版本的同一篇论文。
4. PDF转换后保留页码锚点，便于术语和表达追溯。
5. 扫描版、公式密集或多栏提取异常的PDF会标记为需要OCR或视觉核查。
6. 只有明确要求时才把原始论文复制到翻译项目中。

如需单独运行导入脚本：

```powershell
python skills/translate-hea-manuscript/scripts/local_corpus.py `
  "D:\papers\HEA" `
  --output-dir HEA_translation_project `
  --recursive
```

## 5. 自动检索开放文献

Skill可通过OpenAlex检索候选论文，并根据材料体系、研究方法、期刊、引用情况和翻译用途进行排序。

示例提示词：

```text
$translate-hea-manuscript

围绕NbTaMoWRe_x合金的弹性性质、电子结构和XPS价带谱，
筛选15至25篇适合语言学习的英文论文，下载许可合规的开放获取PDF，
转换为Markdown并建立术语与表达库。
```

默认规则：

- 默认采用`cc-only`下载策略；
- 不绕过付费墙、登录、验证码或出版商访问控制；
- 下载失败时记录DOI、落地页和失败原因；
- 自动排名只用于生成候选论文，正式学习前仍需核对相关性；
- 已存在可读本地副本时，不重复下载相同论文。

OpenAlex API key应通过`OPENALEX_API_KEY`环境变量提供，不得写入Skill、项目文件或Git提交。

独立运行示例：

```powershell
python skills/translate-hea-manuscript/scripts/literature_pipeline.py `
  --output-dir HEA_translation_project `
  --max-results 25 `
  --download `
  --convert
```

## 6. 翻译单个段落或章节

示例：

```text
$translate-hea-manuscript

翻译下面这段结果与讨论，保持数据和结论强度不变，
并给出关键术语对照及需要作者核实的科学问题：

[粘贴中文段落]
```

默认输出包括：

1. 中文原文；
2. SCI英文译文；
3. 关键术语对照；
4. 重要翻译调整说明；
5. 需要作者核实的问题。

只有存在实质性科学歧义时才要求作者核实，不会因为普通语言选择反复提问。

## 7. 执行整篇论文翻译

推荐提示词：

```text
$translate-hea-manuscript

检查当前项目中的中文论文和本地参考文献。
先导入本地论文并建立术语库，再检索开放文献补充缺失内容。
从标题、摘要和关键词开始，按章节翻译全文；
每章完成后检查术语、数据和科学准确性，最后执行三轮全文终审。
```

整稿流程：

```text
读取中文原稿
→ 识别章节、图表、公式和合金命名
→ 导入本地论文并去重
→ 识别语料覆盖缺口
→ 检索开放文献补充
→ 建立术语与表达资源
→ 按章节翻译
→ 逐章质量检查
→ 合并英文全文
→ 科学准确性终审
→ 语言逻辑终审
→ 全文一致性终审
```

## 8. 科学准确性原则

Skill必须遵守以下约束：

- 不增加原文没有的实验或计算结果；
- 不补写未经原稿支持的机理；
- 不修改数值、单位、正负号和变化趋势；
- 不把相关性或可能原因写成确定因果关系；
- 不删除限定条件；
- 不编造参考文献、仪器型号或计算参数；
- 不混淆cohesive energy与binding energy；
- 不混淆Young's modulus、reduced modulus和indentation modulus；
- 不混淆phase、structural、mechanical和thermodynamic stability。

无法确定的专业含义会被明确标记，而不是静默猜测。

## 9. 文献学习边界

这里的“学习”指建立本地、可追溯的翻译语料资源，不是训练或微调模型。

允许学习：

- 专业术语；
- 常用动词和谨慎性表达；
- 句法结构；
- 段落组织；
- 图表描述方式；
- 理论与实验对照方式。

不会将论文中的长句或段落直接拼接到译稿中。句式应提炼为带可替换槽位的抽象模板，并记录DOI和页码或章节来源。

## 10. 输出与质量报告

整篇翻译完成后，主要输出包括：

```text
full_english_manuscript.md
terminology_consistency_report.md
scientific_accuracy_report.md
grammar_style_report.md
final_translation_report.md
corpus_learning_report.md
```

终稿应满足：

- 可复制到Word或LaTeX继续排版；
- 保留原有章节、图号、表号和公式编号；
- 数据与中文原稿一致；
- 术语在全文中统一；
- 表达符合材料科学论文习惯；
- 重大翻译调整可追溯；
- 未解决的科学歧义单独列出。

## 11. 常见问题

### PDF没有提取出文字

文件可能是扫描版或文本层损坏。使用PDF/OCR流程处理，并核对代表性页面后再加入语料库。

### 同一术语在不同论文中写法不同

结合公式、测试方法和上下文判断；重要歧义至少核对两个可靠来源或一个权威方法定义，并在术语库中记录未采用表达。

### 找不到开放获取PDF

保留论文元数据和访问链接，不绕过访问限制。可使用作者公开稿、机构仓储版本或用户已有的合法本地副本。

### 本地论文与在线论文重复

优先使用可读性最好且版本明确的副本，通过DOI和文件哈希合并记录，只学习一次。

### 是否会上传本地论文

默认不会。读取本地论文不代表允许将其上传到第三方服务或公开仓库。

## 12. 隐私与发布注意事项

以下内容不应提交到GitHub：

- 用户论文原稿；
- 下载的PDF或DOCX论文；
- 生成的翻译项目和质量报告；
- 带有绝对本地路径的manifest；
- API key、访问令牌或`.env`文件；
- 可能包含未公开研究内容的语料库。

仓库的MIT许可证只覆盖Skill代码和仓库文档，不覆盖第三方论文、用户原稿或生成语料。
