# qpop — reviewer / contributor reproduction targets.  Run `make help` for the list.
# Everything here works from a clean clone with only Python 3.9+ (the ledger has no deps).
PY ?= python

.PHONY: help test verify-sample tamper validate anchor-demo external-anchor-demo demo paper

help:
	@echo "qpop targets:"
	@echo "  make test                 run the test suite (pytest; 27 ledger/anchor + 5 schema tests)"
	@echo "  make verify-sample        verify the bundled synthetic ledger's hash chain"
	@echo "  make tamper               demo: edit a frozen field and watch verification fail"
	@echo "  make validate             validate data/synthetic/* against schemas/ (needs jsonschema)"
	@echo "  make anchor-demo          write + verify a LOCAL anchor manifest for the sample"
	@echo "  make external-anchor-demo submit + verify an EXTERNAL (OpenTimestamps) anchor"
	@echo "                            (needs network + 'pip install forward-qpop[anchor]')"
	@echo "  make demo                 verify-sample + explain what the chain does / does not prove"
	@echo "  make paper                build research/paper/paper.pdf (needs pdflatex + bibtex)"

test:
	$(PY) -m pytest -q

verify-sample:
	$(PY) scripts/qpop.py verify data/synthetic/qpop_ledger_sample.jsonl

tamper:
	$(PY) repro/tamper_demo.py

validate:
	$(PY) repro/validate_samples.py

anchor-demo:
	$(PY) scripts/qpop.py anchor data/synthetic/qpop_ledger_sample.jsonl
	$(PY) scripts/qpop.py verify-anchor data/synthetic/qpop_ledger_sample.jsonl

external-anchor-demo: anchor-demo
	$(PY) scripts/qpop.py anchor external data/synthetic/qpop_ledger_sample.jsonl --method ots
	$(PY) scripts/qpop.py verify-external data/synthetic/qpop_ledger_sample.jsonl

demo: verify-sample
	@echo ""
	@echo "That output is a real hash chain (entry_hash = sha256(content_hash || prev_hash))."
	@echo "Edit, insert, delete, or reorder any entry in the .jsonl and 'make verify-sample' fails."
	@echo "What it proves: tamper-evidence. What it does NOT prove alone: wall-clock time"
	@echo "(anchor externally — signed commit/release, public CI, OpenTimestamps/Rekor)."

paper:
	cd research/paper && \
	pdflatex -interaction=nonstopmode paper.tex && bibtex paper && \
	pdflatex -interaction=nonstopmode paper.tex && pdflatex -interaction=nonstopmode paper.tex
