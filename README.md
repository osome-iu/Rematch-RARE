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
### Structural Consistency
|AMR Metric|RARE|
|---|---|
|_smatch_|96.57|
|_s2match_|94.11|
|_sembleu_|94.83|
|_WLK_|90.39|
|_WWLK_|86.31|
|**_rematch_**|95.32|

![image](https://github.com/Zoher15/Rematch-RARE/assets/29090730/59eacc05-7923-4f37-a7a0-6935ce0d6b55)



### Semantic Consistency
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

![image](https://github.com/Zoher15/Rematch-RARE/assets/29090730/c8c59655-f4df-41cf-a6a5-e2bc6f8d59db)

### Hybrid Consistency
### Efficiency

