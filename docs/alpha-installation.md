# RIFT//STAR Alpha 0.2.1 installation

The supported client import is `dist/RIFTSTAR-0.2.1-alpha.zip`. In a
CurseForge-compatible launcher, create a Minecraft **1.20.1 Forge 47.4.10**
profile and use **Import** to select that ZIP. The launcher downloads the
manifest-pinned third-party mods; the pack's companion jar and configuration
files are supplied by the ZIP.

For a local/manual install, use a clean Forge 1.20.1 instance, restore the
locked jars with `python fetch_mods.py`, and run
`python assemble_client.py`. Copy the resulting `client/mods`,
`client/config`, `client/defaultconfigs`, `client/kubejs`, and
`client/resourcepacks` into the instance. Do not copy client-only jars to a
dedicated server.

Third-party jars, Forge libraries, worlds, logs, and generated distributions
are intentionally ignored by Git. Re-run the restore and packaging commands
instead of committing generated binaries.
