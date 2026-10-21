"""
Builds labels.csv from data/raw_comments.csv using manual labels assigned by
reading each comment against the taxonomy in README.md (analysis / hot_take /
reaction). See notes.md and README's "How I Used AI" section for how this
labeling pass was actually done.
"""
import csv

LABELS = {
    1: "reaction", 2: "analysis", 3: "reaction", 4: "reaction", 5: "reaction",
    6: "reaction", 7: "reaction", 8: "reaction", 9: "hot_take", 10: "analysis",
    11: "analysis", 12: "hot_take", 13: "analysis", 14: "hot_take", 15: "hot_take",
    16: "hot_take", 17: "hot_take", 18: "analysis", 19: "hot_take", 20: "reaction",
    21: "hot_take", 22: "reaction", 23: "hot_take", 24: "hot_take", 25: "hot_take",
    26: "hot_take", 27: "hot_take", 28: "hot_take", 29: "reaction", 30: "analysis",
    31: "reaction", 32: "reaction", 33: "reaction", 34: "analysis", 35: "reaction",
    36: "analysis", 37: "reaction", 38: "analysis", 39: "hot_take", 40: "hot_take",
    41: "analysis", 42: "analysis", 43: "reaction", 44: "analysis", 45: "analysis",
    46: "analysis", 47: "analysis", 48: "analysis", 49: "analysis", 50: "hot_take",
    51: "analysis", 52: "reaction", 53: "reaction", 54: "analysis", 55: "analysis",
    56: "reaction", 57: "reaction", 58: "reaction", 59: "hot_take", 60: "hot_take",
    61: "reaction", 62: "analysis", 63: "reaction", 64: "analysis", 65: "reaction",
    66: "analysis", 67: "reaction", 68: "hot_take", 69: "reaction", 70: "hot_take",
    71: "hot_take", 72: "hot_take", 73: "reaction", 74: "analysis", 75: "reaction",
    76: "analysis", 77: "reaction", 78: "analysis", 79: "hot_take", 80: "hot_take",
    81: "hot_take", 83: "reaction", 84: "analysis", 85: "hot_take", 86: "hot_take",
    87: "hot_take", 88: "hot_take", 89: "hot_take", 90: "hot_take", 91: "hot_take",
    92: "reaction", 93: "hot_take", 94: "reaction", 95: "analysis", 96: "hot_take",
    97: "hot_take", 98: "reaction", 99: "reaction", 100: "analysis", 101: "reaction",
    102: "reaction", 103: "analysis",
    120: "reaction", 121: "analysis", 122: "reaction", 123: "reaction",
    124: "analysis", 125: "hot_take", 126: "reaction", 127: "reaction",
    128: "hot_take", 129: "hot_take", 130: "hot_take", 131: "analysis",
    132: "hot_take", 133: "analysis", 134: "hot_take", 135: "reaction",
    136: "hot_take", 137: "analysis", 138: "reaction", 139: "analysis",
    140: "analysis", 141: "hot_take", 142: "reaction", 143: "hot_take",
    144: "analysis", 145: "analysis", 146: "hot_take", 147: "analysis",
    148: "hot_take", 149: "hot_take", 150: "analysis", 151: "analysis",
    152: "analysis", 153: "hot_take", 154: "reaction", 155: "analysis",
    156: "analysis", 157: "hot_take", 158: "reaction", 159: "hot_take",
    160: "hot_take", 161: "reaction", 162: "reaction", 163: "reaction",
    164: "hot_take", 165: "hot_take", 166: "analysis", 167: "reaction",
    168: "reaction", 169: "analysis", 170: "reaction", 171: "analysis",
    172: "hot_take", 173: "hot_take", 174: "analysis", 175: "analysis",
    176: "reaction", 177: "analysis", 178: "reaction", 179: "reaction",
    180: "reaction", 181: "analysis", 182: "analysis", 183: "analysis",
    184: "analysis", 185: "hot_take", 186: "analysis", 187: "analysis",
    188: "reaction", 189: "reaction", 190: "reaction", 191: "reaction",
    192: "reaction", 193: "hot_take", 194: "reaction", 195: "reaction",
    196: "analysis", 197: "reaction", 198: "reaction", 199: "reaction",
    200: "reaction", 201: "reaction", 202: "reaction", 203: "reaction",
    204: "reaction", 205: "reaction", 206: "hot_take", 207: "reaction",
    208: "analysis", 209: "reaction", 210: "analysis", 211: "analysis",
    212: "hot_take", 213: "reaction", 214: "analysis", 215: "reaction",
    216: "hot_take", 217: "reaction", 218: "analysis", 219: "reaction",
    220: "reaction", 221: "reaction", 222: "hot_take", 223: "reaction",
    224: "reaction", 225: "hot_take", 226: "reaction", 227: "analysis",
    228: "hot_take", 229: "hot_take", 230: "hot_take", 231: "reaction",
    232: "hot_take", 233: "reaction", 234: "reaction", 235: "reaction",
    236: "reaction", 237: "analysis", 238: "reaction", 239: "hot_take",
    240: "reaction", 241: "analysis", 242: "reaction", 243: "hot_take",
    244: "hot_take", 245: "reaction", 246: "hot_take", 247: "hot_take",
    248: "analysis", 249: "hot_take", 250: "hot_take", 251: "hot_take",
    252: "reaction", 253: "hot_take", 255: "hot_take", 256: "analysis",
    257: "analysis", 258: "reaction", 259: "reaction",
}

# Notes for a handful of genuinely hard calls, for the README's "three hard
# cases" and for anyone reading labels.csv.
HARD_CASE_NOTES = {
    103: "hard case: critiques 'lazy analysis' using statistical reasoning "
         "(shooting variance, sample size) but cites no hard number itself. "
         "Called analysis for the reasoning, could be hot_take.",
    28: "hard case: says 'perfect glue guy stat line' but never states the "
        "actual stat. Called hot_take since no number is actually given.",
    153: "hard case: states a behavior pattern (braids = conditioning tell) "
         "as fact but it's really a running joke, not a checkable claim. "
         "Called hot_take.",
}


def main():
    with open("data/raw_comments.csv") as f:
        rows = list(csv.DictReader(f))

    out_rows = []
    for idx, label in LABELS.items():
        text = rows[idx]["text"]
        note = "ai-labeled" if idx not in HARD_CASE_NOTES else HARD_CASE_NOTES[idx]
        out_rows.append({"text": text, "label": label, "note": note})

    from collections import Counter
    counts = Counter(r["label"] for r in out_rows)
    print("Label counts:", dict(counts))
    print("Total:", len(out_rows))
    for label, n in counts.items():
        print(f"  {label}: {n/len(out_rows):.1%}")

    with open("labels.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["text", "label", "note"])
        w.writeheader()
        w.writerows(out_rows)
    print("\nWrote labels.csv")


if __name__ == "__main__":
    main()
