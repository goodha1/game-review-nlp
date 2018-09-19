"""
Data cleaning(pre-processing):
    1. Remove all reviews contains irregular special characters, like …, § ✦ ♬ ☐ ☑ ☼ ☣ ۞ emojis and other interesting staff commonly contained in gaming reviews. Except for "♥". We found people love to type ♥, and ♥ is a strong indicator of positive reviews.

    2.Calculate statistics about ♥ and divide the data to train, dev, and test.
"""

import re
import random

# convert csv to tsv, and separate year and month into two columns.
# store all special_chars apperrs, happens to be non-english chars and emojis.
TOTAL = 0
special_chars = set()
out = open("scum-review.tsv", "w")
special = open("special-chars.txt", "w")
with open("scum-review.csv", "r") as f:
    for line in f:
        TOTAL += 1
        rec = line.strip().split(",")
        rec[8] = rec[8][1:]
        rec[9] = rec[9][:-2]
        for x in rec[-1]:
            if ord(x) >= 128:
                special_chars.add(x)
        out.write("\t".join(rec) + "\n")
out.close()
special.write(" ".join(special_chars))
special.close()
print("Total number of raw review:", TOTAL)


# separate reviews with/withOUT special chars
review_with_special = open("review-with-special", "w")
review_with_special.write("\t".join(["label", "review"]) + "\n")
WITH_SPECIAL = 0  # number of (invalid) data: reviews with special chars

review_without_special = open("review-without-special", "w")
review_without_special.write("\t".join(["label", "review"]) + "\n")
N = 0  # total number of (valid) data: reviews without special chars except for ♥

# special_chars.remove("♥")
SPECIAL_REGEX = re.compile("[" + "".join(special_chars) + "]")
with open("scum-review.tsv", "r") as f:
    pos_heart, heart = 0, 0  # calculate the proportion of positive reviews in reviews contain ♥
    for line in f:
        rec = line.strip().split("\t")
        if re.search(SPECIAL_REGEX, rec[-1]):
            review_with_special.write("\t".join((rec[6], rec[-1])) + "\n")
            WITH_SPECIAL += 1
        else:
            review_without_special.write("\t".join((rec[6], rec[-1])) + "\n")
            N += 1
            # if "♥" in rec[-1]:
            #     heart += 1
            #     if rec[6] == "1":
            #         pos_heart += 1

review_with_special.close()
review_without_special.close()

print(f"    - {WITH_SPECIAL} reviews contain speial characters.")
print(f"    - {TOTAL - WITH_SPECIAL}({round((TOTAL - WITH_SPECIAL) / TOTAL * 100, 2)}%) valid (reviews without special characters)")
# print(f"Out of {heart} reviews contain ♥, {pos_heart}({round(pos_heart / heart * 100, 2)}%) of them are positive")


def train_test_split(file, train=.6, dev=.2, tag="-ns"):
    "tag -ns means no special chars reviews"
    f_train = open("train" + tag, "w")
    f_dev = open("dev" + tag, "w")
    f_test = open("test" + tag, "w")
    f_train.write("label\treview\n")
    f_dev.write("label\treview\n")
    f_test.write("label\treview\n")
    with open(file, "r") as f:  # input review files
        f.readline()
        for line in f:
            where = random.uniform(0, 1)
            if where <= train:
                f_train.write(line)
            elif where >= (train + dev):
                f_test.write(line)
            else:
                f_dev.write(line)
    f_train.close()
    f_dev.close()
    f_test.close()


train_test_split("review-without-special")


# 现在是不要❤️
