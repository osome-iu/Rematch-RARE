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
![image](https://github.com/Zoher15/Rematch-RARE/assets/29090730/59eacc05-7923-4f37-a7a0-6935ce0d6b55)

### Semantic Consistency
![image](https://github.com/Zoher15/Rematch-RARE/assets/29090730/c8c59655-f4df-41cf-a6a5-e2bc6f8d59db)

### Hybrid Consistency
![image](https://github.com/Zoher15/Rematch-RARE/assets/29090730/5a520f05-eb80-43ab-93d5-58fa6beb942f)

### Efficiency
![time space](https://github.com/Zoher15/Rematch-RARE/assets/29090730/2024bc28-be07-42fe-a406-ee46bc2f8680)
|AMR Metric|Time(s)|RAM(GB)|
|---|---|---|
|_smatch_|927|0.2|
|_s2match_|7718|2|
|_sembleu_|275|0.2|
|_WLK_|315|30|
|**_rematch_**|51|0.2|

