from argparse import ArgumentParser
import os





FINBERT = "TurkuNLP/bert-base-finnish-cased-v1"

CYRILLIC_LANGUAGES = {"myv"}

CYRILLIC_TO_LATIN = {
    "а": "a",  "б": "b",  "в": "v",  "г": "g",  "д": "d",
    "е": "e", "ё": "jo", "ж": "zh",  "з": "z",  "и": "i",
    "й": "j",  "к": "k",  "л": "l",  "м": "m",  "н": "n",
    "о": "o",  "п": "p",  "р": "r",  "с": "s",  "т": "t",
    "у": "u",  "ф": "f",  "х": "h",  "ц": "c",  "ч": "ch",
    "ш": "sh",  "щ": "shch", "ъ": "",   "ы": "y",  "ь": "ʼ",
    "э": "e",  "ю": "ju", "я": "ja",
    "А": "A",  "Б": "B",  "В": "V",  "Г": "G",  "Д": "D",
    "Е": "E", "Ё": "Jo", "Ж": "Zh",  "З": "Z",  "И": "I",
    "Й": "J",  "К": "K",  "Л": "L",  "М": "M",  "Н": "N",
    "О": "O",  "П": "P",  "Р": "R",  "С": "S",  "Т": "T",
    "У": "U",  "Ф": "F",  "Х": "H",  "Ц": "C",  "Ч": "Ch",
    "Ш": "Sh",  "Щ": "Shch", "Ъ": "",   "Ы": "Y",  "Ь": "ʼ",
    "Э": "E",  "Ю": "Ju", "Я": "Ja",
}

def argparser():
    ap = ArgumentParser()
    ap.add_argument("--train", required=True)
    ap.add_argument("--test", required=True)
    ap.add_argument("--output_dir", required=True)
    ap.add_argument("--language", required=True)
    return ap.parse_args()

def transliterate(word):
    return "".join(CYRILLIC_TO_LATIN.get(ch, ch) for ch in word)


def transliterate_conllu(in_path, out_path):
    with open(in_path, encoding="utf-8") as fin:
        with open(out_path, "w", encoding="utf-8") as fout:
            for line in fin:
                stripped = line.rstrip("\n")
                if stripped == "" or stripped.startswith("#"):
                    fout.write(line)
                    continue
                cols = stripped.split("\t")
                if len(cols) >= 2 and "-" not in cols[0] and "." not in cols[0]:
                    cols[1] = transliterate(cols[1])
                fout.write("\t".join(cols) + "\n")
    print(f"Transliterated: {in_path} -> {out_path}")


def read_raw_sentences(path):
    sentences, current = [], []
    with open(path, encoding="utf-8") as f:
        for line in f:
            current.append(line)
            if line.strip() == "":
                sentences.append(current)
                current = []
    return sentences


def write_raw_sentences(sentences, path):
    with open(path, "w", encoding="utf-8") as f:
        for sentence in sentences:
            f.writelines(sentence)






def main():
    args = argparser()
    os.makedirs(args.output_dir, exist_ok=True)

    if args.language in CYRILLIC_LANGUAGES:
        print(f"Transliterating.")
        train_path = f"{args.output_dir}/train_translit.conllu"
        test_path  = f"{args.output_dir}/test_translit.conllu"
        transliterate_conllu(args.train, train_path)
        transliterate_conllu(args.test,  test_path)
    else:
        print(f"No transliteration needed.")
        train_path = args.train
        test_path  = args.test


    train_out = f"{args.output_dir}/train_encoded.conllu"
    test_out = f"{args.output_dir}/test_encoded.conllu"
    raw_train = read_raw_sentences(train_path)
    raw_test = read_raw_sentences(test_path)
    write_raw_sentences(raw_train, train_out)
    write_raw_sentences(raw_test, test_out)




if __name__ == "__main__":
    main()

