# Validation boundary

\`test_source_characterization.mjs\` independently records three source behaviors without exercising browser rendering: invalid command rejection, protection of a user-owned widget and finite/positive geometry checks.

\`test_actor_scoped_command_admission.mjs\` verifies the pure generalized contract, including ownership, missing resources, registered kinds, geometry and non-mutation.

Run with \`node --test validation/*.mjs\` from the module directory.

These tests do not validate DOM construction, pointer events, accessibility, persistence, authentication or the safety of any operation performed after admission.
