# Rematch-RARE
This repository contains the source code, data, and documentation for the research paper titled "Rematch: Robust and Efficient Knowledge Graph Matching for Improved Structural and Semantic Similarity".
![image](https://github.com/Zoher15/Rematch-RARE/assets/29090730/04b4f232-4076-4823-91f8-dd6d0c0542bd)
An example of rematch’s similarity calculation for a pair of AMRs. After AMRs are parsed from sentences,
rematch has a two-step process to calculate similarity. First, sets of motifs are generated. Second, the two sets are
used to calculate the Jaccard similarity (intersecting motifs shown in color).

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

## Data Preprocessing
1. License and download [AMR Annotation 3.0](https://catalog.ldc.upenn.edu/LDC2020T02)
2. Preprocess data by:
   ```bash
   bash methods/preprocess_data/preprocess_amr3.sh <dir>
   ```
   `<dir>` is the directory where your `amr_annotation_3.0_LDC2020T02.tgz` file is located
## Results
### Structural Consistency (RARE)
![image](https://github.com/Zoher15/Rematch-RARE/assets/29090730/787c68a4-2e09-4860-a08f-24b420d905b8)

Steps to reproduce these results:
1. Generate **Randomized AMRs with Rewired Edges** (RARE):
   ```bash
   python experiments/structural_consistency/randomize_amr_rewire.py
   ```
2. Evaluate any metric on RARE test:
   ```bash
   bash experiments/structural_consistency/structural_consistency.sh <metric>
   ```
   `<metric>` should be one of `rematch`, `smatch`, `s2match`, `sembleu`, `wlk` or `wwlk`. Depending on the metric, this could take a while to run.
### Semantic Consistency
![image](https://github.com/Zoher15/Rematch-RARE/assets/29090730/329ade7e-2e6e-4847-965e-7fa8fff3bfdc)

Steps to reproduce these results:
1. Parse AMRs from STS-B and SICK-R:

   a. Parse `AMR3-structbart-L-smpl` and `AMR3-joint-ontowiki-seed42` by:
      ```bash
      bash experiments/semantic_consistency/parse_amrs.sh
      ```


   b. (optional) Parse `Spring` by cloning the [repo](https://github.com/SapienzaNLP/spring). Also download and unzip the [AMR3 pretrained checkpoint](http://nlp.uniroma1.it/AMR/AMR3.parsing-1.0.tar.bz2). Ensure that the resulting unzipped file (`AMR3.parsing.pt`) is in the cloned repo directory `spring/`. Then run (requires cuda):
      ```bash
      bash experiments/semantic_consistency/parse_spring.sh <spring_dir>
      ```
      `<spring_dir>` is where your Spring repo clone is located.


   c. (optional) Parse `Amrbart` by cloning my fork of the [AMRBART repo](https://github.com/Zoher15/AMRBART.git). To resolve errors not addressed by the original repo, also `git reset --hard 4110f1e`. Then run (requires cuda):
      ```bash
      bash experiments/semantic_consistency/parse_amrbart.sh <amrbart_dir>
      ```
      `<amrbart_dir>` is where your Amrbart repo clone is located.

   
4. Evaluate a metric on the test set:
   ```bash
   bash experiments/semantic_consistency/semantic_consistency.sh <metric> <parser>
   ```
   `<metric>` should be one of `rematch`, `smatch`, `s2match`, `sembleu`, `wlk` or `wwlk`.
   
   `<parser>` should be one of `AMR3-structbart-L-smpl`, `AMR3-joint-ontowiki-seed42`, `spring_unwiki` or `amrbart_unwiki`. Ensure the chosen `<parser>` has been executed in the previous step.
### Hybrid Consistency (Bamboo Benchmark)
![image](https://github.com/Zoher15/Rematch-RARE/assets/29090730/8c6de7b9-ed68-4fed-afe6-2ba383360563)

Please follow the instructions in the [Bamboo repo](https://github.com/flipz357/bamboo-amr-benchmark). Do note that by default, Bamboo uses Pearsonr, but for our analysis we chose Spearmanr. That change can be made easily in the [evaluation script](https://github.com/flipz357/bamboo-amr-benchmark/blob/main/evaluation-suite/evaluate4tasks.py) by using find and replace. The word `pearsonr` needs to be replaced with `spearmanr`.

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
1. Generate the time testbed by:
   ```bash
   python experiments/efficiency/generate_matchups.py
   ```
2. Evaluate a specific `<metric>`, one of `rematch`, `smatch`, `s2match`, `sembleu` or `wlk`:
   ```bash
   bash experiments/efficiency/efficiency.sh <metric>
   ```
4. If all metrics have been executed, the plots from the paper can be reproduced by:
   ```bash
   python experiments/efficiency/plot_complexity.py
   ```
