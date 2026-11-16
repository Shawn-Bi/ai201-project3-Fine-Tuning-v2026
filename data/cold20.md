1.
Someone should do an analysis on the rate of Self-promo here.
I think the last 3 posts from here that showed up on my feed were barely veiled self-promos.

I was here when huggingface first started getting popular, and the level of support for running local models here was incredible.

Now I am debating whether or not to leave the sub.  Why isn’t there more attention to moderation to this?  

Take a user’s post, and type their username with quotes into google and then type whatever obscure tool they’re asking a question or talking about and you’ll see the absurd rate or Astro-turfing and shilling.  

They will post here and 6 other LLM places, but this place used to be awesome, so I only care about this sub.  

LABEL: unsupported_claim

2.
Model / harness combination: what works best?
https://i.redd.it/fgy9ko2sku1i1.png

If you are wondering what model / harness combination works the best, here are my findings so far:

1) Model is way more important than the harness, best so far Qwen Flash Next even with low quant outperform Qwen 3.8 27B

2) The inference engine is way more important than the harness, because the size of the context windows can dramatically increase performance. AND because speed make the difference between something useable and something that won't work.

3) Harness optimised for coding like OpenCode or PI outperform more generic agent like OpenClaw and Hermes, even on mondane task like reading emails, making purchase on a store or  complex vision.

LABEL: unsupported_claim

3.
Best direction to go for my setup EPYC 32core + 512GB DDR4 + 44GB GPU ?
Just looking for some advice on what is possble with my setup and speeds I should be gettingI know it won't be super fast tps but I was more after getting the bigger models to run.

This is my spec:

Epyc 7502p - 32 Core  
Gigabyte MZ32-AR0 - 8 channel memory  
512GB DDR4  
1x 4070 12GB  
2x 5060 16GB

quite a few implementations which can I confusing.  
Is this build even useful now? that we have Project Maya which you can stream from the NVME drive?  
  
Anyone have similar setups and what to expect, what software best to use

LABEL: question

4.
Another reminder of the low intelligence of local models
(Note: by local models I mean anything smaller than Deepseek 4.1)

I already gave up on local models for coding tasks 6 months ago, due to what I perceived was intelligence too low for the tasks I give it. I made a post about it on here back then and it was a huge discussion, I think 800 comments. I went against the /r/LL orthodoxy and many didn't take my comments well, but we can agree to disagree.

Since then I only use local LLMs for translation and ComfyUI prompt enhancement. I stick to big cloud models for coding. I think the electricity cost of running Qwen 27B alone exceeds what you'd pay Deepseek to use their cloud API in their own harness, and you'd get a far more intelligent and far faster model.

But this post isn't about the economics. It's purely about ability. I still see people commenting in favor of buying GPUs for local intelligence. "Sonnet at home" is a ridiculous phrase I've seen more times than I should in relation to Qwen 27B.

**The simplest of tech tasks is still too hard to one-shot**

I keep Qwen 3.8 27B running on my Spark for occasional non-coding stuff. Today I gave it a trivial coding task I needed for my server, just out of curiosity.

- llama-server launched with `--model Swift-1.5-Qwen3.8-27B-Q4_K_L.gguf --reasoning on --reasoning-effort xhigh`
- Open llama webpage and leave Reasoning at Default, leave system prompt empty
- Prompt: 

    Give me a bash script that will list all files in directory sorted by date. Output should be:
    2025-12-31 12:13:14 file1.ext
    2025-12-31 12:13:14 subdir/file2.ext

1630 tokens later, most of it reasoning, I get a script. When I run it, here's the output, as you can see the timestamp is wrong:

    2026-10-16 20 tmp.59eH9w3JLe
    2026-10-17 20 tmp.5xvczTbSS4
    2026-10-18 20 tmp.nWOEDw2wlu
    2026-10-20 20 tmp.JVEZIFfKx3
    ...

I then tried Gemma 31B Reasoning on duck.ai. The output only showed the timestamps, no filenames!

This is the most trivial of coding tasks (the answer is a 3-5 lines script), using the most ancient and commonly-available training data (bash), on the most praised local coding model on this sub (Qwen 27B), at a recommended/popular quantization (Q4), and it still can't one-shot this. The 2nd most popular local model, Gemma 4 31B, also fails.

(Editor's note: I think my post could've ended here, in a "Ecce homo" way, but I went on for a few more paragraphs)

**Weak local LLM + software development = bad time**

I'm sure if I had run this task with your average agent harness with a system prompt that makes it test its code, it would run the script it created, see the issue, then get it right on the 2nd attempt. But while I think this "try until you succeed" workhorse approach is acceptable for small self-contained coding tasks, I don't think anyone should be doing any serious coding this way.

If you're writing something you intend to maintain over time (ie not a one-shot), or that you will be sharing with other people, you need a higher degree of LLM intelligence and knowledge to create it. A strong LLM will be able to avoid entire classes of problems from the start, when designing the app. From design to implementation to maintenance, it will make better decisions every time and without laboring its way to them, resulting in a codebase that is smaller, well-designed, more easily modifiable, less buggy, and developed in a fraction of the time.

Coding with local LLMS is like insisting on using a donkey for transportation in the age of cars. It can be done for fun, but it shouldn't be done seriously.

**Sonnet at home my ass**

Btw I've seen several people say Qwen 27B is like having a local Sonnet 4. The benchmarks say it's even better than Sonnet 4, actually. So I went on openrouter.ai out of curiosity and gave the same prompt to 3 models.

- Sonnet 4.5 (oldest Sonnet I could find): one-shots it
- GPT 4.1 Mini, which was comparable to Haiku 3.5: one-shots it
- GPT 4.1 Nano, which is even worse than Mini: one-shots it

**Weak local LLM + Linux server management = even worse time**

This post's getting long so I'll just speedrun this part.

- Managing an OS is actually harder tasks that LLM struggle even more with. And the stakes are higher because you don't want your server to go down.
- I used to never trust LLMs enough to let them onto my server, I'd just ask for something, copy-paste the command, report back, repeat. A huge waste of my limited free time. Now I just rawdog a frontier model on the server. Although I have it avoid making any changes without my supervision, Docker is a big benefit here for both organization and safety/stability.
- Even top models won't one-shot a task like "I want to install and run https://github.com/rando/something on this system in a Docker container in /opt/docker/something/. Create the Dockerfile and docker compose file", especially for AI-related tools, where having the right CUDA, not having python wheels for my server's ARM CPU, etc, introduces a lot of failure opportunities. When I had Claude five months ago, even it struggled to get these right.

Thanks for reading my wall of text. Downvotes to the left.

LABEL: evidence_based

5.
BigMoeOnEdge outperforms Strata and colibri on 8-16 GB cards and Mac and you can run any model
Hi!

for those who might not know the solution:

\- it takes any MoE GGUF llama.cpp can load, whatever the quant. No repacking, no special format

\- it runs on whatever you have: NVIDIA, AMD, Intel, Mac, a phone, or just the CPU

\- Windows, Linux, macOS, Android, iOS

\- output is the same as llama.cpp, don't cut corners on quality

\- you start it with \`--auto\` and it works out the settings for your machine

Below is a brief overview of the benchmark:

\- 8 GB card, Qwen3.6-35B: I get about 35 tok/s. colibri around 23. Strata wouldn't start at 16k context

\- 12 GB card, same model: about 45 for bmoe, about 30 for Strata

\- long prompt on the 8 GB card: bmoe 5 s to the first token. Strata 14 s, colibri close to 2 minutes

\- Basalt needs an RTX 50, so I couldn't run it on these

16 GB MacBook, Qwen3.6-35B: about 20 tok/s for bmoe, colibri's release 3.5

\- same Mac, Qwen3.8-Flash-Next 125B: 10 tok/s, Strata about 7

On the cards Strata is tuned for it's still ahead but only by a little.

On two 5060 Ti with Qwen3.8-Flash-Next it was 1.3x faster than bmoe. They write kernels for a handful of models, bmoe does not.

Repo, with the logs: https://github.com/Helldez/BigMoeOnEdge

If you have an 8 to 32 GB card I'd like to see what you get.

Benchmark: https://github.com/Helldez/BigMoeOnEdge/tree/main/docs/bench-data

LABEL: evidence_based

6.
I run a daily isekai guessing-game pipeline on a DGX Spark with Qwen3.6-35B-A3B (vLLM) and Qwen-Image (ComfyUI, fp8)
This is a hobby project, not a product pitch. I saw a TikTok where people rewrote famous movies and games as over-long isekai light-novel titles, and I wanted to see how far I could take that with local models. The game is at https://itsisekai.com. Five quests a day, guess the original.

**Hardware.** NVIDIA DGX Spark (GB10, 20 Arm cores, 121 GB unified memory), set up as a self-hosted GitHub Actions runner. A nightly workflow (or a manual run) runs the pipeline on the same box as the models. No API fees for generation.

**Models.**

- Text and judge: Qwen3.6-35B-A3B, official FP8 build, served with vLLM (OpenAI-style API). fp8 KV cache, 128K context, MTP speculative decoding with 3 draft tokens, prefix caching, and 45% of GPU memory so ComfyUI fits beside it. The judge is the same model, and thinking is left on. Generation runs about 70 tok/s typically, peaking around 240 tok/s.
- Images: Qwen-Image in ComfyUI with the official fp8 weights (`qwen_image_fp8_e4m3fn` + `qwen_2.5_vl_7b_fp8_scaled` encoder), 832x1248, 20 steps, cfg 2.5, euler/simple. One render takes about 64 seconds (around 3.15 s per step).
- I had to drop vLLM `--gpu-memory-utilization` from 0.80 to 0.45 so ComfyUI fits beside it.

**Pipeline.** It fills missing quests for the next several days. All missing titles are written first, one at a time, so later quests can see the answers already picked. Then covers are drawn. A day is only saved when all its quests succeed, so the site never shows a half-filled day.

For each quest the model writes the answer, hints, a 10-40 word title that can't contain the answer, and an art prompt. A second "how obvious is this title?" check can send it back for a rewrite. The cover is judged on the image alone: if the model can name the work, the prompt is rewritten more abstractly and redrawn, up to 3 times. If every try still gives it away, the cover stays sealed until the player finishes the quest.

**Timings** from a production run on Nov 15 (8 quests across 2 days, 0 failed). The whole run took 61 min 29 s.

- Titles, including the obviousness check and rewrites: 2 min 14 s to 6 min, average 4 min 26 s. Four of the eight were first judged too obvious and rewritten.
- Cover attempts, draw + judge together: 1 min 38 s to 3 min 34 s, average 2 min 23 s. About 64 s of that is the render; the rest is the vision judge thinking about whether it can guess the work.
- The judge passed 8 of 10 cover attempts. Two covers gave it away on try 1 and passed on try 2. None had to be sealed.

**What went wrong.** vLLM's guided JSON didn't mix with Qwen thinking: requests could jam and loop until they timed out. I dropped guided JSON for Qwen and just parse the JSON out of the reply. Without a presence penalty, Qwen could also think in circles until it filled the context; I set `presence_penalty` 1.5 and `max_tokens` 16384. One failed model call used to wipe out a whole day; now it retries and moves on. I also learned not to overlap manual workflow runs with the nightly cron.

Happy to answer questions. I'm not selling anything, I just thought the timings and the "don't use guided JSON on a thinking Qwen" bit might be useful.

LABEL: evidence_based

7.
1Cat-vLLM vs Strata
Everyday we see posts about speeds on Strata and its forks, but just recently I came to know that 1Cat has added support for expert caching recently, like a month ago. So I did (asked claude) a comparison of speeds on a Qwen3.8-Flash-Next UD-IQ3_XXS quant. My rig is 4x 16gb Tesla V100 on PCIe 3 x16 links, with 8 channel 3200 mt/s ddr4 ram, Epyc 7543 CPU. Now, for numbers:

## Single stream

Median of 3 runs, except the 97k tokens one which I asked to run only once to save time.

| Prompt (tokens) | Prefill tok/s, Strata | Prefill tok/s, 1Cat | Decode tok/s, Strata | Decode tok/s, 1Cat | MTP acceptance, Strata / 1Cat |
|:--|--:|--:|--:|--:|:-:|
| 2,654 | 861 | **1,850** | 74.8 | **124.9** | 0.61 / 0.45 |
| 8,674 | 1,146 | **2,483** | 79.3 | **140.8** | 0.67 / 0.66 |
| 30,299 | 2,480 | **2,776** | 76.4 | **139.3** | 0.63 / 0.58 |
| 96,588 | **3,384** | 2,649 | 77.2 | **142.6** | 0.72 / 0.62 |

Strata has better draft acceptance and still 1cat beats it, imagine if 1cat could get better draft acceptance.

## The same 103K-token prompt three times

Same prompt, 3 times in a row, just different enough to not trigger prefill cache.

| Run | Decode tok/s, Strata | Decode tok/s, 1Cat | Prefill tok/s, Strata | Prefill tok/s, 1Cat | MTP acceptance, Strata / 1Cat |
|:-:|--:|--:|--:|--:|:-:|
| 1 | 70.8 | 99.9 | 3,398 | 2,736 | 0.65 / 0.60 |
| 2 | 78.9 | 138.4 | 3,340 | 2,752 | 0.71 / 0.60 |
| 3 | 77.8 | 123.5 | 3,348 | 2,751 | 0.69 / 0.57 |
| run 1 to 3 | +10% | +24% | - | - | - |

LABEL: evidence_based

8.
MoE offload on a 3090: prefill 345 -> 466 t/s by tuning cudaMemcpy (Qwen3.6 35B-A3B)
https://i.redd.it/5dlnj6wict1i1.gif

    I made a tool that tunes copies that speeds up CPU offloading.
    
    1 3090 + 7800X3D
    
    llama-bench -m Qwen3.6-35B-A3B-Q8_0.gguf -ngl 99 -fa 1 -ot exps=CPU -p 2048 -n 0 -r 3
    
    cmt tune -- llama-bench -m Qwen3.6-35B-A3B-Q8_0.gguf -ngl 99 -fa 1 -ot exps=CPU -p 2048 -n 0 -r 3
    
    before: prefill 345 t/s
    after: prefill 466 t/s
    
    
    blog: https://maknee.github.io/blog/2026/CudaMemcpy/
    code: https://github.com/Maknee/cudamemcpy-tuner

LABEL: evidence_based

9.
Is there a community about finetuning and training models?
There seems to be a lot of discussion here about inference and using the models, but is there anywhere where discussion about making them is more common?

LABEL: question

10.
Probable GLM model
https://i.redd.it/k7ife2j2ms1i1.png

Because of Theo gg tweet of all people,   
I Launch QFN DeepResearch swarm agent to find anything about this.

**THREE** model names, blurred out, sitting at 59.4% / 57.1% / 54.0%.  


1. The blurred names are most likely **\[GLM-Nano or GLM-Name\]** Pro, Med, and Small**.** One community experiment reconstructed the suspected text, applied Gaussian blur (σx ≈ 6.9px), and achieved an RMSE of just 1.254/255 against the original. 
2. AICodeKing track record.  Someone compared his previous GLM statements against official release dates: GLM-4.6 (same day), GLM-5 (1 day), GLM-5.1 (11 days), GLM-5.2 (3 days), and GLM-5.3 (4 days).
3. Antrhopic timing. The leaderboard surfaced on November 12 vs AICodeKing timing, while Anthropic IPO on Nov 18. If [Z.ai](http://Z.ai) releases GLM-Nano this week, the timing would make for quite a coincidence

[https://linux.do/t/topic/3166447](https://linux.do/t/topic/3166447)

Another strong signal is HF activities, i know it is not bullet proof, just another signal, 3-4 days compare to last 27 days

https://i.redd.it/oa0ix3vpls1i1.png

Yes Stylobot i use LLM to fix my grammar.  
Since it is speculation and not actual open model this post has a high probability to be removed, so yeah

LABEL: unsupported_claim

11.
ISTA Qwen3.8 27b on 3060 12gb
Hey guys 

I am a seasoned local llm user and I ain't quite ram rich like only 16gb ddr4 🥀

So I can't run qwen3.8 flash next on my 3060 

This guy felt the best for me yet 

Have you guys tried it 

I have ran iq3\_xss quant non mtp with turboquant at 65k context completely on my 3060 though I did offload mmproj to cpu ram 

Have guys tried this it really felt like a blessing to my life using the peak of local ai on my 3060 

It seriously packs the punch 👊 I was able to perform various of my agent task complete on device not like simple but the ones which require actual reasonings 

Here is my cmd if you want to see

llama-tq serve -m "E:\\MODELS\\ISTA-DASLab\\Qwen3.8-27B-GSQ-RCO-GGUF\\Qwen3.8-27B-GSQ-RCO-IQ3\_XXS.gguf" --mmproj "E:\\MODELS\\ISTA-DASLab\\Qwen3.8-27B-GSQ-RCO-GGUF\\mmproj-Qwen3.8-27B-BF16.gguf" --no-mmproj-offload -ngl 99 -c 65536 -ctk turbo4 -ctv turbo3 -ub 256 -b 2048 -t 3 -tb 3 --reasoning-budget 256 --reasoning-preserve --alias Qwen --port 8080 -lm none

Sources: for my recipe

ISTA-DASLab/Qwen3.8-27B-GSQ-RCO-GGUF

https://huggingface.co/ISTA-DASLab/Qwen3.8-27B-GSQ-RCO-GGUF/discussions

Turboquant

https://github.com/TheTom/llama-cpp-turboquant

Pi coding agent

https://pi.dev/

I would like know the communities views and any suggestions would be welcome 🤗

Thankyou for your time 

LABEL: evidence_based

12.
Ninfer and GGUF of Qwen3.8-27B-UD-Q3_K_XL ASCII-Condensed
Hi,

I've put on HF a condensed version of Unsloth Q3\_K\_XL [ASCII-Condensed](https://github.com/bsaleh03/ASCII-Condensed-prune-tools) from bsaleh03 with only ASCII + Latin-1 / Latin-Extended-A (P2) to use with a 16GB VRAM GPU.

I created a GUFF version and also a ninfer to be used with [ninfer-all](https://github.com/iamwavecut/ninfer-all/)

To create the ninfer version I had put up some helper conversion scripts and modify iamwavecut conversion scripts due to different vocabulary size.   
In the HF repo [https://huggingface.co/fakezeta/Qwen3.8-27B-UD-Q3\_K\_XL-Condensed-P2](https://huggingface.co/fakezeta/Qwen3.8-27B-UD-Q3_K_XL-Condensed-P2) there is  what is needed to replicate it and I also submitted a PR to the upstream repo.

Quality: IFEval result 84,4% vs 83,9% of base model (Instruct, 1 run) so within STD Deviation error.

With this I achieved 75K context with rk8v4 kv type with an average of about 60tok/s in the 541 IFEval samples on my 5060Ti 16GB.

I'm also planning to create a light GGUF and ninfer version with the lower quantized MTP released separately by Unsloth in their repo to save about 90MB of RAM for other context.

LABEL: evidence_based

13.
I used local Gemma 4 to moderate a community and it was it is promising
I run a couple of small communities and it's becoming difficult to moderate them all. So today I built a script on top of my existing app which I use to track the content on those communities.

The script does a few things based on where I am. So I store the general notes of my communities in a dedicated place I can easily query.

And in the moderation panel I go through each of the item which needs moderation and I run them through my notes and let Gemma 4 decide whether the item is following community notes or not. If Gemma thinks it's not, then my script will remove the content from public and add a reason as well.

At first I had tried GPT oss 20b model which was really faster but the results were not really good. Then I ran the same process through Gemma 4 with thinking enabled. Results were good but speed was extremely slow. So I tried with thinking disabled and I did not see any noticable drop in the results.

Now soon I will try to run the same thing at scale and see if the results are generally accurate and if they are, I might ship this tool with my friends.

I agree, the setup is quite tough and I've managed to run it properly on my network. If I have to share this with other people I may need to host the model somewhere and check if it can be scaled to a bigger number of requests per hour.

Anyways it was a really good experience. Especially when I had to build it on top of my existing app.

Just thought I'd share this small win over here

LABEL: unsupported_claim

14.
Latest version of strata made my Qwen3.8-Flash-Next dumb and useless
I updated the strata to the latest version from v0.1.42.0, so I can try the latest unsloths models and see how they fare against the iq3\_s variant I have been using. Upon updating it, I noticed it messed up the whole thing, It got faster, but it got way dumber! previously it would only take 15\~30 minutes to create the pagoda , 50 mins to an hour if I used xhigh. 

But when I siwtched to the latest version, not only it takes at least an hour and half to come up with something, its not even done! and it has many issues! 

[0.1.42.0](http://0.1.42.0) is the last version that seems to work decently. 

I noticed, when im using the latest model, it always tries to go for something grandiose and failing. unlike the older version which seems to take a more modest path! 

whats going on? Do any of you have this problem? 

here are example outputs I did to make sure its not a one time thing! 

my prompt : 

Design and create a very creative, elaborate, and detailed voxel art scene of a pagoda in a beautiful garden with trees, including some cherry blossoms. Make the scene impressive and varied and use colorful voxels. Add as many details as possible to showcase your attention to them. Use whatever libraries to get this done but make sure I can paste it all into a single HTML file.

  
these are the outputs : 

[0.1.42.0](http://0.1.42.0) : 

xhigh: 

![img](hbwsi2vj5r1i1 "xhigh-1")

![img](c7h8vspq5r1i1 "xhigh2")

![img](823v96oa6r1i1 "xhigh3")

![img](ilaf1foe6r1i1 "xhigh4")



default: 

![img](g9z06cvx5r1i1 "default1")

![img](f7ayt9126r1i1 "default2")

![img](ie20z5kk6r1i1 "default3")



![img](6vdbnwvq6r1i1 "default4")

  
the latest version created this after 1 hour and 32 minutes to only fail with excessive thinking:

![img](c1jdlx947r1i1 "xhigh")

![img](4jag7e5mnr1i1 "default(failed after 1 hour and 31 minites exausting all context size of 262K)")

As you can see, not only it takes way longer to create an output, if it doesn't fail already, the attention to details is also gone, everything is in haphazard form! I tried 4 5 times and the majority all failed because it couldn't create an output after an hour and a half or it constantly gets something wrong and tries to either fix it or goes to look at other things leaving the issues untouched! 

The model at least, the qwen3.8-Flash-Next-q3\_s that I have been working with so far is not usable! it takes too long and it fails more by getting stuck at thinking forever! 

I used the new unsloth quant iq4\_xs too and it was a mess as well. so I figured its the strata version. sadly I cant test the iq4\_sx on [0.1.42.0](http://0.1.42.0) and I get an error. 

So if any of you faced this issue, can you kindly share with me what you do to fix this? what version does it work for you? 

I have RTX3080 10G/ 64G of RAM and I'm using the Linux terminal version along with deepseek harness.

Thank you all in advance

LABEL: question

15.
Placing an implant into AI brain with Lazarus: Anatomy of a trojan
hello there, I recently got a bit fascinated about Lazarus from Microsoft (even tho it is probably old technique) and I wrote a blog post showing a thought process I had while researching it - maybe it is helpful to anyone   
  
[https://int8.io/implanting-ai-with-lazarus/](https://int8.io/implanting-ai-with-lazarus/)

https://i.redd.it/pt7hjyffcr1i1.png



LABEL: unsupported_claim

16.
Best sub 80b total or 6b active MoE for document intelligence?
I'd like to make a pipeline capable of understanding pdfs of bank statements and then group expenses by categories etc. My thought was to first parse them with ocr into .md files and then feed that to a text model. I think it's more lightweight and accurate this way. But then I'm not sure what model to use to feed all these md files to get something good. When accuracy matters, should I go for qwen, gemma, lfm, or something else? Thank you for your help! 

LABEL: question

17.
How many of you started using AbliteratedOutTheBox(or similar options) apart from downloading Abliterated models? How is it?
Myself saved more than bunch of **medium** sized Abliterated/heretic/Uncensored/Decensored/etc., models. Ex:

* Qwen3.8-27B
* Qwen3.6-35B-A3B
* Gemma-4-31B
* Gemma-4-26B-A4B
* Muse-Glimmer-30B

But when it comes to **big**/**large** sized models, requires at least 100+GB downloads & also HD Space for each models additionally. MiniMax-M3.1-Flash

* DeepSeek-V4.1-Flash-1017
* NVIDIA-Nemotron-3.5-Super-VL-120B-A12B
* DeepSeek-V4-Flash-Vision-Exp
* GLM-5.3-Flash
* Qwen3.8-Flash-Next
* MiMo-V2.6-Flash-MOPD
* Step-3.7-Flash
* MiniMax-M2.7

AND

* Qwen4
* Gemma-5
* NVIDIA-Nemotron-4
* etc.,

I need to download above big/large models. Regular GGUF is must. For Abliterated version, I'm still thinking whether AbliteratedOutTheBox is enough or Abliterated GGUF is must. So what are you doing on this?

I hope that most of you aware of AbliteratedOutTheBox, here's threads related to that. 

* [Inference time abliteration](https://www.reddit.com/r/LocalLLaMA/comments/1xc1e9y/inference_time_abliteration/)
* [AbliteratedOutTheBox Strata Announcement](https://www.reddit.com/r/LocalLLaMA/comments/1xe8x9c/abliteratedoutthebox_strata_announcement/)

Do we have any other similar options like AbliteratedOutTheBox? Please share.

LABEL: question

18.
RASA will cause total chaos to open LLMs and beyond
Commerce Moves to Finalize Rule Blocking Chinese AI Firms From Renting Nvidia GPUs Abroad  
[https://explainx.ai/blog/commerce-final-rule-chinese-ai-firms-remote-nvidia-chips-the-information-2026](https://explainx.ai/blog/commerce-final-rule-chinese-ai-firms-remote-nvidia-chips-the-information-2026)  
House Passes Remote Access Security Act to Limit Adversaries’ Remote Access to Critical Technology  
[https://www.cmtradelaw.com/2026/01/house-passes-remote-access-security-act-to-limit-adversaries-remote-access-to-critical-technology/](https://www.cmtradelaw.com/2026/01/house-passes-remote-access-security-act-to-limit-adversaries-remote-access-to-critical-technology/)

# H.R.2683 - Remote Access Security Act

[https://www.congress.gov/bill/119th-congress/house-bill/2683](https://www.congress.gov/bill/119th-congress/house-bill/2683)

LABEL: evidence_based

19.
Do we want Huang back?
There's a petition floating around out there to put Jensen Huang back at the helm of nVidia.  Currently it has over 129,000 signatures.  If you want to sign it, you can find it pretty easily.

But do we want him back?  He's pro-local, but he's also completely driving the circular-financing game that's detonated prices for all of us, everywhere, for fucking everything.

How likely is it the nVidia board hires someone pro-local and smart enough to not run the circular financing sham?  Thankfully the interim-CEO, Colette Kress, was against such money shenanigans:

> Colette Kress spent years as the one Nvidia executive willing to check CEO Jensen Huang’s enormous, ​often risky ambitions. ...
>
> Kress and her staff clashed with Huang and the company's sales team over the massive and risky financing deals that ⁠fed into what some Wall Street critics deemed a circular AI economy, including investments in OpenAI and AI infrastructure companies such as Lambda, according to one of the people familiar with the matter.

https://www.reuters.com/business/colette-kress-cfo-who-challenged-huangs-bets-is-nvidias-interim-ceo-2026-11-13/

That's significant.  Not only did she have the stones to deny the Huang, she's the only one to have them at all.

I think that petition can stuff it.  Keep Kress and let her run the show.

LABEL: unsupported_claim

20.
Normies, or the Standard Task Benchmark ???
Is there actually a benchmark for us normies who aren’t rocket scientists or mini-Eulers? Mathematically, we could describe it as a **95% confidence interval benchmark**. All models that reach the 95% threshold receive 100%. The goal would be to identify those models that we classify as “good enough” for us normies. If this could also be set in relation to costs—whether on-premises or in the cloud—it would also provide a measure of what AI really costs us **normies**.

LABEL: question

