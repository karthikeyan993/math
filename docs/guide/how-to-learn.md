# How these lessons teach

Each lesson is built from techniques with solid evidence behind them. This page says what each technique is, what it looks like here, and where the evidence comes from. If a part of a lesson feels slow or effortful, it's probably on purpose. The research calls these *desirable difficulties* (Bjork, 1994): ways of studying that feel worse while you're doing them and work better a week later.

## The core loop

Every lesson runs the same cycle:

**try first → see it → name it → prove it → finish one yourself → recall it later**

| Step | What you do | Why |
|---|---|---|
| **Try first** | Answer a *Predict* box before you're taught the idea | Productive failure |
| **See it** | Play with an interactive visual | Concreteness fading, dual coding |
| **Name it** | Read the formal statement, with symbols explained right where they appear | Cognitive load |
| **Prove it** | Read a worked proof, explaining each line to yourself | Worked examples, self-explanation |
| **Finish one** | Fill in a proof with parts left blank, then write one from scratch | Fading, expertise reversal |
| **Recall it** | Answer *Check yourself* questions, then review flashcards spaced over days and weeks | Retrieval practice, spacing |

## The techniques

### Retrieval practice
Pulling an idea out of memory strengthens it more than reading it again. This is one of the most reliable results in learning science. Roediger & Karpicke (2006) found that testing beat re-studying on delayed tests, and Dunlosky et al. (2013) rated practice testing as one of only two "high-utility" study techniques.
**Here:** *Check yourself* questions are recall first, then reveal. Rate yourself honestly.

### Spacing
The same total study time works better split across days than crammed into one sitting (Cepeda et al., 2006, meta-analysis).
**Here:** every lesson comes with an Anki deck in `flashcards/`. The tutor also opens each session with a few questions from older lessons.

### Interleaving
Mixing problem types makes you practise *choosing the method*. Doing all the same type in a row lets you skip that choice (Rohrer & Taylor, 2007). In this course the hard part is often "which proof technique?", so this matters a lot.
**Here:** once a few lessons exist, the tutor's *quiz me* mode mixes them: induction, contradiction, well ordering, invariants.

### Productive failure
Trying a problem *before* you're taught how to solve it, and usually failing, then getting instruction, builds deeper conceptual understanding than instruction first. This holds especially when the instruction then builds on your failed attempts (Kapur, 2008; Sinha & Kapur, 2021, meta-analysis in *Review of Educational Research*). It helps conceptual understanding more than procedural skill.
**Here:** the *Predict* boxes. The courtyard lesson has you try the naive induction and watch it get stuck before you see the fix.

### Worked examples, then fading
Beginners learn more from studying worked solutions than from solving problems unaided (Sweller's cognitive load theory). Removing steps one at a time (*fading*) moves you from studying solutions to producing them (Renkl & Atkinson, 2003). Once you're fluent, worked examples stop helping and can even slow you down. This is the *expertise reversal effect* (Kalyuga et al., 2003).
**Here:** each lesson goes from a full proof to a proof with blanks to your own proof. If something is already easy for you, skip the worked example. That's the right call, not cutting corners.

### Self-explanation, especially for proofs
Learners who explain each step to themselves ("why does this follow?") understand much more than those who just read the steps (Chi et al., 1989). For proofs specifically, a short self-explanation training raised undergraduates' proof comprehension scores (Hodds, Alcock & Inglis, 2014). Their booklet reports students scoring 30% higher than a control group. Their method, used on every line of a proof:
1. What are the main ideas in this line?
2. Why does it follow from earlier lines, definitions, or theorems?
3. How does it connect to the goal?

Paraphrasing a line ("so we add n+1") doesn't count. The explanation has to say *why*.
**Here:** proofs come with "why is this line true?" prompts. The tutor's *check my proof* mode asks you to explain your own lines before it gives any feedback.

### Concrete → pictorial → abstract (concreteness fading)
Start with something concrete you can manipulate, move to a schematic picture, then to symbols. This transfers better than starting abstract or staying concrete (Fyfe et al., 2014, review).
**Here:** dominoes → staircase of blocks → $\sum_{i=1}^n i = \frac{n(n+1)}{2}$.

### Multimedia design
Words and pictures together beat words alone (Paivio's dual coding; Mayer's multimedia principles). It helps only if the picture sits *next to* the words it explains, highlights what matters, shows one step at a time, and has no decoration (Mayer, *Multimedia Learning*).
**Here:** visuals sit right beside the idea they show, the tiling solver steps through one recursion level at a time, and colours carry meaning (colour = recursion depth).

### Active beats passive (ICAP)
Engagement levels rank Interactive > Constructive > Active > Passive (Chi & Wylie, 2014). Watching an animation is *passive*. Predicting what it will do, or changing a parameter to test a guess, is *constructive*. Arguing with a tutor is *interactive*.
**Here:** every visual asks you to do something before it shows you something.

### Learning from wrong proofs
Finding and fixing errors in someone else's worked example builds understanding that correct examples alone don't (McLaren, Adams & Mayer, 2015, on erroneous examples).
**Here:** every lesson has a *Spot the bug* section, and the tutor can generate subtly broken proofs for you to debug. As a software engineer you already do this for a living.

### Teaching it back
Preparing to explain something, and actually explaining it, improves your own understanding (Fiorella & Mayer, 2013).
**Here:** the tutor's *teach-back* mode plays a sharp but confused student, and you explain the idea to it.

### Mastery before moving on
Bloom (1984) reported one-to-one tutoring with mastery learning about 2 standard deviations above conventional classes. A later review found much smaller effects for human tutoring, about 0.79 SD, with step-based computer tutoring nearly as good at about 0.76 SD (VanLehn, 2011). Mastery learning still matters, but don't expect 2 sigma.
**Here:** move on when you can do the *Check yourself* questions cold and write the lesson's proof without looking. Not when you've finished reading.

## Designed for you: an adult engineer coming back to maths

Most of the studies above were run on school or university students. The direction of the effects should carry over to you, but treat the exact sizes as rough. Below are the factors specific to your situation that changed the design.

| Your situation | What the evidence says | What we do about it |
|---|---|---|
| **15 years away from maths.** Algebra and notation are rusty | Anxiety about maths takes up working memory, and that hurts performance on exactly the hardest problems (Ashcraft & Kirk, 2001) | Low-stakes practice everywhere. Notation explained right where it appears, not front-loaded. A diagnostic drills only the gaps. Before a timed mock exam, an optional 10 minutes writing about your worries, which improved exam scores in classroom trials (Ramirez & Beilock, 2011) |
| **"I'm a visual learner"** | Matching teaching to a learning style has no good evidence behind it (Pashler et al., 2008). Combining pictures with words *does* help, and it helps everyone | The visuals are here because of dual coding, not a learning style. You still write every proof in words and symbols |
| **Experienced software engineer** | Prior knowledge is the strongest predictor of learning. Experts need fewer worked examples (expertise reversal). Building maths concepts by programming them has a long history in university maths education (e.g. Leron & Dubinsky, 1995) | Code is a second representation. You test a conjecture in Python before proving it. CS links appear only where they're real |
| **Full-time job, limited time** | Spacing helps (Cepeda et al., 2006), and sleep consolidates memory between sessions (Diekelmann & Born, 2010) | Short sessions on several days beat a weekend cram. The tutor schedules reviews |
| **Self-directed, no class** | Motivation lasts when you feel autonomy, competence and connection (Ryan & Deci, 2000). Growth-mindset pep talks show only weak average effects (Sisk et al., 2018) | You pick the path. Visible mastery comes from the progress log and passed checks. Explaining to someone else, or to the tutor, stands in for classmates. No motivational speeches |
| **Mid-30s** | Nothing in this literature suggests your age is the bottleneck. Time, fatigue and interruptions are. *(This is my reading of the evidence, not a cited finding.)* | Sessions designed to be paused and resumed, with the log as your save file |

## Attention: easily distracted, and building the muscle

You described mild, undiagnosed ADHD-like distractibility: you lose focus when something is uninteresting or runs too long, and you want to build stamina. I'm not qualified to diagnose anything, and none of this is treatment. If it's affecting your work generally, a professional evaluation is worth it. What follows is the learning-science side.

| Problem | Evidence | What we do |
|---|---|---|
| **Mind wandering in long explanations** | Short quizzes interspersed through online lectures reduced mind wandering, increased note-taking, and improved learning. They also lowered anxiety about the final test (Szpunar, Khan & Schacter, 2013) | Every few minutes a lesson asks you to *do* something: predict, recall, or drag. Lessons are split into **sittings of 10–20 min with checkpoints** between them, and every checkpoint is a fine place to stop |
| **Getting started, and getting back after drifting** | "If-then" plans ("*when* X happens, *then* I do Y") help people follow through on goals across many studies (Gollwitzer & Sheeran, 2006, meta-analysis). They also improved response inhibition in children with ADHD (Gawrilow & Gollwitzer, 2008) | Set your plan once, e.g. *"When I sit down after dinner, I open the lesson at my last checkpoint."* The **Focus block** button has an *I drifted* path: a 30-second re-entry routine instead of guilt |
| **Fixed timers (Pomodoro)?** | **Mixed evidence.** Biwer et al. (2023) found fixed breaks led to less fatigue and distraction than self-chosen breaks, with the same amount of work done. A 2026 study (Göksu et al.) found self-regulated breaks felt better, with no difference in performance | The focus timer is a tool, not a rule. You pick the length. If fixed blocks feel bad after a couple of weeks, drop them |
| **Building stamina** | I found no strong direct evidence for "focus training" schedules. *(The ladder below is my recommendation, by analogy with progressive overload, not a cited finding.)* One study found two weeks of mindfulness training reduced mind wandering and improved reading-comprehension scores (Mrazek et al., 2013). It's a single study, so treat it as optional | **Focus ladder:** start with a block you can finish cleanly (say 15 min). After about 3 clean blocks, go one step longer. If drift goes up, step back down. The log tracks it |
| **Losing interest** | Interest and curiosity drive attention, and you can't force them. (This is the motivation research above, Ryan & Deci 2000, applied to your case) | Hooks first: a puzzle, a visual, or a real CS link before the definitions. When energy is low, ask the tutor to start with the most interesting angle. Tangents go to a parking-lot list, not into the current block |

## What the tutor is good and bad at

You're learning with an AI model, so its strengths and weaknesses are part of the design too.

**What it does well, and we use fully**
- **Endless fresh practice.** It writes new variants of a problem at your level, so you aren't limited to the book's exercises.
- **Instant, step-level feedback** on your proofs. This includes **photos of handwritten work**, since it can read images.
- **A visual on demand.** Say *show me* about anything that confuses you, and it builds an interactive picture for that exact question, the same way these lesson visuals were built.
- **Checking by code.** It can brute-force finite cases, simulate probabilities, and test a conjecture over thousands of inputs in seconds.
- **Reading the textbook with you.** With `mcs.pdf` in the repo root, it assigns exact sections and cites pages.
- **Patience and availability.** Ask the same thing five ways at 11 pm. That's fine.

**Where it's weak, and the guardrails for each**
- **It can be confidently wrong**, especially in long proofs. *Guardrail:* it grounds claims in the textbook and checks finite cases in code before asserting them. It's required to say when it's unsure.
- **It tends to agree with you.** Language models are biased toward telling users what they want to hear (Sharma et al., 2023). *Guardrail:* `CLAUDE.md` tells it to point to the exact broken line and give a plain verdict. Push back if it seems too nice.
- **It can make learning too easy.** That's the crutch effect below. *Guardrail:* hints in a ladder, and AI-off mock exams.
- **It doesn't remember you between sessions** unless it's written down. *Guardrail:* `progress/log.md` and `progress/mistakes.md` are its memory.

## Beyond the usual: study modes this setup makes possible

These modes combine the techniques above with what the tools can do. Each one says which technique it builds on.

| Mode | How it works | Built on |
|---|---|---|
| **Conjecture lab** (`lab/`) | Before a theorem: compute examples in Python, spot the pattern, state a conjecture, *then* prove it. This is how mathematicians actually work | Productive failure, prior knowledge |
| **Proof as a pull request** (`proofs/`) | Write each pset proof as a Markdown file on a branch and open a PR. The tutor reviews it line by line as GitHub review comments, and you fix and push like code review | Self-explanation, feedback, erroneous examples |
| **Show me** | Any confusing moment becomes a custom interactive visual | Dual coding, concreteness fading |
| **Mistake ledger** (`progress/mistakes.md`) | Every error is logged like a bug: symptom, root cause (e.g. *P(n) not stated*, *step fails at n=1*), fix. Quizzes target your own error patterns | Retrieval practice, metacognition |
| **Break a proof** | The tutor writes a subtly wrong proof for you to find the bug in | Erroneous examples |
| **Teach-back** | You explain the idea to the tutor playing a confused student | Learning by teaching |
| **AI-off mock exam** | Timed, closed-book, no tutor, using past OCW exams. Graded afterwards | Retrieval practice; guards against the crutch effect |

## Using AI without letting it do the learning

The evidence on AI tutors cuts both ways, and both results shaped how the tutor here is set up.

- **Unguarded chat can hurt learning.** In a field experiment with nearly a thousand high-school maths students, plain ChatGPT access raised practice grades by 48%. When access was taken away, those students did **17% worse** than students who never had it. They had used it as a crutch. A version with guardrails (hints, no answers) largely removed that harm (Bastani et al., *PNAS*, 2025).
- **A well-designed tutor can beat a good class.** In a Harvard physics RCT, students using an AI tutor learned more than in an active-learning class: 0.63 SD in the main regression, which the authors call an underestimate because of a ceiling effect, and 0.73–1.3 SD in quantile regression. Median time on task was 49 minutes (Kestin et al., *Scientific Reports*, 2025). The tutor was built for active engagement, managing cognitive load, and growth mindset. It took students through problems **one step at a time**, and it was **grounded in pre-written correct solutions** so its feedback was accurate.

So the tutor (`CLAUDE.md` in this repo) is built to:

1. **Never hand over a pset answer** unless you explicitly ask for it *after* you've made a real attempt. Help comes as a ladder of hints, smallest first.
2. **Go one step at a time.** It asks you for the next step instead of writing the whole proof.
3. **Ground itself.** It checks claims against the textbook (with page numbers) and brute-forces finite cases in Python before telling you something is true. That's the accuracy safeguard.
4. **Make you produce.** Self-explanation, teach-back, and finding bugs: you do the work, and it gives feedback.
5. **Track and space.** It keeps `progress/log.md` updated and opens sessions by quizzing you on older material.

## The human side

AI can't do these for you:

- **Write proofs by hand first.** Paper, then type them up. Struggling over the blank page is the training.
- **Watch the lectures.** The MIT OCW videos and the book are the primary source. These lessons are a companion to them, not a replacement.
- **Sleep between sessions.** Spacing works partly because of consolidation. Three 40-minute sessions beat one two-hour session.
- **Rate yourself honestly.** "Shaky" is useful information. A "got it" you didn't earn hides a gap until the pset finds it.

## References

All checked against their publisher records (Crossref / arXiv) in November 2026.

- Ashcraft, M. H., & Kirk, E. P. (2001). The relationships among working memory, math anxiety, and performance. *J. Exp. Psych.: General*. [doi:10.1037/0096-3445.130.2.224](https://doi.org/10.1037/0096-3445.130.2.224)
- Biwer, F., et al. (2023). Understanding effort regulation: Comparing 'Pomodoro' breaks and self-regulated breaks. *British J. of Educational Psychology*. [doi:10.1111/bjep.12593](https://doi.org/10.1111/bjep.12593)
- Bastani, H., et al. (2025). Generative AI without guardrails can harm learning: Evidence from high school mathematics. *PNAS*. [doi:10.1073/pnas.2422633122](https://doi.org/10.1073/pnas.2422633122)
- Bjork, R. A. (1994). Memory and metamemory considerations in the training of human beings. In *Metacognition: Knowing about Knowing*, MIT Press. (Book chapter, no DOI)
- Bloom, B. S. (1984). The 2 sigma problem. *Educational Researcher*. [doi:10.3102/0013189X013006004](https://doi.org/10.3102/0013189X013006004)
- Cepeda, N. J., et al. (2006). Distributed practice in verbal recall tasks: A review and quantitative synthesis. *Psychological Bulletin*. [doi:10.1037/0033-2909.132.3.354](https://doi.org/10.1037/0033-2909.132.3.354)
- Chi, M. T. H., et al. (1989). Self-explanations: How students study and use examples in learning to solve problems. *Cognitive Science*. [doi:10.1207/s15516709cog1302_1](https://doi.org/10.1207/s15516709cog1302_1)
- Chi, M. T. H., & Wylie, R. (2014). The ICAP framework. *Educational Psychologist*. [doi:10.1080/00461520.2014.965823](https://doi.org/10.1080/00461520.2014.965823)
- Diekelmann, S., & Born, J. (2010). The memory function of sleep. *Nature Reviews Neuroscience*. [doi:10.1038/nrn2762](https://doi.org/10.1038/nrn2762)
- Dunlosky, J., et al. (2013). Improving students' learning with effective learning techniques. *Psych. Science in the Public Interest*. [doi:10.1177/1529100612453266](https://doi.org/10.1177/1529100612453266)
- Fiorella, L., & Mayer, R. E. (2013). The relative benefits of learning by teaching and teaching expectancy. *Contemporary Educational Psychology*. [doi:10.1016/j.cedpsych.2013.06.001](https://doi.org/10.1016/j.cedpsych.2013.06.001)
- Fyfe, E. R., et al. (2014). Concreteness fading in mathematics and science instruction: A systematic review. *Educational Psychology Review*. [doi:10.1007/s10648-014-9249-3](https://doi.org/10.1007/s10648-014-9249-3)
- Gawrilow, C., & Gollwitzer, P. M. (2008). Implementation intentions facilitate response inhibition in children with ADHD. *Cognitive Therapy and Research*. [doi:10.1007/s10608-007-9150-1](https://doi.org/10.1007/s10608-007-9150-1)
- Göksu, A., et al. (2026). When to take a break: Comparing effects of systematic short (Pomodoro) and self-regulated breaks on subjective experience and actual learning. *Behavioral Sciences*. [doi:10.3390/bs16071158](https://doi.org/10.3390/bs16071158)
- Gollwitzer, P. M., & Sheeran, P. (2006). Implementation intentions and goal achievement: A meta-analysis of effects and processes. *Advances in Experimental Social Psychology*. [doi:10.1016/S0065-2601(06)38002-1](https://doi.org/10.1016/S0065-2601(06)38002-1)
- Hodds, M., Alcock, L., & Inglis, M. (2014). Self-explanation training improves proof comprehension. *JRME*. [doi:10.5951/jresematheduc.45.1.0062](https://doi.org/10.5951/jresematheduc.45.1.0062) · [training booklet (PDF)](https://www.lboro.ac.uk/media/media/schoolanddepartments/mathematics-education-centre/downloads/research/SE-booklet.pdf)
- Kalyuga, S., et al. (2003). The expertise reversal effect. *Educational Psychologist*. [doi:10.1207/S15326985EP3801_4](https://doi.org/10.1207/S15326985EP3801_4)
- Kapur, M. (2008). Productive failure. *Cognition and Instruction*. [doi:10.1080/07370000802212669](https://doi.org/10.1080/07370000802212669)
- Kestin, G., et al. (2025). AI tutoring outperforms in-class active learning: an RCT introducing a novel research-based design in an authentic educational setting. *Scientific Reports*. [doi:10.1038/s41598-025-97652-6](https://doi.org/10.1038/s41598-025-97652-6)
- Leron, U., & Dubinsky, E. (1995). An abstract algebra story. *American Mathematical Monthly*. [doi:10.1080/00029890.1995.11990563](https://doi.org/10.1080/00029890.1995.11990563)
- Mayer, R. E. *Multimedia Learning* (3rd ed., 2020). Cambridge University Press. (Book)
- McLaren, B. M., Adams, D. M., & Mayer, R. E. (2015). Delayed learning effects with erroneous examples. *Int. J. of AI in Education*. [doi:10.1007/s40593-015-0064-x](https://doi.org/10.1007/s40593-015-0064-x)
- Mrazek, M. D., et al. (2013). Mindfulness training improves working memory capacity and GRE performance while reducing mind wandering. *Psychological Science*. [doi:10.1177/0956797612459659](https://doi.org/10.1177/0956797612459659)
- Pashler, H., et al. (2008). Learning styles: Concepts and evidence. *Psych. Science in the Public Interest*. [doi:10.1111/j.1539-6053.2009.01038.x](https://doi.org/10.1111/j.1539-6053.2009.01038.x)
- Ramirez, G., & Beilock, S. L. (2011). Writing about testing worries boosts exam performance in the classroom. *Science*. [doi:10.1126/science.1199427](https://doi.org/10.1126/science.1199427)
- Renkl, A., & Atkinson, R. K. (2003). Structuring the transition from example study to problem solving. *Educational Psychologist*. [doi:10.1207/S15326985EP3801_3](https://doi.org/10.1207/S15326985EP3801_3)
- Roediger, H. L., & Karpicke, J. D. (2006). Test-enhanced learning. *Psychological Science*. [doi:10.1111/j.1467-9280.2006.01693.x](https://doi.org/10.1111/j.1467-9280.2006.01693.x)
- Rohrer, D., & Taylor, K. (2007). The shuffling of mathematics problems improves learning. *Instructional Science*. [doi:10.1007/s11251-007-9015-8](https://doi.org/10.1007/s11251-007-9015-8)
- Ryan, R. M., & Deci, E. L. (2000). Self-determination theory and the facilitation of intrinsic motivation. *American Psychologist*. [doi:10.1037/0003-066X.55.1.68](https://doi.org/10.1037/0003-066X.55.1.68)
- Sharma, M., et al. (2023). Towards understanding sycophancy in language models. [arXiv:2310.13548](https://arxiv.org/abs/2310.13548)
- Sinha, T., & Kapur, M. (2021). When problem solving followed by instruction works: Evidence for productive failure. *Review of Educational Research*. [doi:10.3102/00346543211019105](https://doi.org/10.3102/00346543211019105)
- Sisk, V. F., et al. (2018). To what extent and under which circumstances are growth mind-sets important to academic achievement? *Psychological Science*. [doi:10.1177/0956797617739704](https://doi.org/10.1177/0956797617739704)
- Szpunar, K. K., Khan, N. Y., & Schacter, D. L. (2013). Interpolated memory tests reduce mind wandering and improve learning of online lectures. *PNAS*. [doi:10.1073/pnas.1221764110](https://doi.org/10.1073/pnas.1221764110)
- VanLehn, K. (2011). The relative effectiveness of human tutoring, intelligent tutoring systems, and other tutoring systems. *Educational Psychologist*. [doi:10.1080/00461520.2011.611369](https://doi.org/10.1080/00461520.2011.611369)
