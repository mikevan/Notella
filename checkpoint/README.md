# Owner-run check-in

The owner inspects and executes this script. The assistant does not stage, commit, create the GitHub repository or push.

From C:\workspace\Notella:

```powershell
.\Check-In.ps1
```

This previews a frozen allowlist and verifies each listed file's SHA-256. It changes no repository state.

For the requested first check-in to mikevan/Notella, inspect the script, then run:

```powershell
.\Check-In.ps1 -Execute -Push -CreateRemote
```

This initializes the local repository if needed, verifies the Git author, creates mikevan/Notella **privately** if it cannot already access it, stages only listed files, checks the staged changes, commits and performs a normal push. It requires Git and authenticated GitHub CLI. If the repository exists but is inaccessible, creation fails rather than replacing it. A nonempty remote with no local history is rejected for manual reconciliation. No force-push is used.

Omit -Push for a local commit only. Omit -CreateRemote when the remote already exists. Existing staged files or a different origin cause a stop, preserving the owner's choices. Failures after staging preserve staged changes for inspection; the script does not reset them automatically.

Selected evidence is copied out of ignored runtime folders into checkpoint/evidence. Large model/optimizer weights remain local. Subsequent experiments are not part of the frozen allowlist. Changing a listed file causes verification to fail; regenerate and review a new checkpoint rather than weakening the hash check.

The manifest is a local review aid, not a signed security attestation. Inspect the script and manifest before execution. The script verifies the remote branch after a successful push.
