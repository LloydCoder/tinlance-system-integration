import json
from pathlib import Path
def main():
 o=json.loads((Path(__file__).parents[1]/"workflows/canonical.json").read_text()); b=json.loads((Path(__file__).parents[1]/"policies/closed-loop-baseline.json").read_text())
 w=next(x for x in o["workflows"] if x["id"]=="acquisition-feedback")
 assert w["steps"]==["world-intelligence","tads","sdea","reconos","fadereach","fdse","outcome","evidence","economic-attribution","evaluation","tads"]
 assert b["authority"]=="tsic"
 print("PASS TSIC-35 closed-loop certification")
if __name__=="__main__": main()
