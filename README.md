# Rematch-RARE
This repository contains the source code, data, and documentation for the research paper:

```
@inproceedings{kachwala2024rematch,
  title = {Rematch: Robust and Efficient Matching of Local Knowledge Graphs for Improved Structural and Semantic Similarity},
  author = {Kachwala, Zoher and An, Jisun and Kwak, Haewoon and Menczer, Filippo},
  booktitle = {2024 Annual Conference of the North American Chapter of the Association for Computational Linguistics},
  year = {2024},
  url = {https://openreview.net/forum?id=dBnsZ72qUQ},
  eprint = {https://openreview.net/forum?id=T5e7G9UQ1vK}
}
```



![rematchflow](https://github.com/Zoher15/Rematch-RARE/assets/29090730/7f7e9995-2d5c-4b09-897d-d6bb2ebe025c)


An example of rematch similarity calculation for a pair of AMRs. After AMRs are parsed from sentences,
rematch has a two-step process to calculate similarity. First, sets of motifs are generated. Second, the two sets are
used to calculate the Jaccard similarity (intersecting motifs shown in color).

## Authors

* Zoher Kachwala (Indiana University)
* Jisun An (Indiana University)
* Haewoon Kwak (Indiana University)
* Filippo Menczer (Indiana University)

## Abstract

Knowledge graphs play a pivotal role in various applications, such as question-answering and fact-checking. Abstract Meaning Representation (AMR) represents text as knowledge graphs. Evaluating the quality of these graphs involves matching them structurally to each other and semantically to the source text. Existing AMR metrics are inefficient and struggle to capture semantic similarity. We also lack a systematic evaluation benchmark for assessing structural similarity between AMR graphs. To overcome these limitations, we introduce a novel AMR similarity metric, _rematch_, alongside a new evaluation for structural similarity called RARE. Among state-of-the-art metrics, _rematch_ ranks second in structural similarity; and first in semantic similarity by 1--5 percentage points on the STS-B and SICK-R benchmarks. _Rematch_ is also five times faster than the next most efficient metric.
## Keywords

Knowledge Graphs, Graph Matching, Abstract Meaning Representation (AMR), Semantic Graphs, Graph Isomorphism, Semantic Similarity, Structural Similarity.

## Installation and Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/Zoher15/Rematch-RARE.git
   ```
2. Create and activate conda Environment:
   ```bash
   conda env create -f rematch_rare.yml
   ```
   ```bash
   conda activate rematch_rare
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
![image](https://github.com/osome-iu/Rematch-RARE/assets/29090730/ac85dd60-acac-41d9-9c1e-1d7f99e20f5f)

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
![image](https://github.com/osome-iu/Rematch-RARE/assets/29090730/2d27747d-805d-423b-b3bc-1c149a9d57c9)

Steps to reproduce these results:
1. Parse AMRs from STS-B and SICK-R:

   a. Follow the [instructions to install the transition_amr_parser](https://github.com/IBM/transition-amr-parser). Highly recommend creating an independent conda environment called `transition_amr_parser`. Parse `AMR3-structbart-L-smpl` and `AMR3-joint-ontowiki-seed42` by activating the environment and executing the script (requires cuda):
      ```bash
      conda env create -f transition_amr_parser.yml
      conda activate transition_amr_parser
      bash experiments/semantic_consistency/parse_amrs.sh
      ```


   b. (optional) Parse `Spring` by [cloning the repo and following the instructions to install](https://github.com/SapienzaNLP/spring). Highly recommend creating an independent conda environment called `spring`. Also download and unzip the [AMR3 pretrained checkpoint](http://nlp.uniroma1.it/AMR/AMR3.parsing-1.0.tar.bz2). Ensure that the resulting unzipped file (`AMR3.parsing.pt`) is in the cloned repo directory `spring/`. Then run the following, where `<spring_dir>` is the location of your Spring repo (requires cuda):
      ```bash
      conda env create -f spring.yml
      conda activate spring
      bash experiments/semantic_consistency/parse_spring.sh <spring_dir>
      ```


   c. (optional) Parse `Amrbart` by [cloning the repo and following the instructions to install](https://github.com/goodbai-nlp/AMRBART). Highly recommend creating an independent conda environment called `amrbart`. Then run the following, where `<amrbart_dir>` is the location of your Amrbart repo (requires cuda):
      ```bash
      conda env create -f amrbart.yml
      conda activate amrbart
      bash experiments/semantic_consistency/parse_amrbart.sh <amrbart_dir>
      ```
   
4. Evaluate a metric on the test set:
   ```bash
   conda activate rematch_rare
   bash experiments/semantic_consistency/semantic_consistency.sh <metric> <parser>
   ```
   `<metric>` should be one of `rematch`, `smatch`, `s2match`, `sembleu`, `wlk` or `wwlk`.
   
   `<parser>` should be one of `AMR3-structbart-L-smpl`, `AMR3-joint-ontowiki-seed42`, `spring_unwiki` or `amrbart_unwiki`. Ensure the chosen `<parser>` has been executed in the previous step.
### Hybrid Consistency (Bamboo Benchmark)
![image](https://github.com/osome-iu/Rematch-RARE/assets/29090730/41fc3afc-27f2-4717-bc2e-7d2d8a57bfb7)

Please follow the instructions in the [Bamboo repo](https://github.com/flipz357/bamboo-amr-benchmark). Do note that by default, Bamboo uses Pearsonr, but for our analysis we chose Spearmanr. That change can be made easily in the [evaluation script](https://github.com/flipz357/bamboo-amr-benchmark/blob/main/evaluation-suite/evaluate4tasks.py) by using find and replace. The word `pearsonr` needs to be replaced with `spearmanr`.

### Efficiency
![image](https://github.com/osome-iu/Rematch-RARE/assets/29090730/9c5dc4f0-0c79-46a4-8811-1eb7a45c1b18)

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
   conda activate rematch_rare
   python experiments/efficiency/generate_matchups.py
   ```
2. Evaluate a specific `<metric>`, one of `rematch`, `smatch`, `s2match`, `sembleu` or `wlk`:
   ```bash
   bash experiments/efficiency/efficiency.sh <metric>
   ```
4. If all metrics have been executed, the plots from the paper can be reproduced by (save in `data/processed/AMR3.0`):
   ```bash
   python experiments/efficiency/plot_complexity.py
   ```
