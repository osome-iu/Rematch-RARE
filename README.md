# Rematch-RARE

This repository contains the source code, data, and documentation for the research paper titled "Rematch: Robust and Efficient Knowledge Graph Matching for Improved Structural and Semantic Similarity".

## Authors

* [Author 1 Name] ([Affiliation])
* [Author 2 Name] ([Affiliation])
* ...

## Abstract

Knowledge graphs play a pivotal role in various applications, such as question-answering and fact-checking. Abstract Meaning Representation (AMR) represents text as knowledge graphs. Evaluating the quality of these graphs involves matching them structurally to each other and semantically to the source text. Existing AMR metrics are inefficient and struggle to capture semantic similarity. We also lack a systematic evaluation benchmark for assessing structural similarity between AMR graphs. To overcome these limitations, we introduce a novel AMR similarity metric, _rematch_, alongside a new evaluation for structural similarity called RARE. Among state-of-the-art metrics, _rematch_ ranks second in structural similarity; and first in semantic similarity by 1--5 percentage points on the STS-B and SICK-R benchmarks. _Rematch_ is also five times faster than the next most efficient metric.
## Keywords

[List relevant keywords here.]

## Installation and Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/Zoher15/Rematch-RARE.git
   ```
2. Create and activate conda Environment:
   ```bash
   conda env create -f rematch-rare.yml
   ```
   ```bash
   conda activate rematch-rare
   ```

## Experiments


41 changes: 39 additions & 2 deletions 41
README.md
@@ -21,16 +21,53 @@ Knowledge graphs play a pivotal role in various applications, such as question-a

   ```bash
   git clone https://github.com/Zoher15/Rematch-RARE.git
   ```
2. Create and activate conda Environment:
   ```bash
   conda env create -f rematch-rare.yml
   ```
   ```bash
   conda activate rematch-rare
   ```

## Experiments
### Structural Consistency
![image](https://github.com/Zoher15/Rematch-RARE/assets/29090730/787c68a4-2e09-4860-a08f-24b420d905b8)

Steps to reproduce this experiment:
1. Download [AMR Annotation 3.0](https://catalog.ldc.upenn.edu/LDC2020T02) to `data/raw` directory
2. Unzip AMR Annotation 3.0:
   ```bash
   tar -xvzf data/raw/amr_annotation_3.0_LDC2020T02.tgz
   ```
3. Merge AMR Annotation 3.0 files (script from [transition amr parser](https://github.com/IBM/transition-amr-parser)):
   ```bash
   python methods/preprocess_data/merge_files.py data/raw/amr_annotation_3.0/data/amrs/split/ data/processed/AMR3.0/
   ```
5. Remove wiki edges from AMRs:
   ```bash
   python methods/preprocess_data/unwikify.py
   ```
6. Generate RARE:
   ```bash
   python methods/RARE/randomize_amr_rewire.py
   ```
### Semantic Consistency
![image](https://github.com/Zoher15/Rematch-RARE/assets/29090730/329ade7e-2e6e-4847-965e-7fa8fff3bfdc)

Steps to reproduce this experiment:

### Hybrid Consistency (Bamboo Benchmark)
![image](https://github.com/Zoher15/Rematch-RARE/assets/29090730/8c6de7b9-ed68-4fed-afe6-2ba383360563)

Steps to reproduce this experiment:

### Efficiency
![time space](https://github.com/Zoher15/Rematch-RARE/assets/29090730/2024bc28-be07-42fe-a406-ee46bc2f8680)
|AMR Metric|Time(s)|RAM(GB)|
|---|---|---|
|_smatch_|927|0.2|
|_s2match_|7718|2|
|_sembleu_|275|0.2|
|_WLK_|315|30|
|**_rematch_**|51|0.2|

Steps to reproduce this experiment:
