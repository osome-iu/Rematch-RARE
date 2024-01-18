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

|AMR Metric|RARE|
|---|---|
|_smatch_|96.57|
|_s2match_|94.11|
|_sembleu_|94.83|
|_WLK_|90.39|
|_WWLK_|86.31|
|**_rematch_**|95.32|

### Semantic Consistency
![image](https://github.com/Zoher15/Rematch-RARE/assets/29090730/329ade7e-2e6e-4847-965e-7fa8fff3bfdc)

**STS-B**
|AMR Metric|spring|amrbart|sbart|mbse|
|---|---|---|---|---|
|_smatch_|53.84|54.67|54.73|55.16|
|_s2match_|56.60|57.15|57.54|57.64|
|_sembleu_|n/a|58.62|58.17|58.95|
|_WLK_|63.18|64.60|64.33|65.37|
|_WWLK_|63.89|64.80|64.34|65.40|
|**_rematch_**|**64.93**|**65.88**|**65.06**|**66.52**|

**SICK-R**
|AMR Metric|spring|amrbart|sbart|mbse|
|---|---|---|---|---|
|_smatch_|58.69|58.89|58.70|57.84|
|_s2match_|58.09|58.56|58.42|57.58|
|_sembleu_|60.15|60.61|59.62|59.57|
|_WLK_|63.09|63.33|63.07|62.59|
|_WWLK_|62.72|62.99|62.55|62.66|
|**_rematch_**|**67.03**|**67.72**|**67.10**|**67.34**|
### Hybrid Consistency (Bamboo Benchmark)
![image](https://github.com/Zoher15/Rematch-RARE/assets/29090730/8c6de7b9-ed68-4fed-afe6-2ba383360563)

### Efficiency
![time space](https://github.com/Zoher15/Rematch-RARE/assets/29090730/2024bc28-be07-42fe-a406-ee46bc2f8680)
|AMR Metric|Time(s)|RAM(GB)|
|---|---|---|
|_smatch_|927|0.2|
|_s2match_|7718|2|
|_sembleu_|275|0.2|
|_WLK_|315|30|
|**_rematch_**|51|0.2|

