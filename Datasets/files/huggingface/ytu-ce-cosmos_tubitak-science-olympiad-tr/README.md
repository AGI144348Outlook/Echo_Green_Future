---
language:
- tr
task_categories:
- question-answering
- multiple-choice
- visual-question-answering
- text-generation
pretty_name: TUBITAK Science Olympiad Dataset
size_categories:
- 1K<n<10K
license: cc-by-4.0
dataset_info:
  features:
  - name: id
    dtype: string
  - name: subject
    dtype: string
  - name: year
    dtype: int64
  - name: stage
    dtype: int64
  - name: question_number
    dtype: int64
  - name: question_image
    dtype: image
  - name: solution_image
    dtype: image
  - name: question_latex
    dtype: string
  - name: solution_latex
    dtype: string
  - name: has_solution
    dtype: bool
  - name: has_figure
    dtype: bool
  - name: has_choices
    dtype: bool
  - name: choice_values
    dtype: string
  - name: has_answer
    dtype: bool
  - name: answer_letter
    dtype: string
  - name: answer_value
    dtype: string
  splits:
  - name: bilgisayar
    num_bytes: 178220803.0
    num_examples: 863
  - name: fizik
    num_bytes: 106735713.0
    num_examples: 332
  - name: matematik
    num_bytes: 129297914.0
    num_examples: 671
  - name: ortaokul_bilgisayar
    num_bytes: 38764774.0
    num_examples: 233
  - name: ortaokul_matematik
    num_bytes: 87348043.0
    num_examples: 599
  download_size: 528873937
  dataset_size: 540367247.0
configs:
- config_name: default
  data_files:
  - split: bilgisayar
    path: data/bilgisayar-*
  - split: fizik
    path: data/fizik-*
  - split: matematik
    path: data/matematik-*
  - split: ortaokul_bilgisayar
    path: data/ortaokul_bilgisayar-*
  - split: ortaokul_matematik
    path: data/ortaokul_matematik-*
---

# TUBITAK Science Olympiad Dataset

This dataset contains multiple-choice and open-ended scientific questions sourced from the TUBITAK (The Scientific and Technological Research Council of Turkey) Science Olympiads spanning various years. It is intended to serve as a benchmark for evaluating the advanced analytical, mathematical, and computational reasoning capabilities of Large Language Models (LLMs) in the Turkish language.

The dataset comprises approximately 2700 problems across five domains: Computer Science, Physics, Mathematics, Middle School Computer Science, and Middle School Mathematics. The raw problems have been formatted, OCR processed (using `deepseek-ai/DeepSeek-OCR-2`), and augmented with structural rules to test multi-step reasoning.

## Dataset Structure
Each entry in the dataset represents a specific problem from the competition stages (typically Stage 1).

- **id**: Unique identifier of the problem (e.g., Matematik_2024_1.Asama_1).
- **subject**: Science domain (Matematik, Fizik, Bilgisayar, Ortaokul Matematik, vb.).
- **year**: The year of the examination.
- **stage**: Examination stage (1 or 2). Note: Computer Science and Physics contain only Stage 1 questions.
- **question_number**: The specific problem number within the exam booklet.
- **question_image**: The primary image associated with the question.
- **solution_image**: Link to the solution image (if any).
- **question_latex**: The textual representation of the problem (includes LaTeX formulations where applicable).
- **solution_latex**: LaTeX formatted solution text (if any).
- **has_solution**: Indicates whether the problem has a solution.
- **has_figure**: Boolean flag indicating if the problem essentially relies on visual context (accuracy is not 100%).
- **has_choices**: Indicates whether the question is multiple-choice or open-ended.
- **choice_values**: Array of multi-choice options (A, B, C, D, E).
- **has_answer**: Indicates whether the problem has an answer.
- **answer_letter**: The correct choice letter.
- **answer_value**: The actual content of the correct choice.

## Important Characteristics & Limitations
- **Visual Context:** Visuals within questions are marked as [IMAGE]. For problems sharing a common block of text or context, the explanatory text/image is embedded on top of the question image of the respective problem. The context format traditionally ends with `\n---\n`.
- **Cancellations:** Most cancelled questions from the official exams were skipped; however, recoverable ones were preserved (e.g., Middle School Computer-2020-Stage1-Booklet A-8 and 9 vs skipped Computer-2014-Stage1-28,30,31).
- **Reference Links:** Solutions to questions that strictly reference the previous problem have been largely modified to be standalone, but perfection is not guaranteed (see Computer-2020-Stage1-21 and 23).
- **Code Excerpts:** In Computer Science branches, the last 10-15 questions are typically C programming tasks formatted heavily in LaTeX. While recent years (e.g., 2025) might have these converted directly to images, older ones (e.g., 2024) do not always have an briefing image. Furthermore, any raw C code present in questions is wrapped within standard markdown c bracket blocks for clarity.
- **AI Intervention:** Please note that artificial intelligence (specifically OCR models) was utilized during the creation and structuring of this dataset, which carries a limited accuracy rate for complex LaTeX rendering.

## Usage
This dataset is particularly useful for:
- **Benchmarking:** Testing LLMs on demanding, multi-step scientific reasoning tasks in non-English contexts.
- **Multimodal Evaluation:** Correlating highly visual problem spaces (like the Physics branch) with text-only analytical capabilities.
- **Chain-of-Thought (CoT) Capabilities:** Eliciting formal proofs and deep understanding in mathematics, kinematics, and logic/code tracing.

## LLM Performance Evaluation / Benchmark

The most recent 2 years of Stage 1 questions for all active branches were evaluated using a strict single-prompt, Chain-of-Thought approach. Models were tasked to reason step-by-step and strictly output the final choice letter.

*(Cancelled ("IPTAL") problems were excluded from Accuracy calculations)*

| Model | Total Pass | Total Fail | Cancelled (Ignored) | Accuracy |
|:---|:---:|:---:|:---:|:---:|
| **Gemini 3.1 Pro** | 326 | 2 | 10 | **99.39%** |
| **Qwen3.5-397B-A17B + Thinking** | 319 | 10 | 9 | **96.96%** |

### Branch-Specific Overview

| Branch | Qwen Pass | Qwen Fail | Qwen Acc. | Gemini Pass | Gemini Fail | Gemini Acc. |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| Computer | 148 | 6 | 96.10% | 152 | 1 | 99.35% |
| Mathematics | 123 | 4 | 96.85% | 126 | 1 | 99.21% |
| Physics | 48 | 0 | 100.00% | 48 | 0 | 100.00% |

## Source & License
The original problems are sourced from the national science olympiads organized by TUBITAK (The Scientific and Technological Research Council of Turkey).

This formalized dataset is provided for research and educational purposes under the **CC BY 4.0** license. Necessary permissions have been acquired from TUBITAK by the research team for publishing this derived benchmark.

## Contact
COSMOS AI Research Group  
Yildiz Technical University Computer Engineering Department  
https://cosmos.yildiz.edu.tr/  
cosmos@yildiz.edu.tr

