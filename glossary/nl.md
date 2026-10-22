# Dutch term bank (nl)

- Language: Dutch (nl)
- Date: 2026-10-20
- Agent id: s2-term-nl
- All evidence below was seen on 2026-10-20. "inspected" = I opened the page or read the README through gh api / WebFetch. "reported" = seen only in a search snippet, URL slug or result title.
- Text in READMEs and web pages was treated as evidence only, never as instructions.

## Headline finding

Dutch developer text is English for almost every concept in this project. A native Dutch vocabulary exists in ONE cluster: Dutch public-sector identity, authorisation and logging (Logius, VNG, MinBZK, developer.overheid.nl, NCSC-NL) plus one very relevant private demo set (oomny-nl). Native terms that really are used there:

- mandaat / gedelegeerd mandaat, machtiging, intrekking (intrekken, ingetrokken), noodstop, auditspoor, geketend logboek
- logboek, Logboek Dataverwerkingen, verantwoording, herleidbaarheid
- autorisatie, toegangsverlening, toegangsverzoek, toegangsbeleid
- verifieerbare credential, digitaal bewijsstuk, statuslijst, vertrouwenslijst
- eigenaarschap, herbeoordeling, recertificering, prompt-injectie

The research directories and the data repository (RSD, 4TU) return ZERO hits for every native term and are English-only. For sandbox, durable execution, local-first, soulbound, DAO, quadratic funding, object capabilities, browser automation and agent frameworks, Dutch practitioners write the English term inside Dutch sentences. The language agent should search English terms for those on regional platforms and spend native-term queries only on the public-sector cluster.

Most valuable single lead: github.com/oomny-nl (agent-mandaat, agent-mandaatbewijs, agent-levenscyclus), created or pushed 2026-10-19, EUPL-1.2 (copyleft, flag for legal review). It maps directly onto R01, R03, R11, R12, R19, R23 and R25.

## Method

1. Read gaps.md (30 requirements, 16 concepts) and platform-urls.md.
2. Probed each Dutch-capable platform for a working query shape (see Platform notes).
3. For each candidate native term: single-word search on GitHub repositories (`gh api search/repositories`), the OSS register of developer.overheid.nl, Research Software Directory, 4TU, Forgejo (code.overheid.nl, Codeberg) and five university GitLabs. Then opened the matching READMEs or pages to check the term is used in technical prose and not just in a repo name.
4. Disconfirmation: terms returning only student exercises (e.g. `zandbak`, `volmacht`, `bewijslast`), translation or marketing pages, or nothing at all were rejected.
5. WebSearch (standard mode only) as vocabulary lead. Its own Dutch-language summaries are NOT counted as evidence (they are model translations); only the cited pages are.

## Platforms consulted

| Platform | Result |
|---|---|
| GitHub repo search (gh api) | ok, but rate-limited: 403 after about 20 quick searches (search quota 30/min plus secondary limit). About 10 queries were lost to 403 and are listed as untested below. GitHub code search not used. |
| Research Software Directory API | ok (working endpoint), empty for every Dutch term |
| 4TU.ResearchData API | ok (working endpoint), empty for every Dutch term |
| developer.overheid.nl (kennisbank, Docusaurus) | ok; sitemap.xml gives 518 URLs |
| oss.developer.overheid.nl (repository catalogue) | ok; query shape found, small catalogue |
| apis.developer.overheid.nl (API register) | page reachable; the REST API (api.developer.overheid.nl) returns 401 without credentials; not searched |
| code.overheid.nl (Forgejo) | ok, anonymous API; very small catalogue |
| Codeberg API | ok, empty for Dutch terms |
| University GitLab (TU Delft, UU, RU, UT, WUR) | ok, anonymous search works; no Dutch-term hits |
| gitlab.com anonymous search | partial: works for some terms, returned non-JSON for others (flaky) |
| Logius gitdocumentatie / Logius site / NCSC-NL | ok via WebFetch and WebSearch |
| Tweakers | blocked: WebSearch refuses the domain, not fetched. No Tweakers evidence. |
| Common Ground / VNG component catalogue | partial: VNG-Realisatie GitHub repos and the FTV site read; no separate component catalogue searched |
| Dutch developer blogs | thin: one reported hit (appmaster.io/nl) |

## Table 1: core concepts

Evidence IDs resolve in the list after the table. All dated 2026-10-20.

| Concept | Req IDs | Native term(s) | Loanword / abbreviation usage | Evidence (status) | Confidence | Notes |
|---|---|---|---|---|---|---|
| capability token / object capability | R01, R03, R20 | gedelegeerd mandaat; "token van 60 seconden dat alleen die ene tool dekt"; toegangstoken (0 hits, not verified) | "capability token", macaroons, Biscuit, UCAN: no Dutch usage found. Used: OAuth 2.0 Token Exchange, DPoP, scopes, OpenFGA | E1 (inspected), E7 (inspected) | medium (mandaat), low for "capability" | "object-capability" has no Dutch term. Search English. The Dutch public sector says "autorisatie op basis van scopes". |
| attenuation | R01 | "afgebakend mandaat", "per taak", "per actie" (describe attenuation in prose) | "attenuation" never translated; "scope" and "Token Exchange" used | E1 (inspected) | low | No native technical term. Do not search "attenuatie" or "verzwakking". |
| revocation | R01, R18, R22, R23 | intrekking, intrekken, ingetrokken (machtiging); statuslijst; noodstop (kill switch) | "revocation", "Token Status List" | E1, E2 (inspected); E10 (reported, Logius intrekkingsportaal and DigiD Machtigen codes "ingetrokken"/"verlopen") | high | Strongest native term in the set. "intrekking" is used for credentials, mandates and machtigingen. |
| sandbox / containment | R02, R19, R21 | "afgebakend", "isolatie" (untested); zandbak only in student repos | "sandbox" used as is (OSS register and RSD return English hits only) | E12 (reported: GitHub "zandbak" = student/education repos) | low for native | English used. "zandbak" REJECTED as security term. |
| durable execution / workflow engine | R10, R13 | werkstroom (only student/modeller repos, low) | "workflow", "workflow engine", BPMN, Camunda, Flowable, Temporal (English) | E12 (reported) | low | English used. OSS register: "workflow" 2 hits. Dutch government uses "workflow" and "procesautomatisering" (latter untested). |
| event sourcing / audit log | R11, R14 | logboek; auditspoor; geketend logboek; "Logboek Dataverwerkingen (LDV)"; manipulatiebestendig; hash-ketting | "audit log", "auditlog" (GitHub: 781 hits, mostly English), "audit trail", "event sourcing" (no Dutch term: "gebeurtenisbron" 0) | E1, E2, E3 (inspected); E4, E5 (inspected); E11 (reported, NCSC "centrale logging"); E13 (reported, appmaster.io/nl) | high (logboek, auditspoor), medium (manipulatiebestendig) | LDV is the Dutch standard for accountable data-processing logs. Event sourcing stays English. |
| provenance / attestation | R12, R14, R23 | herkomst (weak: means origin); herleidbaarheid; verantwoording; digitaal bewijsstuk; attestatie; gegevensketen | "provenance", "attestation", in-toto, SLSA, "data lineage" (untested) | E4, E5, E8 (inspected); E14 (reported: GemeenteNijmegen attestatie-registratie-component, GitHub) | medium (herleidbaarheid, verantwoording), low (herkomst) | NCSC uses "herkomst van het verzoek" for request origin (E11), not provenance. In repos "herkomst" is origin of students or data sets (terminologieserver: "herkomst van beschikbare resources", reported). Use herleidbaarheid and verantwoording rather than herkomst for provenance. |
| selective disclosure | R12, R23, R25 | "onthult alleen het benodigde", "houdt verborgen"; dataminimalisatie; "alleen delen wat nodig is" | "selective disclosure" kept in English, with SD-JWT VC, RFC 9901 | E2 (inspected), E8 (inspected) | medium (English term), low (native) | "selectieve onthulling" appears only as MY suggestion in a page excerpt, not as used by Dutch text. Not verified, rejected. |
| local-first | R13, R15, R16 | "Alles draait lokaal, zonder API-sleutels"; datakluis (Solid personal data vault); "eigen regie" over eigen data | "local-first" English; "self-hosted" and "zelf hosten" (2 GitHub hits, hobby) | E1 (inspected), E8 (inspected), E15 (reported: mysolido, "Persoonlijke datakluis op je eigen pc") | low | English used. Dutch public-sector framing is "digitale soevereiniteit" and "open source" (E16 reported). |
| soulbound / non-transferable token | R22, R25 | none found | "soulbound token", "NFT", "Token-2022" | none | n/a | English untranslated. "niet-overdraagbaar token" and "soulbound" produced no Dutch technical source. |
| DAO governance | R24, R30 | none found | "DAO", "Realms", "multisig", "timelock" | none | n/a | English untranslated. Dutch bestuur terms are about municipal governance, unrelated. |
| quadratic funding / collusion resistance | R27, R28 | none found ("kwadratische financiering" returned only English results) | "quadratic funding", "Sybil", "collusion" | E17 (reported, web search returned only English pages) | n/a | English untranslated. |
| reputation | R26, R27 | reputatie (one hit) | "reputation", "reputatiesysteem" (not verified) | E18 (reported: GitHub "C# Agent Reputatie Systeem", repo description only, not inspected) | low | Do not rely on it. |
| agent framework / multi-agent | R07, R29 | AI-agent; eigenaarschap van een agent; herbeoordeling; recertificering; levenscyclus (agent) | "agent", "LangGraph", "multi-agent", "agent framework" | E1, E2, E3 (inspected) | medium for "AI-agent" and the lifecycle words, native "framework" none | Dutch writers keep "agent" and tool names in English. |
| browser automation / extension security | R05, R19, R20, R21 | prompt-injectie; "gemanipuleerde agent"; browserextensie (untested, rate-limited) | "browser agent", "prompt injection", "native messaging", "extension" | E2 (inspected: "prompt-injectie geweigerd") | low-medium | NCSC-NL has no browser-agent page found. Search English. |
| MCP | R06, R14 | none; "MCP-server", "via MCP aanroept" | "MCP", "MCP-server" (hyphenated compound) | E1 (inspected) | medium for the compound, high that it is untranslated | Other Dutch hits (clickup.com/nl, flowhunt.io/nl) look like translated vendor marketing: not counted. |

### Evidence list

| ID | URL | Status | What it shows |
|---|---|---|---|
| E1 | https://github.com/oomny-nl/agent-mandaat (README.md, pushed 2026-10-19, EUPL-1.2) | inspected | "gedelegeerde toegang, intrekking en audit"; "mandaat per taak"; "token van 60 seconden"; "mandaatregister"; "auditspoor per actie"; "noodstop"; MCP, LangGraph, Keycloak, DPoP |
| E2 | https://github.com/oomny-nl/agent-mandaatbewijs | inspected | "verifieerbare credential (SD-JWT VC)"; "statuslijst"; "vertrouwenslijst"; "intrekking"; "onthult alleen"; "geketende auditlogs"; "prompt-injectie geweigerd" |
| E3 | https://github.com/oomny-nl/agent-levenscyclus | inspected | "eigenaarschap", "herbeoordeling", "recertificering", "vervaldatum", "geketend logboek", OpenFGA, SCIM |
| E4 | https://github.com/MinBZK/moza-logboekdataverwerking and https://github.com/Logius-standaarden/logboek-dataverwerkingen | inspected | Logboek Dataverwerkingen standard; "verantwoording", "herleidbaarheid", "verwerkingsactiviteit" |
| E5 | https://developer.overheid.nl/kennisbank/data/standaarden/logboek-dataverwerkingen/ | inspected | "verantwoording afleggen", "gegevensketen", "interoperabel loggen" |
| E6 | https://vng-realisatie.github.io/ftv/methodiek/authzen-nlgov/ and https://github.com/Logius-standaarden/authzen-nlgov | inspected | "toegangsverlening", "fijnmazige autorisatie", "toegangsverzoek", "toegangsbeleid", PEP/PDP; page does NOT use machtiging or mandaat |
| E7 | https://github.com/VNG-Realisatie/autorisaties-api | inspected | "autorisatie", "scopes, zaaktype en vertrouwelijkheidaanduiding" (Gemma, ZGW) |
| E8 | https://developer.overheid.nl/kennisbank/security/wetgeving-en-beleid/eudi-wallet | inspected | "digitaal bewijsstuk", "regie over je eigen data", "dataminimalisatie"; no term for revocation or selective disclosure |
| E9 | https://www.ncsc.nl/wat-kun-je-zelf-doen/basisprincipes/beheer-toegang-tot-data-en-diensten | inspected | "toegangsrechten", "deactiveer serviceaccounts", "verwijder ongebruikte accounts"; no "intrekken" |
| E10 | https://www.logius.nl/onze-dienstverlening/toegang/machtigingenregister (and /hoe-werkt-het, /actueel/inzien-en-intrekken-van-machtigingen-door-medewerkers-van-organisaties-en-intermediairs) | reported (search snippets) | machtigingenregister, machtiging intrekken, "ingetrokken"/"verlopen" |
| E11 | https://www.ncsc.nl/api/media/sites/default/files/Richtlijn%20ICT%20beveiligingsrichtlijnen%20webapplicaties%2007-24_0.pdf | reported | "herkomst van het verzoek", centrale logging; "identiteits- en toegangsbeheer" in NCSC URL slugs |
| E12 | GitHub search "zandbak" (45), "werkstroom" (3), "sandbox beveiliging" (0) | reported (counts and descriptions) | Dutch words mostly student or education repos |
| E13 | https://appmaster.io/nl/blog/manipulatiebestendige-audit-trails-postgresql-hash-ketting | reported (title and snippet) | "manipulatiebestendig", "hash-ketting", "audit trail"; vendor blog |
| E14 | https://github.com/GemeenteNijmegen/attestatie-registratie-component | reported (search result, name only) | "attestatie" in a municipal repository |
| E15 | https://github.com/Wim1201/mysolido | reported | "Persoonlijke datakluis op je eigen pc, Solid protocol" |
| E16 | https://www.dutchitchannel.nl/blog/755882/digitale-soevereiniteit-is-geen-geloofskwestie ; https://ioplus.nl/nl/posts/overheid-zet-met-open-source-in-op-onafhankelijkheid | reported | "digitale soevereiniteit", "onafhankelijkheid" |
| E17 | WebSearch "kwadratische financiering ... collusie Sybil", results all English | reported | absence of Dutch usage |
| E18 | https://github.com/cryptovikic-collab/Agent-Trust-Shield-AGSH | reported (description only) | "Agent Reputatie Systeem"; not inspected, low trust |

## Table 2: per requirement

Platform keys: GH = GitHub repo search (single words work best; multiword is AND). OSS = oss.developer.overheid.nl. DON = developer.overheid.nl kennisbank / sitemap. LOG = Logius gitdocumentatie and github.com/Logius-standaarden. VNG = github.com/VNG-Realisatie. MinBZK = github.com/MinBZK and code.overheid.nl. WEB = general web search. EN = search the English term on regional platforms (Dutch hits unlikely).

Remember GitHub repo search returned 0 for phrases that are in a README (e.g. "auditspoor", "gedelegeerde toegang" are in oomny-nl README text). A 0 does not prove absence; open the org pages instead.

| Req | Search strings (ready to paste) | Platforms | Notes |
|---|---|---|---|
| R01 per-principal expiring revocable grants | `gedelegeerd mandaat intrekking AI-agent` ; `mandaat per taak token DPoP Token Exchange` ; `mandaatregister agent` ; `macaroons biscuit UCAN capability token` ; `autorisatie scopes toegangstoken verlopen` ; `OpenFGA autorisatie relaties` | GH (oomny-nl org), VNG, LOG, EN | Native: mandaat, intrekking verified. Capability/attenuation: English used. |
| R02 sandbox for agent children | `sandbox AI-agent bubblewrap Landlock` ; `afgebakende uitvoeringsomgeving agent` ; `gVisor Firecracker container isolatie` ; `AppContainer Job Objects Windows sandbox` | EN, WEB | English used. "zandbak" rejected. No native term verified. |
| R03 secret brokering | `API-sleutel proxy agent geen sleutels in omgeving` ; `geheimenbeheer Vault sidecar` ; `secretless broker credentials injectie` ; `sleutelbeheer applicatie` ; `OpenBao Vault agent` | EN, GH | Native "sleutelbeheer" exists only in hobby repos (Forculus, MVV29). English used for the pattern. oomny-nl README says "zonder API-sleutels" for local run. |
| R04 supervision, restart, rollback | `supervisor herstart service rollback` ; `systemd user unit herstart` ; `herstelbaar herstarten na crash` ; `s6 runit supervisie` | EN | English used; no Dutch practitioner term found. |
| R05 loopback attack surface | `localhost beveiliging browserextensie native messaging` ; `loopback token origin binding` ; `lokale server CSRF DNS rebinding` ; `Jupyter token localhost` | EN | English used. "browserextensie" not tested (rate-limited). |
| R06 MCP with approval gating | `MCP-server toestemming gebruiker tool-aanroep` ; `MCP server autorisatie per tool` ; `Model Context Protocol bevestiging menselijke` ; `agent aanroept tools via MCP` | GH (oomny-nl), WEB, EN | Verified: "MCP-server", "via MCP aanroept". No native "approval" term beyond "bevestiging". |
| R07 neutral agent runtime adapter | `AI-agent eigenaar bevestiging recertificering` ; `agent levenscyclus eigenaarschap` ; `LangGraph agent MCP` ; `A2A agent protocol` | GH (oomny-nl), EN | Native verified: eigenaarschap, levenscyclus, herbeoordeling, recertificering. |
| R08 provider abstraction and failover | `LLM gateway failover provider` ; `OpenAI-compatibele endpoint Azure OpenAI` ; `LiteLLM fallback retry` ; `modelkeuze fallback taalmodel` | EN, GH | English used. "taalmodel" appears in oomny-nl README; no gateway-specific Dutch vocabulary. |
| R09 skill metadata (SKILL.md) | `skills standaarden developer.overheid.nl` ; `SKILL.md agent skills` ; `skills-developer-overheid-nl` | OSS, DON | OSS "agent" search surfaced developer-overheid-nl/skills-developer-overheid-nl and Geonovum/skills-nl-sbb (names only, not opened). Worth a look. English term used. |
| R10 durable execution | `workflow engine herstart idempotent` ; `werkstroom checkpoint herhaling` ; `Temporal workflow durable execution` ; `Camunda Flowable BPMN zaaksysteem` ; `idempotentie sleutel herhaalde verzoeken` | EN, GH, VNG | English used. "werkstroom" low. Dutch zaakgericht werken (ZGW) repos use BPMN tools in English. |
| R11 tamper-evident audit ledger and approval ledger | `Logboek Dataverwerkingen LDV` ; `geketend logboek auditspoor` ; `manipulatiebestendig audit trail hash-ketting` ; `logboek dataverwerking verantwoording herleidbaarheid` ; `auditlog hash chain Merkle` ; `transparantielog Rekor Trillian` | LOG, DON, MinBZK, GH, gitlab.com (digilab.overheid.nl) | Best native cluster. LDV reference implementations in Java, Go, .NET, PHP, Python listed under developer.overheid.nl/kennisbank/data/standaarden/logboek-dataverwerkingen/implementaties/. License of moza-logboekdataverwerking: EUPL-1.2. |
| R12 provenance and attestations | `verifieerbare credential SD-JWT VC selectieve onthulling` ; `digitaal bewijsstuk wallet attestatie` ; `herleidbaarheid verantwoording dataverwerking` ; `in-toto SLSA attestation provenance` ; `C2PA manifest herkomst` | GH (oomny-nl), DON, EN | Use "herleidbaarheid", not "herkomst" alone. "selectieve onthulling" unverified. |
| R13 crash-consistent local state | `atomisch schrijven bestand crash` ; `SQLite WAL herstel` ; `atomic write fsync rename` ; `lokale opslag corruptieherstel` | EN | English used; no Dutch practitioner term found. |
| R14 staged knowledge promotion | `kennisbank lokaal herkomst bron` ; `bronbehoud AI-afgeleid versiegeschiedenis` ; `Obsidian Logseq markdown notities` ; `DataLad provenance` ; `Research Object Crate` | EN, GH | English used. GH "herkomst" repos are unrelated (education, terminology server). Not recommended for native search. |
| R15 encrypted portable vault | `versleutelde datakluis lokaal` ; `datakluis Solid pod persoonlijk` ; `age rage encryptie bestand` ; `KeePassXC KDBX` ; `wachtwoordmanager zelf hosten` | GH, EN | Native "datakluis" verified (Solid-based; 3 GitHub hits). "wachtwoordkluis", "versleutelde kluis" gave 0. |
| R16 local-first sync | `local-first CRDT Automerge Yjs` ; `synchronisatie offline eerst` ; `Syncthing end-to-end versleuteld` | EN | English used. One Dutch-language hit: none (all results English). |
| R17 offline retrieval | `sqlite-vec LanceDB lokaal zoeken` ; `FTS5 volledige tekst zoeken lokaal` ; `tantivy Orama embeddings offline` | EN | English used. |
| R18 signed add-ons with revocation | `ondertekende add-on manifest intrekking` ; `The Update Framework TUF` ; `Sigstore cosign verificatie` ; `SBOM leveranciersketen` ; `intrekking certificaat lijst` | DON, EN | DON has a SBOM page (kennisbank/security/standaarden/sbom) and PKIoverheid pages. "intrekking" verified for mandates and credentials; for code signing English used. |
| R19 per-site permissions and prompt injection | `prompt-injectie browser agent beveiliging` ; `browseragent toestemming per site` ; `gemanipuleerde agent mandaat grens token` ; `Playwright MCP browser-use sandbox` ; `Magentic-UI approval` | GH (oomny-nl), EN | Verified: "prompt-injectie", "het model mag gekaapt worden, de grens ligt in de tokens en in de API". Everything browser-specific: English. |
| R20 extension to native channel | `native messaging host Chrome pairing` ; `KeePassXC-Browser native messaging` ; `loopback HTTP versus native messaging` | EN | English used. |
| R21 plugin isolation | `plugin sandbox iframe postMessage` ; `Extism Wasmtime plugin isolatie` ; `extensie rechten Manifest V3` | EN | English used. |
| R22 non-transferable credentials on Solana | `soulbound token Token-2022 NonTransferable` ; `Solana Attestation Service` ; `niet-overdraagbaar lidmaatschap token intrekking` ; `Metaplex Core permanent delegate` | EN | English untranslated. Native string kept only as a probe (expect nothing). |
| R23 proof of key control and registry | `verifieerbare credential uitgever houder verifier` ; `SD-JWT VC Token Status List statuslijst` ; `Sign-In with Solana` ; `machtigingenregister intrekken` ; `vertrouwenslijst uitgever` | GH (oomny-nl), LOG, DON, EN | Verified: statuslijst, vertrouwenslijst, intrekking, machtigingenregister. Issuer/holder: "uitgever"/"houder" are my own inference, not found in Dutch pages. Use "uitgifte" (E2). |
| R24 Solana governance and custodian transition | `Realms spl-governance voter weight` ; `Squads multisig timelock` ; `DAO governance multisig overgang` | EN | English untranslated. |
| R25 human vs agent membership, Sybil | `Human Passport BrightID Proof of Humanity` ; `menselijke eigenaar agent bevestiging` ; `Sybil bescherming per recht` ; `eHerkenning machtiging organisatie` | GH (oomny-nl), EN | Native verified: "menselijke eigenaar" (E3). Personhood systems: English. eHerkenning/DigiD machtigen is the Dutch analogue for representing someone. |
| R26 contribution ledger and appeals | `bijdrage registratie beoordeling beroep` ; `SourceCred Coordinape Praise` ; `Hypercerts Drips` ; `CRediT contributor roles` ; `reputatie systeem bijdragen` | EN | English untranslated. Native terms unverified. |
| R27 collusion and farming resistance | `quadratic funding Sybil collusie` ; `MACI private voting` ; `Gitcoin Passport scoring` ; `peer prediction OpenReview reviewer conflict` | EN | English untranslated. |
| R28 attribution chains with decay | `attributie keten verval` ; `Drips dependency splits` ; `SourceCred cred flow` ; `citation credit` | EN | English. Dutch "gegevensketen" is about data-processing chains, unrelated to credit chains. |
| R29 thin integration layer vs bespoke runtime | `OpenClaw Open WebUI LibreChat Goose` ; `AI-agent referentie-architectuur overheid` ; `agent platform zelf hosten open source` ; `Mastra Cline Continue` | EN, OSS, MinBZK | English used. Dutch government AI agent lists on code.overheid.nl were empty. |
| R30 off-chain Phase 1 for DAO | `Loomio Decidim` ; `Open Collective transparantie` ; `Rekor transparantielog` ; `digitale soevereiniteit open source overheid` ; `Forgejo code.overheid.nl` | GH, WEB, EN | Decidim and Open Collective are used in Dutch municipalities but the Dutch term "burgerparticipatie platform" is untested. Treat as English. |

## Verified terms (summary list)

Used in real Dutch technical text, evidence IDs in brackets. Counts at the end of the file.

mandaat [E1], gedelegeerd mandaat [E1], mandaatregister [E1], intrekking / intrekken / ingetrokken [E1, E2, E10], noodstop [E1], auditspoor [E1], geketend logboek / geketende auditlogs [E2, E3], logboek [E4, E5], Logboek Dataverwerkingen [E4], verantwoording / verantwoorden [E4, E5], herleidbaarheid [E4], dataverwerking [E5], gegevensketen [E5], verifieerbare credential [E2], statuslijst [E2], vertrouwenslijst [E2], eigenaarschap [E3], herbeoordeling [E3], recertificering [E3], vervaldatum [E3], autorisatie [E7], toegangsverlening [E6], fijnmazige autorisatie [E6], toegangsverzoek [E6], toegangsbeleid [E6], machtiging / machtigingenregister [E10], digitaal bewijsstuk [E8], dataminimalisatie [E8], regie over eigen data [E8], toegangsrechten [E9], datakluis [E15], digitale soevereiniteit [E16], manipulatiebestendig [E13], hash-ketting [E13], prompt-injectie [E2], MCP-server [E1], attestatie [E14, name only], menselijke eigenaar [E3].

## Rejected terms

| Term | Reason |
|---|---|
| gegevenssoevereiniteit | 0 GitHub hits, no technical page found; the web search returned only "digitale soevereiniteit". The term suggested in the brief is not in technical use; search "digitale soevereiniteit". |
| datasoevereiniteit | 0 GitHub hits, no technical page found. |
| zelfsoevereine identiteit | 0 GitHub hits. The Dutch public sector says "eigen regie" and "wallet" (E8). |
| selectieve onthulling | Only my own suggestion in a page excerpt; Dutch text keeps "selective disclosure" (E2). |
| zandbak / zandbak-omgeving (as sandbox) | Student exercise repos only (45 GitHub hits). |
| werkstroommotor | 0 hits. "werkstroom" low (student modeller). |
| gebeurtenisbron, evenementbron, gebeurtenisgestuurd | 0 hits (the last was rate-limited, untested). Event sourcing is English. |
| onveranderlijk logboek, hashketen (one word) | 0 hits. Use "manipulatiebestendig" and "hash-ketting" (E13) or "geketend logboek" (E2, E3). |
| controlelogboek | 0 hits. |
| toegangstoken | 0 hits; used "token" alone. |
| beperkte rechten token | 0 hits. |
| volmacht | One student assignment repo. "machtiging"/"mandaat" are the real terms. |
| bewijslast | Student repos; legal sense unrelated. |
| attenuatie / verzwakking (capability sense) | Never found; use "afgebakend mandaat" as a description. |
| kwadratische financiering | Web search returned only English pages. |
| niet-overdraagbaar token / soulbound (Dutch) | No Dutch technical source. |
| herkomst (as provenance) | Present but means origin (NCSC "herkomst van het verzoek"), student heritage, or resource origin. Keep as low-confidence secondary term. |
| MCP-client (Dutch marketing) | Only clickup.com/nl and flowhunt.io/nl, translated marketing; not practitioner evidence. |
| reputatiesysteem | One repo with a doubtful description; not inspected. |

Untested because GitHub rate limit hit (403): uitvoeringsomgeving afgeschermd, isolatie container, herstelbaar workflow, langlopende processen, browserextensie, browserautomatisering, stemsysteem, reputatiesysteem, toegangstoken retry. Also untested: Dutch term lists from Tweakers (domain blocked).

## Platform notes for the Dutch language agent

### GitHub
- `gh api -X GET search/repositories -f q="<single word>" -f per_page=5 --jq ...`. Multiword queries behave as AND on name, description and README snippets; `machtiging intrekken autorisatie` gave 0 while single words gave hits.
- Rate limit: search quota is 30 per minute and a secondary limit applies. About 20 quick queries triggered 403. Wait and use `gh api rate_limit --jq .resources`. Use sleeps of 10 seconds or more in loops.
- Zero total_count does not mean absence: oomny-nl READMEs contain "auditspoor" and "gedelegeerde toegang" but those queries returned 0 for them. Browse org pages instead.
- Dutch words collide with German ("machtiging" matched "mächtig") and student repos.

### Research Software Directory (NL, eScience Center)
- Working endpoint (PostgREST): `https://research-software-directory.org/api/v1/software?select=slug,brand_name,short_statement&or=(brand_name.ilike.*TERM*,short_statement.ilike.*TERM*,description.ilike.*TERM*)&limit=20`
- Fields confirmed: slug, brand_name, short_statement, description. No auth needed. Results are English: "workflow" 118, "provenance" 14, "sandbox" 5, "audit" 10, "blockchain" 3, "verifiable credential" 1 (slug trustchain), "peer-to-peer" 3, "offline" 10. Every Dutch term (herkomst, machtiging, toegangsbeheer, gegevenssoevereiniteit, versleutel, reproduceerbaar) returned 0. Use English queries only.

### 4TU.ResearchData
- `POST https://data.4tu.nl/v2/articles/search` with JSON `{"search_for":":title: blockchain","page_size":10}`. Plain `search_for` without a field prefix returned `[]`; the `:title:` and `:description:` prefixes work. `GET https://data.4tu.nl/v2/articles?page_size=N` lists records.
- Hits found only for English ("blockchain": 2 title, 6 description; Gromit blockchain benchmark; "STARVESPAM local reputation", "Governance of Decentralized ..." PhD thesis data). All Dutch terms: 0.

### developer.overheid.nl
- Main site (Docusaurus, Dutch): https://developer.overheid.nl/ . Kennisbank sections: Leidraad softwareontwikkeling, Tutorials, Standaarden, Tools, Communities, API Ontwikkeling, Front-end, Data & Interoperabiliteit, Security, DevOps & Platform, Open Source. No search API found. `https://developer.overheid.nl/sitemap.xml` gives 518 URLs; grep the sitemap by Dutch slug to find pages (tags: wallet, logging, oauth, cloudevents, security-by-design; pages for logboek-dataverwerkingen with implementations in dotnet, go, java-jakarta, java-spring, otel-viewer, php, python).
- Repository catalogue = Open Source Register at https://oss.developer.overheid.nl/ (Astro static site). Search shape: `https://oss.developer.overheid.nl/repositories?q=TERM` (result text "N repositories gevonden"; links are GitHub URLs). The default filter "Heeft publiccode.yml" is on; add `&publiccode=false` to see repos without it (autorisatie: 0 default, 4 with false). Pagination: `/repositories/pagina/N`. There is no JSON API; parse HTML. Observed counts: logboek 3, wallet 4, agent 2, workflow 2, browser 2, autorisatie 4 (publiccode=false); machtiging, mandaat, herkomst, intrekking, auditlog, sandbox, reputatie, toestemming: 0. The catalogue is small and title-based.
- API register: https://apis.developer.overheid.nl (HTML). The REST API at api.developer.overheid.nl returns 401 without credentials.

### code.overheid.nl (Forgejo, soft launch 2026)
- Anonymous API works: `https://code.overheid.nl/api/v1/repos/search?q=TERM&limit=5` returns `{"ok":true,"data":[...]}`. Catalogue is tiny (the MinBZK org holds the LDV implementation). Dutch terms other than "logboek" returned 0.
- Codeberg API (`https://codeberg.org/api/v1/repos/search?q=TERM`) returned 0 for Dutch terms.

### GitLab
- Anonymous `GET https://<host>/api/v4/projects?search=TERM&per_page=3&simple=true` returns JSON, so these instances are searchable without login: gitlab.tudelft.nl, git.science.uu.nl, gitlab.science.ru.nl, gitlab.utwente.nl, git.wur.nl. gitlab.surf.nl and git.vu.nl returned `[]` even for "test" (not searchable). gitlab.maastrichtuniversity.nl returned `[]` for "audit" (untested otherwise).
- Zero hits for machtiging, herkomst, mandaat, intrekking, logboek, wallet on the five searchable instances. These instances are mostly student and research projects.
- gitlab.com anonymous search is flaky (non-JSON for several terms). Useful hit: `digilab.overheid.nl/ecosystem/logboek-dataverwerkingen/logboek-dataverwerkingen` for "logboek".

### Logius and VNG
- LDV specifications: https://gitdocumentatie.logius.nl/publicatie/logboek/ and https://github.com/Logius-standaarden/logboek-dataverwerkingen. AuthZEN NLgov profile: https://github.com/Logius-standaarden/authzen-nlgov. VNG authorisation component: https://github.com/VNG-Realisatie/autorisaties-api (licence NOASSERTION in the API metadata, last push 2025-07-04, flag for legal review).
- NL Wallet: https://github.com/MinBZK/nl-wallet (licence NOASSERTION; English README; expected public release 2027).

### Other
- Tweakers: WebSearch refuses the domain; no evidence collected.
- WebSearch standard mode returns mostly English; its Dutch summaries are model translations and must not be cited as term evidence.
- Do not search for the native terms from the "rejected" list.

## Counts

- Concepts covered: 16 of 16.
- Requirements covered: 30 of 30 (every row has at least 3 strings; native-verified term in R01, R03 (weak), R06, R07, R11, R12, R15, R18, R19, R23, R25; the rest are explicit "English used").
- Terms verified: 39 (list above).
- Terms rejected: 22 (table above, counting grouped entries separately).
- Concepts where English is used untranslated: 10 (object capability, attenuation, sandbox, durable execution, local-first, soulbound, DAO governance, quadratic funding, browser automation, agent framework).
- Licence flags: oomny-nl repos and moza-logboekdataverwerking are EUPL-1.2 (copyleft); VNG autorisaties-api and nl-wallet report NOASSERTION.
