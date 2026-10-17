# Alpha 0.2 manual client checklist

- [ ] Use Java 17 and a clean Minecraft 1.20.1 Forge 47.4.10 profile.
- [ ] Import `dist/RIFTSTAR-0.2.0-alpha.zip` or run `python assemble_client.py`.
- [ ] Confirm the Forge title screen reaches the main menu without a crash.
- [ ] Confirm the Mods screen includes `RIFT//STAR Companion`, KubeJS, and the
      pinned content mods.
- [ ] Create a new test world and confirm the Prism Lens recipe appears in JEI.
- [ ] Craft or obtain a Prism Lens and confirm the `riftstar:first_colour`
      advancement is awarded.
- [ ] Check that the configured resource pack loads and no missing-resource
      errors appear in the client log.
- [ ] Enable `RIFTSTAR_Visuals` and confirm the Fractured Cosmos advancement
      backdrop renders without missing-texture errors.
- [ ] Confirm native visits award Moonlit Misfit, Honeyed Horizon, and
      Understone Rainbow without changing any mod's route or unlocks.
- [ ] Join a dedicated server built from the same lockfile and confirm the
      client can connect.

Record the launcher, Java version, operating system, and any crash-report path
when a check fails.
