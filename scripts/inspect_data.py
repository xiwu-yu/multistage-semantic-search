import csv
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "scifact"


def load_jsonl(path):
    records = {}
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            item = json.loads(line)
            records[str(item["_id"])] = item
    return records


corpus = load_jsonl(DATA_DIR / "corpus.jsonl")
queries = load_jsonl(DATA_DIR / "queries.jsonl")

with (DATA_DIR / "qrels" / "test.tsv").open(
    "r", encoding="utf-8", newline=""
) as file:
    qrels = list(csv.DictReader(file, delimiter="\t"))

test_query_ids = {row["query-id"] for row in qrels}
positive = next(row for row in qrels if int(row["score"]) > 0)

query = queries[positive["query-id"]]
document = corpus[positive["corpus-id"]]

print("文档数:", len(corpus))
print("全部查询数:", len(queries))
print("测试查询数:", len(test_query_ids))
print("标注条数:", len(qrels))
print("查询:", query["text"])
print("相关文档标题:", document["title"])
print("相关文档内容前400字:", document["text"][:400])