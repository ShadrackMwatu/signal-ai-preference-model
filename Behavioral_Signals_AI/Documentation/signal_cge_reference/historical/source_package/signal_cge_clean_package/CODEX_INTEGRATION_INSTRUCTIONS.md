Store and integrate the Signal CGE adapted reference package into the repository.

Tasks:
1. Create signal_cge/canonical_reference/signal_cge_reference/docs/.
2. Add Signal_CGE_User_Guide_Adapted.docx and Signal_CGE_User_Guide_Adapted.pdf to that folder if file sizes are acceptable.
3. Add docs/SIGNAL_CGE_REFERENCE_README.md explaining that this is a Signal-native adapted guide for implementation.
4. Do not commit generated runtime outputs, GDX/G00 files, logs, local paths, secrets, or large binaries.
5. Ensure .gitignore excludes *.gdx, *.g00, *.lst, *.log, *.tmp, *.bak, 00_Save/, 10_gdx/, and generated results folders.
6. Update Documentation/SIGNAL_CGE_DOCUMENTATION_INDEX.md to link to the adapted Signal CGE guide.
7. Update README.md with a short note under Signal CGE Architecture.
8. Run python -m pytest -q.
9. Commit with: git commit -m "Add Signal CGE adapted reference guide".
10. Do not push automatically.