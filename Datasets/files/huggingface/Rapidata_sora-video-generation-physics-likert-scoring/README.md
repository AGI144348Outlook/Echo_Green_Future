---
dataset_info:
  features:
  - name: Prompt
    dtype: string
  - name: Video
    dtype: string
  - name: LikertScore
    dtype: float64
  - name: LikertScoreNormalized
    dtype: float64
  - name: DetailedResults
    list:
    - name: selectedCategory
      dtype: string
    - name: userDetails
      struct:
      - name: age
        dtype: string
      - name: country
        dtype: string
      - name: gender
        dtype: string
      - name: language
        dtype: string
      - name: occupation
        dtype: string
      - name: userScore
        dtype: float64
  - name: FileName
    dtype: string
  splits:
  - name: train
    num_bytes: 507060
    num_examples: 198
  download_size: 64756
  dataset_size: 507060
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
license: apache-2.0
task_categories:
- video-classification
- text-to-video
language:
- en
tags:
- t2v
- text2video
- texttovideo
- t2i
- likert
- scale
- human
- preference
- coherence
- physics
- collision
- movement
- interactions
pretty_name: t2v Sora Style Likert Scores
size_categories:
- 1K<n<10K
---

<style>

.vertical-container {
    display: flex;  
    flex-direction: column;
    gap: 60px;  
}

.image-container img {
  height: 250px; /* Set the desired height */
  margin:0;
  object-fit: contain; /* Ensures the aspect ratio is maintained */
  width: auto; /* Adjust width automatically based on height */
}

.image-container {
  display: flex; /* Aligns images side by side */
  justify-content: space-around; /* Space them evenly */
  align-items: center; /* Align them vertically */
}

  .container {
    width: 90%;
    margin: 0 auto;
  }

  .prompt {
    width: 100%;
    text-align: center;
    font-weight: bold;
    font-size: 16px;
    height: 60px;
  }

  .score-amount {
margin: 0;
margin-top: 10px;
  }

  .score-percentage {
    font-size: 12px;
    font-weight: semi-bold;
    text-align: right;
  }

  .main-container {
    display: flex;  
    flex-direction: row;
    gap: 60px;  
}

  .good {
    color: #18c54f;
  }
  .bad {
    color: red;
  }
  
</style>

# Rapidata Video Generation Physics Dataset

<a href="https://www.rapidata.ai">
<img src="https://cdn-uploads.huggingface.co/production/uploads/66f5624c42b853e73e0738eb/jfxR79bOztqaC6_yNNnGU.jpeg" width="300" alt="Dataset visualization">
</a>

<a href="https://huggingface.co/datasets/Rapidata/text-2-image-Rich-Human-Feedback">
</a>

<p>
If you get value from this dataset and would like to see more in the future, please consider liking it.
</p>

This dataset was collected in ~1 hour using the [Rapidata Python API](https://docs.rapidata.ai), accessible to anyone and ideal for large scale data annotation.

# Overview

In this dataset, ~6000 human evaluators were asked to rate AI-generated videos based on if gravity and colisions make sense, without seeing the prompts used to generate them. The specific question posed was: "Does gravity, movements, collisions, and interactions make physical sense in this video?"

# Calculation Details

Evaluators were given five response options ranging from "Make total sense" to "Don't make any sense", with numerical values assigned as follows:

- Make total sense = 1
- Mostly make sense = 2
- Somewhat make sense = 3
- Rarely make sense = 4
- Don't make any sense = 5

The final Likert score was calculated based on the evaluators' responses using these assigned numerical values as well as their userScore.

Note that this means the lower the score, the better the performance.

# Videos

The videos in the dataset viewer are previewed as scaled down gifs. The original videos are stored under [Files and versions](https://huggingface.co/datasets/Rapidata/sora-video-generation-gravity-likert-scoring/tree/main/Videos)

These are some of the examples that you will find in the dataset, along with their Likert scale and the prompt used for their generation.

Evaluators have been asked the following:

<h3>
Does gravity, movements, collisions, and interactions make physical sense in this video?
</h3>

<div class="main-container">

  <div class="container">
      <div class="prompt">
          <q>Mouse in chef hat cooking cat dinner in fancy restaurant</q>
      </div>
      <div class="image-container">
          <div>
              <img src="https://assets.rapidata.ai/180_20250114_sora.gif" width=500>
              <div class="score-percentage bad">Score: 3.9797</div>
          </div>
      </div>
  </div>

  <div class="container">
      <div class="prompt">
          <q>Old TV screen size, faded colors, waves crashing over rocks</q>
      </div>
      <div class="image-container">
          <div>
              <img src="https://assets.rapidata.ai/170_20250114_sora.gif" width=500>
              <div class="score-percentage good">Score: 2.2683</div>
          </div>
      </div>
  </div>

</div>

<br/>
<br/>

<div class="main-container">

  <div class="container">
      <div class="prompt">
          <q>Cats playing intense chess tournament, in the background giant hourglass drains between floating islands</q>
      </div>
      <div class="image-container">
          <div>
              <img src="https://assets.rapidata.ai/206_20250114_sora.gif" width=500>
              <div class="score-percentage bad">Score: 4.1136</div>
          </div>
      </div>
  </div>

  <div class="container">
      <div class="prompt">
          <q>Butterfly emerging from blue to gold in morning light</q>
      </div>
      <div class="image-container">
          <div>
              <img src="https://assets.rapidata.ai/067_20250114_sora.gif" width=500>
              <div class="score-percentage good">Score: 2.4006</div>
          </div>
      </div>
  </div>
  
</div>