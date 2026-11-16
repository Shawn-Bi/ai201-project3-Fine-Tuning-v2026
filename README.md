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

**Pre-labelling disclosure:** Rows 21–196 were pre-labeled by Claude Code using my README definitions and rules. I reviewed all 176 and made 0 corrections. Rows 1–20 were labeled by me with no AI.



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
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

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
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



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
