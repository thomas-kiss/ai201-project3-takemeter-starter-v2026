# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1. Overall accuracy

Overall accuracy of at least 0.65 on the held-out test set.

**Why this target:** Three labels. A coin flip gets about 33%. 0.65 is
clearly above guessing and is where I'd actually trust the model to sort
comments for me instead of double checking every one.

---

## 2. `hot_take` vs `analysis`, the hard boundary

F1 for `hot_take` of at least 0.55 on the held-out set.

**Why this target:** This is my hardest boundary. I expect the model to
mix up `hot_take` and `analysis` sometimes, same as I did when labeling.
0.55 is lower than my overall target on purpose.

---

## 3. `reaction` performance

F1 for `reaction` of at least 0.60 on the held-out set.

**Why this target:** `reaction` is the easiest label to spot. Banter and
jokes don't look like the other two. I expect this to be the model's best
label, so the bar is higher here than for `hot_take`.

---

## 4. Balance

No label makes up less than 20% of the 200 examples in `labels.csv`.

**Why this target:** The project caps any label at 70%. That stops one
label from taking over. But a label could still sit at 21% and be too thin
to measure well. 20% of 200 is 40 examples, enough that the test split
still has a reasonable number in it.

---

## 5. Confidence

When the model's top prediction has confidence 0.8 or higher, it should be
right at least 85% of the time.

**Why this target:** If the model is going to say it's sure, I want sure to
mean something. 85% leaves room for the model to be wrong sometimes even
when confident, since this is a small dataset, but it should still beat its
overall accuracy by a real margin when it claims to be confident.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
