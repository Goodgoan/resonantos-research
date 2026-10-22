# What-if reporting (Gate 3, D4.0 (3)(d)): capture-weighted profile and score perturbation

These tables are reporting only. The decision weights in `weights.json` are unchanged, and no reference architecture or proposed layer is scored (D4.0 (3)(c)). Totals rate the upstream artifact as inspected (D3.7 (c)).

## 1. What if the DAO skeptic's capture-weighted profile were used for dao_contract?

Weights: requirement_fit 0.22, isolation_and_security 0.24, demonstrated_maturity 0.16, maintenance_sustainability 0.12, licence 0.06, integration 0.04, sovereignty 0.06, interoperability 0.04, operations 0.06 (reviews/dao-skeptic.md C-2). Baseline = the pre-registered dao_contract weights.

| Capture rank | Codebase | Capture total | Baseline total | Baseline rank | Change |
|---|---|---|---|---|---|
| 1 | openwallet-foundation-labs-identity-common-ts | 3.40 | 3.56 | 1 | same |
| 2 | openwallet-foundation-labs-identity-common-ts@R23 | 3.18 | 3.40 | 2 | same |
| 3 | transparency-dev-tessera | 3.16 | 3.28 | 3 | same |
| 4 | mythic-project-spl-governance-v3-1-3 | 2.48 | 2.54 | 5 | up 1 |
| 5 | hypercerts-org-hypercerts-lexicon | 2.32 | 2.66 | 4 | down 1 |
| 6 | solana-foundation-rewards | 1.76 | 2.08 | 6 | same |

Reading: the capture profile shifts weight from the five convenience criteria (licence, integration, sovereignty, interoperability, operations: 0.36 of the baseline) to requirement fit and isolation (0.46). Ranks that move under it are listed above; the article reports them beside the baseline, not instead of it.

## 2. W-6 score-perturbation pass (isolation_and_security +1 and -1 per candidate)

For each group below, each candidate's isolation score is moved by +1 and then by -1 (clamped to 0..5), one candidate at a time, with the pre-registered weights. FLIPS lists the moves that change that candidate's rank; a flip under a one-point change on the heaviest criterion is as fragile as a weight flip (reviews/security-engineer.md W-6).

### Profile: os_kernel (all requirements; cross-requirement order is indicative only)

| Rank | Codebase | Baseline total | Isolation | Perturbation result |
|---|---|---|---|---|
| 1 | anthropics-sandbox-runtime | 3.76 | 3 | FLIPS: anthropics-sandbox-runtime iso -1; theupdateframework-tuf-js iso +1 |
| 2 | theupdateframework-tuf-js | 3.74 | 3 | FLIPS: anthropics-sandbox-runtime iso -1; theupdateframework-tuf-js iso +1 |
| 3 | eclipse-biscuit | 3.28 | 2 | FLIPS: anthropics-sandbox-runtime@R03 iso +1; eclipse-biscuit iso -1; openworkflowdev-openworkflow iso +1; transparency-dev-tessera iso +1 |
| 4 | transparency-dev-tessera | 3.26 | 3 | FLIPS: anthropics-sandbox-runtime@R03 iso +1; eclipse-biscuit iso -1; holepunchto-hypercore iso +1; openworkflowdev-openworkflow iso +1; transparency-dev-tessera iso +1; transparency-dev-tessera iso -1 |
| 5 | anthropics-sandbox-runtime@R03 | 3.14 | 2 | FLIPS: anthropics-sandbox-runtime@R03 iso +1; anthropics-sandbox-runtime@R03 iso -1; convira-convira-sandbox iso +1; eclipse-biscuit iso -1; holepunchto-hypercore iso +1; openworkflowdev-openworkflow iso +1; transparency-dev-tessera iso -1 |
| 6 | openworkflowdev-openworkflow | 3.08 | 1 | FLIPS: anthropics-sandbox-runtime@R03 iso -1; convira-convira-sandbox iso +1; eclipse-biscuit iso -1; holepunchto-hypercore iso +1; openworkflowdev-openworkflow iso +1; openworkflowdev-openworkflow iso -1; transparency-dev-tessera iso -1 |
| 7 | holepunchto-hypercore | 3.04 | 2 | FLIPS: anthropics-sandbox-runtime@R03 iso -1; convira-convira-sandbox iso +1; holepunchto-hypercore iso +1; holepunchto-hypercore iso -1; openworkflowdev-openworkflow iso -1; transparency-dev-tessera iso -1 |
| 8 | convira-convira-sandbox | 3.02 | 3 | FLIPS: anthropics-sandbox-runtime@R03 iso -1; convira-convira-sandbox iso +1; convira-convira-sandbox iso -1; holepunchto-hypercore iso -1; openworkflowdev-openworkflow iso -1 |
| 9 | dapr-durabletask-go | 2.80 | 1 | FLIPS: convira-convira-sandbox iso -1; dapr-durabletask-go iso -1; nanobrowser-nanobrowser iso +1 |
| 10 | nanobrowser-nanobrowser | 2.78 | 2 | FLIPS: dapr-durabletask-go iso -1; nanobrowser-nanobrowser iso +1 |
| 11 | getaegis-aegis | 2.20 | 0 | stable |

### Profile: user_facing_app (all requirements; cross-requirement order is indicative only)

| Rank | Codebase | Baseline total | Isolation | Perturbation result |
|---|---|---|---|---|
| 1 | aaif-goose-goose | 3.52 | 2 | stable |
| 2 | datalad-datalad | 2.72 | 1 | stable |
| 3 | nanobrowser-nanobrowser | 2.60 | 2 | stable |

### Profile: dao_contract (all requirements; cross-requirement order is indicative only)

| Rank | Codebase | Baseline total | Isolation | Perturbation result |
|---|---|---|---|---|
| 1 | openwallet-foundation-labs-identity-common-ts | 3.56 | 3 | FLIPS: openwallet-foundation-labs-identity-common-ts iso -1; openwallet-foundation-labs-identity-common-ts@R23 iso +1 |
| 2 | openwallet-foundation-labs-identity-common-ts@R23 | 3.40 | 3 | FLIPS: openwallet-foundation-labs-identity-common-ts iso -1; openwallet-foundation-labs-identity-common-ts@R23 iso +1; openwallet-foundation-labs-identity-common-ts@R23 iso -1; transparency-dev-tessera iso +1 |
| 3 | transparency-dev-tessera | 3.28 | 2 | FLIPS: openwallet-foundation-labs-identity-common-ts@R23 iso -1; transparency-dev-tessera iso +1 |
| 4 | hypercerts-org-hypercerts-lexicon | 2.66 | 0 | FLIPS: mythic-project-spl-governance-v3-1-3 iso +1 |
| 5 | mythic-project-spl-governance-v3-1-3 | 2.54 | 2 | FLIPS: mythic-project-spl-governance-v3-1-3 iso +1 |
| 6 | solana-foundation-rewards | 2.08 | 0 | stable |

### Requirement R01, profile os_kernel (competitors)

| Rank | Codebase | Baseline total | Isolation | Perturbation result |
|---|---|---|---|---|
| 1 | eclipse-biscuit | 3.28 | 2 | stable |
| 2 | getaegis-aegis | 2.20 | 0 | stable |

### Requirement R02, profile os_kernel (competitors)

| Rank | Codebase | Baseline total | Isolation | Perturbation result |
|---|---|---|---|---|
| 1 | anthropics-sandbox-runtime | 3.76 | 3 | stable |
| 2 | convira-convira-sandbox | 3.02 | 3 | stable |

### Requirement R03, profile os_kernel (competitors)

| Rank | Codebase | Baseline total | Isolation | Perturbation result |
|---|---|---|---|---|
| 1 | anthropics-sandbox-runtime@R03 | 3.14 | 2 | stable |
| 2 | getaegis-aegis | 2.20 | 0 | stable |

### Requirement R10, profile os_kernel (competitors)

| Rank | Codebase | Baseline total | Isolation | Perturbation result |
|---|---|---|---|---|
| 1 | openworkflowdev-openworkflow | 3.08 | 1 | stable |
| 2 | dapr-durabletask-go | 2.80 | 1 | stable |

### Requirement R11, profile os_kernel (competitors)

| Rank | Codebase | Baseline total | Isolation | Perturbation result |
|---|---|---|---|---|
| 1 | transparency-dev-tessera | 3.26 | 3 | FLIPS: holepunchto-hypercore iso +1; transparency-dev-tessera iso -1 |
| 2 | holepunchto-hypercore | 3.04 | 2 | FLIPS: holepunchto-hypercore iso +1; transparency-dev-tessera iso -1 |
| 3 | dapr-durabletask-go | 2.80 | 1 | stable |

### Requirement R29, profile user_facing_app (competitors)

| Rank | Codebase | Baseline total | Isolation | Perturbation result |
|---|---|---|---|---|
| 1 | aaif-goose-goose | 3.52 | 2 | stable |
| 2 | nanobrowser-nanobrowser | 2.60 | 2 | stable |

### Requirement R12, profile dao_contract (competitors)

| Rank | Codebase | Baseline total | Isolation | Perturbation result |
|---|---|---|---|---|
| 1 | openwallet-foundation-labs-identity-common-ts | 3.56 | 3 | stable |
| 2 | hypercerts-org-hypercerts-lexicon | 2.66 | 0 | stable |

### Requirement R23, profile dao_contract (competitors)

| Rank | Codebase | Baseline total | Isolation | Perturbation result |
|---|---|---|---|---|
| 1 | openwallet-foundation-labs-identity-common-ts@R23 | 3.40 | 3 | stable |
| 2 | solana-foundation-rewards | 2.08 | 0 | stable |

Totals are indicative. Read the dossiers' section 13 reasons before acting on a rank.
