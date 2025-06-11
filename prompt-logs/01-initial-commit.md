# Pull Request #1
**Prompt:**
You are a **Lead Python Automation Engineer**.  
Read the project’s root-level `spec.md` and generate the **initial commit scaffolding** exactly as files that can be piped straight into `git apply`.  
Produce **un-fenced** output in patch-style blocks:

```

\--- path/to/file.ext        (new) <file contents>
\--- end of file

```

List every new or modified file in this format. Use **Python 3.12** with docstrings only; no Sphinx.  

### Required files  
1. **Code** – modules, packages, and an `openai_client.py` thin wrapper (env-var key, retry + back-off).  
2. **tests/** – pytest stubs (≥ 1 happy path + 1 edge case per public API).  
3. **pyproject.toml** (PEP 621 metadata, deps, `[tool.pytest.ini_options]`).  
4. **.gitignore** – Python, venv, VS Code.  
5. **README.md** – “Quick-start for contributors” (venv, install, test, run example).  

### Conventions  
* One concern per file; no circular imports.  
* Default `DEBUG = True` pattern, `logging` (minimal formatter `"%(levelname)s: %(message)s"`), in-memory buffer `log_buffer`; include `# TODO:` on every stub.  
* Where `spec.md` is ambiguous, insert `STUB_…` placeholders and note them in **Next steps**.  
* If `spec.md` cannot be read, prompt the user: *“Please paste the file or upload it.”*  
* Keep each patch block ≤ 300 lines; split as `Part n/m` if longer.  

### Output order  
1. Summary file-tree.  
2. Patch blocks for all files.  
3. **Next steps** – ≤ 5 bullets of follow-up work (e.g., refine algorithm, supply sample data).  