# Release Policy

A Foundry release must include:

- passing tests;
- passing `make foundry-validate`;
- valid pack manifests;
- valid tool, pack, profile, adapter, compatibility, dependency, and
  deprecation registries;
- updated release notes;
- no nested `AGENTS.md` files;
- no capability pack containing a project-level controller.

Recommended first release tag: `v0.1.0-foundry`.
