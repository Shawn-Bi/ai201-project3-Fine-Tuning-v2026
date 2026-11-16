# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

TakeMeter sorts r/LocalLLaMA posts into three labels: `evidence_based` (makes a claim backed by a checkable result), `unsupported_claim` (makes a judgment with no evidence), and `question` (asks others for help). It's a small fine-tuned text classifier trained on 196 posts I labeled.

When I first read the community, I noticed three differences:

1. **Does it show concrete test results?** Some posts report generation
   speed, response latency, or how many questions the model got right; others
   only say it's "really strong" or "amazing" without showing any results.
2. **Does it state the test conditions?** Some posts specify the hardware,
   model version, quantization method, and test parameters, and share the
   prompts or code; others never explain how they tested, which makes the
   claims hard for anyone else to check.
3. **Does it report failures and limitations?** Some posts show wrong answers
   and note that the sample was small, or that they only tested on one device
   or in one scenario; others show only the successes and conclude the model
   is great overall.

---

## Label Taxonomy

Community: r/LocalLLaMA

### `evidence_based`

**Definition:** The post contains at least one checkable result — a test number, raw output, or an official link. Test conditions (hardware/model/quantization) alone do not count.

**Example 1:**
> "MoE offload on a 3090: prefill 345 -> 466 t/s" — before/after numbers, hardware, and commands. https://www.reddit.com/r/LocalLLaMA/comments/1xx1owx/

**Example 2:**
> "Berth v0.6.0" — measured counts on an RTX 4090 workstation and an official repo link. https://www.reddit.com/r/LocalLLaMA/comments/1xx9fjs/

### `unsupported_claim`

**Definition:** The post makes a judgment about a model or tool, but contains none of the evidence above.

**Example 1:**
> "AI prose feels so bad to read..." — judges local models' prose with no evidence. https://www.reddit.com/r/LocalLLaMA/comments/1xuqyfu/

**Example 2:**
> "Finally clicked for me: local AI is the future" — opinion and prediction, no measurement. https://www.reddit.com/r/LocalLLaMA/comments/1xwf8bb/

### `question`

**Definition:** The post contains a sentence asking others for help.

**Example 1:**
> "Best direction to go for my setup EPYC 32core..." — asks for hardware and software advice. https://www.reddit.com/r/LocalLLaMA/comments/1xx6dpd/

**Example 2:**
> "Is there a community about finetuning..." — asks where to find a community. https://www.reddit.com/r/LocalLLaMA/comments/1xwyfr8/

### The hardest boundary

**Which two labels:** `question` vs `evidence_based`

**The decision rule I used every time:** If a post asks others for help, label it `question`, even if it contains test data.

**Supporting rules:**
- A closing "thoughts?" does not count as asking for help; label by the body.
- News posts are `evidence_based` only if they include an official link.
- Judge only by the post's text. Evidence that appears only in an image does not count.
- A post that asks readers specific questions to decide what to build next (feature requests, feedback) counts as asking for help → `question`, even if it includes an official link.
- A self-reported result number (e.g. "~90% on my eval set") counts as evidence, even if the data is private.
- Test conditions without any result (number or output) are not evidence → `unsupported_claim` if the post makes a judgment.
- Asking for help = asking about the poster's own specific problem or choice ("which quant should I try?", "how do I fix this?"). Asking for opinions ("what do you think?", "anyone agree?") is not asking for help; label by the body.

---

## The Dataset

**Where the posts came from:** r/LocalLLaMA. I gathered post links from the New feed, Top (month), and searches for "t/s" and "benchmark" (the searches were to find more evidence-heavy posts). Post text was fetched from the Arctic Shift public Reddit archive with a script. 196 posts saved; 4 skipped (3 duplicates, 1 missing from the archive).

**How I labelled them:** I labeled the first 20 posts cold, with no AI help (marked `cold` in the note column). An AI pre-labeled the other 176 using my definitions and rules (marked `prelabeled`). I then reviewed all 176 and changed 0 of them.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| evidence_based | 76 | 39% |
| unsupported_claim | 60 | 31% |
| question | 60 | 31% |

**Hard cases:**
1. "Model / harness combination: what works best?" — the benchmark results were only in an image; the text was just opinions. → `unsupported_claim`, and I added the rule that evidence only in an image doesn't count.
2. "Hot take: frontier models haven't actually become much smarter" — long argument that ends by asking whether others agree. → `unsupported_claim`: asking for opinions isn't asking for help, so I labeled by the body, which has no evidence.
3. "RustingStrata has a new built-in chat page. What is missing?" — has an official repo link (evidence) but also asks readers specific questions about what to build. → `question`, and I added a rule that specific feature-request questions count as asking for help.
 

---

## The Training Run

**Starting model:** distilbert-base-uncased

**Device:** CPU

**Settings:** notebook defaults — 3 epochs, learning rate 2e-5, batch size 16, max 128 tokens per post, seed 42. I changed nothing.

**Split:** 136 train / 30 val / 30 test. Test split per label: evidence_based 12, unsupported_claim 9, question 9 (all at least 8).



---

## How I Used AI

**Moment 1**
- *What I asked for:* I asked an AI browser assistant to find 3 clear example posts for each of my labels.
- *What came back:* 9 posts with labels and reasons.
- *What I changed:* I found 3 of them weren't clear (evidence only in an image, a closing opinion question, a feature-request post). I made them hard cases and added rules for each.

**Moment 2**
- *What I asked for:* I asked Claude Code to write a script to fetch post text from my list of links.
- *What came back:* The first request failed with HTTP 403.
- *What I changed:* I let it add an honest User-Agent naming this as a student project. The script then saved 196 posts.

**Moment 3 (unit 6)**
- *What I asked for:* I asked Claude Code to list every `evidence_based` row with the exact quote it saw as evidence, without changing any labels.
- *What came back:* 1 row with no evidence at all, plus about 20 weak rows (only a link, or someone else's numbers).
- *What I changed:* I read the 21 flagged rows and decided each one myself: 16 relabeled, 5 kept. This is how the AI helped me spot the pattern in my own errors.

**Moment 4 (unit 6)**
- *What I asked for:* I asked Claude Code whether results_three_seeds_before.json could measure my criterion 5 (confidence ≥ 0.8).
- *What came back:* It couldn't. The file stores only thirds, and the mean confidence was about 0.40.
- *What I changed:* I revised criterion 5 underneath the original in criteria.md, keeping the same 0.90 bar.

**Pre-labelling disclosure:** Rows 21–196 were pre-labeled by Claude Code using my README definitions and rules. I reviewed all 176 and made 0 corrections. Rows 1–20 were labeled by me with no AI.In unit 6 I re-checked the `evidence_based` rows and relabeled 16 of them, including 2 from my cold 20 (see The Improvement).



<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.300 | 0.567 | +0.267 |
| Macro F1 | 0.162 | 0.497 | +0.335 |
| F1 — `evidence_based` | 0.000 | 0.667 | +0.667 |
| F1 — `question` | 0.486 | 0.462 | -0.025 |
| F1 — `unsupported_claim` | 0.000 | 0.364 | +0.364 |

**What I predicted before I looked:**
I predict the trained model will beat the baseline most on `evidence_based`, because it saw 76 examples of that label during training, while the baseline scored 0 on it using only my definitions.

**What the gap actually means:**
Training helped overall (+0.267 accuracy), almost entirely by learning `evidence_based` and `unsupported_claim`, which the baseline got 0 on. On `question` it added nothing (-0.025): help requests are easy to spot from the wording, so the untrained model already did as well.



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.75 | 0.567 | 0.533 | 0.533 | MISSED |
| 2. Every label F1 (lowest) | ≥ 0.70 | 0.364 | 0.000 | 0.364 | MISSED |
| 3. Largest label share of labels.csv | ≤ 50% | 39% | 39% | 39% | MET |
| 4. Agreement with staff labels | ≥ 90% | 90% (one check, not seeded) | — | — | MET |
| 5. Most-sure third accuracy (revised) | ≥ 0.90 | 0.900 | 0.700 | 0.800 | MISSED |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted | evidence_based | unsupported_claim | question |
|---|---|---|---|
| **evidence_based** | 12 | 0 | 0 |
| **unsupported_claim** | 6 | 2 | 1 |
| **question** | 6 | 0 | 3 |

**My biggest off-diagonal number, and what it means:**
6 real `unsupported_claim` posts were called `evidence_based`, and 0 went the other way (the same happened to 6 `question` posts). The model leans hard toward `evidence_based`: it seems to react to technical words like model names and hardware, not to whether the post actually shows a checkable result.



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Overall accuracy | ≥ 0.75 | MISSED | All three seeds (0.533-0.567) are below 0.75. |
| 2 | Every label F1 | ≥ 0.70 | MISSED | `unsupported_claim` was 0.364, 0.000, 0.364; `question` was 0.421-0.571. Only `evidence_based` came close (0.649-0.667). |
| 3 | No label above 50% | ≤ 50% | MET | Largest label is `evidence_based` at 39%. A dataset property, the same for every seed. |
| 4 | Agreement with staff | ≥ 90% | MET | 27/30 = 90%, exactly at target. Measured once; not seed-dependent. |
| 5 | Most-sure third accuracy (revised) | ≥ 0.90 | MISSED | Hit 0.90 on seed 42 only; 0.70 and 0.80 on the others. |

**Diagnoses**

**Criteria 1 and 2 (accuracy and per-label F1):** mostly a labeling problem at the `evidence_based` boundary, plus small test counts. My confusion matrix shows 12 of the 18 non-`evidence_based` test posts were called `evidence_based`, and 0 went the other way. My agreement report backs this up: all 3 of my disagreements with staff were pile (a), and 2 of them came from treating any number as evidence. If I did that on the staff set, I likely did it in my own 196 labels too, so the model learned "numbers or technical words = `evidence_based`". `unsupported_claim` also has only 9 test posts, so one or two misses swing its F1 a lot, which explains the 0.000 on seed 7.

**Criterion 5 (confidence):** the model is barely confident at all. Its mean confidence is about 0.40, only a little above the 0.33 of random guessing among three labels. With 196 examples and inconsistent labels at the main boundary, the model never got sure enough for its "most confident" predictions to be reliably right.

---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** 27 / 30 = 90%

**Disagreements**

**1.**
> *The post:* "Times are down about 3% since the shoe rules changed, so obviously the shoes are the whole story and the sport has a problem."
>
> *Staff said / I said:* `hot_take` / `analysis`
>
> *My call, and why:* Staff is right. The author reaches the conclusion first ("so obviously"); the 3% is decoration, not the reason. Rule 1 says the fact must carry the argument.
>
> *Which pile:* (a) — the rule covered it and I applied it loosely.

**2.**
> *The post:* "Wind was so bad on the out section I was leaning at about 20 degrees. Coming back felt like cheating."
>
> *Staff said / I said:* `reaction` / `analysis`
>
> *My call, and why:* Staff is right. "About 20 degrees" is the writer's own estimate, not a checkable fact, and it doesn't argue anything. The post reports what just happened to the writer and how it felt ("felt like cheating"). Rule 3: without a load-bearing checkable fact, it isn't analysis.
>
> *Which pile:* (a) — the rule covered it and I applied it loosely.

**3.**
> *The post:* "Just realised the shoes I set every PB in this year are the ones I bought by accident in the wrong size."
>
> *Staff said / I said:* `reaction` / `hot_take`
>
> *My call, and why:* Staff is right. The post is about the writer's own discovery ("Just realised... I set... I bought") and makes no general claim about the world. Rule 2: about the writer means reaction. I marked this one "?" while labeling.
>
> *Which pile:* (a) — the rule covered it and I applied it loosely.

**What the pattern in my disagreements tells me:**
All three are pile (a): clear rules that I applied loosely. Two of the three (#1, #2) came from treating any number as evidence. That is the same mistake my model makes: it calls 6 `unsupported_claim` and 6 `question` posts `evidence_based`. This suggests my own 196 labels may also have called some posts `evidence_based` just because they contained numbers or technical terms, so part of the model's confusion is likely a labeling problem, not just a model problem.
---

## The Improvement

**What I changed:** I re-checked every row labeled `evidence_based` (76 rows) against my own rule: a post needs a checkable *result*, not just numbers, model names or technical words. An AI listed the quote it saw as evidence for each row and flagged 21 weak ones; I read those 21 and changed 16 (13 → `unsupported_claim`, 3 → `question`). Nothing else changed. New counts: evidence_based 60, unsupported_claim 73, question 63. Two of the changed rows (11 and 18) were from my cold-labeled 20, so I made this mistake even without AI help.

**Which diagnosis pointed at it:** The confusion matrix sent 12 of 18 non-`evidence_based` test posts to `evidence_based`, and my agreement report showed 2 of my 3 disagreements came from treating any number as evidence. Both pointed at the `evidence_based` boundary in my labels.

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.75 | 0.567 | 0.533 | 0.567 | MISSED |
| 2. Every label F1 (lowest) | ≥ 0.70 | 0.286 | 0.167 | 0.000 | MISSED |
| 3. Largest label share of labels.csv | ≤ 50% | 37% | 37% | 37% | MET |
| 4. Agreement with staff labels | ≥ 90% | 90% (unchanged) | — | — | MET |
| 5. Most-sure third accuracy (revised) | ≥ 0.90 | 0.700 | 0.800 | 1.000 | MISSED |

**Did it help, and how do I know:** Not overall. Accuracy barely moved (0.533–0.567 before and after), and macro F1 rose only slightly on two seeds and fell on one. The relabel fixed the problem I aimed at: `evidence_based` F1 rose to 0.588–0.737 and `unsupported_claim` to 0.621–0.667, and the seed-42 matrix now sends only 2 posts to `evidence_based` by mistake instead of 12. But the bias moved instead of disappearing: 7 of 10 `question` posts are now called `unsupported_claim`, and `question` F1 fell to 0.000–0.286. One caveat: changing labels also changed which posts landed in each test split, so before and after were not scored on exactly the same posts.

---

## What's Still Broken

**Criterion 1 (accuracy ≥ 0.75) — still missed (0.533–0.567).** Next I would add about 30 more posts for whichever label is weakest, labeled with the same care, because 196 posts with 9–12 per label in each test split is too few to separate three overlapping labels. I stopped because the unit allows only one change, and I used mine on the relabel.

**Criterion 2 (every label F1 ≥ 0.70) — still missed; the weak label moved from `unsupported_claim` to `question`.** Next I would re-check the `question` / `unsupported_claim` boundary the same way I re-checked `evidence_based`, especially posts that ask a question but are mostly opinion. I stopped for the same reason: one change per unit.

**Criterion 5 (most-sure third ≥ 0.90) — still missed (0.7, 0.8, 1.0).** Each third is only 10 posts, so one post moves the score by 0.1. I'd need a bigger test set before this number means much.

**The gap between what I meant my labels to capture and what the model learned:**
I meant my labels to capture whether a post shows a checkable result, asks for help, or just gives an opinion. The confusion matrices show the model instead learned surface signals, first "numbers and technical words = `evidence_based`", and after my relabel "no numbers = `unsupported_claim`", which pulled in 7 of 10 `question` posts.

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
