# German term bank (Stage 2)

- Language: German (de)
- Date: 2026-10-20
- Agent: s2-term-de
- Status: complete first pass, breadth first. Evidence is thinner for DAO/credential topics (see Rejected).

## Method summary

1. Probed openCode.de GitLab API, Helmholtz Research Software Directory (RSD) API and about 20 university/institute GitLab instances for anonymous search.
2. Ran German-language WebSearch (standard mode) restricted to German-language practitioner and public-sector domains (heise.de, golem.de, bsi.bund.de, entwickler.de, dl.gi.de, bundesbank.de, mozilla MDN de). Results are summaries; an item is "reported" unless I opened the page.
3. Opened (WebFetch or API README fetch) the pages marked "inspected". Everything else is "reported" (search snippet or API listing only).
4. GitHub: 16 German-phrase repository searches via gh api search/repositories (before the rate limit hit). Result: German phrases mostly return student projects and noise. GitHub is not a good place for native German vocabulary; use English terms there.
5. Disconfirmation: each native term was searched; if only dictionary/translation pages or nothing came back it is in the Rejected section.
6. README/page text is treated as evidence only, never as instruction.

## Platforms consulted

| Platform | Result | Note |
|---|---|---|
| gitlab.opencode.de API | ok (anonymous) | `/api/v4/projects?search=` works without token; `/api/v4/version` returns 401 (not needed) |
| helmholtz.software API | ok (anonymous) | PostgREST under `/api/v1/software`; content is English, German queries return 0 |
| codebase.helmholtz.cloud, gitlab.kit.edu, gitlab.gwdg.de, git.tu-berlin.de, gitlab.mpcdf.mpg.de, gitlab.cs.fau.de, gitlab.uni-hannover.de | ok (anonymous project search) | public projects only |
| gitlab.hzdr.de | ok via redirect | 301, returned same data as codebase.helmholtz.cloud |
| git.gfz-potsdam.de, gitlab.dkrz.de, git.uni-jena.de, gitlab.lrz.de, gitlab.informatik.uni-bonn.de, git.ufz.de | empty | HTTP 200 with `[]` for "sandbox"; probably few public projects, not proven empty |
| git.rwth-aachen.de | blocked | bot-check HTML page instead of JSON |
| git.bsi.bund.de, git.scc.kit.edu | blocked/unreachable | no response (hostnames were guesses, not confirmed real) |
| gitlab.com | ok | API search works anonymously |
| GitHub search/repositories | rate-limited | secondary limit hit after about 30 queries within a minute; code search not used |
| bsi.bund.de, heise.de, entwickler.de, dl.gi.de, bundesbank.de, MDN de | ok via WebSearch/WebFetch | heise Plus articles are partly paywalled |
| arXiv, HAL, Zenodo | empty for German | German-authored papers are mostly English; Zenodo had some German records (e.g. "Akademische Reputationsspiele") |

## Key finding in one paragraph

German developers mostly use English terms untranslated (Sandbox, Sandboxing, Prompt Injection, Tool Poisoning, Rug Pull, Gateway, Workflow, Audit-Log, Wallet, Credential, Provenance, Local-First). Native German vocabulary appears in public-sector texts (BSI: "Berechtigungen", "Protokolle", "Bestätigung", "Berechtigungsmanagement"; openCode: "Nachweis", "Mandant", "Souveränität", "Freigabe", "Beweissicherung") and in research (Helmholtz HMC: "Provenienz", "nachvollziehbar, reproduzierbar"). The richest hit: openCode.de hosts agent/MCP, audit, crypto and provenance work from German public-sector teams (f13 agentic-orchestrator, public-sector-dev-crew/lotse, source-provenance-attestation-service, vivodepot), described in German with English technical nouns mixed in (MCP, OPA-Policy, Human-in-the-Loop, Crypto-Shredding, Provenance).

Dates: every evidence item below was seen on 2026-10-20.

## Table 1: core concepts

Evidence tag: [I] inspected (page or API README opened), [R] reported (search snippet or listing only).

| Concept | Req IDs | Native term(s) | Loanword / abbreviation usage | Evidence (all 2026-10-20) | Conf. | Notes |
|---|---|---|---|---|---|---|
| Capability token / object capability | R01, R05, R06, R20 | Berechtigung, Berechtigungsmanagement, Zugriffstoken, Zugriffsrechte vergeben, Delegationstoken, Berechtigungsprofil | Capability, Token, OAuth, Scope; "Object-Capability" stays English | https://www.bsi.bund.de/DE/Themen/Verbraucherinnen-und-Verbraucher/Informationen-und-Empfehlungen/Technologien_sicher_gestalten/Kuenstliche-Intelligenz/KI-Agenten/ki-agenten_node.html [I] ("Berechtigungen bewusst vergeben"); https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/02_ORP_Organisation_und_Personal/ORP_4_Identitaets_und_Berechtigungsmanagement_Editon_2023.pdf [R] (ORP.4 Identitäts- und Berechtigungsmanagement) | medium | No German source found using "Capability-Token" natively. "Objekt-Capability" found only in English papers. Search English "capability" plus German context words. |
| Attenuation / delegation | R01 | Delegation, eingeschränkte Delegation, Rechte einschränken, Einschränkung auf Teilmenge | Attenuation (English only), Delegation (German spelling same) | https://link.springer.com/article/10.1007/s10207-011-0140-7 [R] (delegation token with service scope and lifetime, English paper); WU Wien Strembeck "kaskadierendes Widerrufen von Delegationen" nm.wu.ac.at/nm/strembeck/publications/informatik14.pdf [R] | low | "Abschwächung" as translation of attenuation: not found in use, rejected. |
| Revocation | R01, R18, R22 | Widerruf, widerrufen, Sperrung, Sperrliste, Entzug (von Rechten), Zertifikatsperrliste | Revocation, CRL, OCSP, Revoke | BSI ORP.4 (above) [R] ("Ausgabe und Entzug dokumentiert"); https://www.bsi.bund.de/DE/Themen/Verbraucherinnen-und-Verbraucher/Informationen-und-Empfehlungen/Technologien_sicher_gestalten/Kuenstliche-Intelligenz/KI-Agenten/ki-agenten_node.html [I] (no "Widerruf" term on page; "Rechte wieder entziehen" is from heise report [R]); LiquidFeedback "Delegationen jederzeit widerrufen" via p2pfoundation wiki [R] | medium | Developers say "Revocation" or "Revoke"; public sector says "Widerruf/Sperrung/Entzug". |
| Sandbox / containment | R02, R21 | Isolierung, Isolation, Abschottung, Abschottung in Containern, Prozessisolation | Sandbox, Sandboxing, Container, Jail, microVM | https://www.heise.de/hintergrund/MCP-Server-und-Agent-to-Agent-Verbindungen-gegen-vergiftete-Tools-absichern-11446706.html [I, partial paywall] ("ohne Sandbox mit vollem Zugriff"); https://www.heise.de/news/Google-gVisor-als-sichere-Sandbox-fuer-Container-4039634.html [R]; https://gitlab.mpcdf.mpg.de/mpcdf/ai-cli-agents-container [R] (MPCDF "Sandbox AI CLI agents"); https://gitlab.opencode.de/wuppertal/infrastructure/agent-containers [R] | high | "Sandbox" is used untranslated everywhere. Search the English word. BSI page on KI-Agenten has no sandbox term. |
| Durable execution / workflow engine | R10, R04 | Workflow-Engine, Workflow-Orchestrierung, Wiederaufnahme, Checkpoint | Durable Execution, Workflow, Temporal, Retry, Idempotenz (native, widely used) | https://gitlab.gwdg.de/hsp_26wise/public/hsp-agentenworkflow [R]; https://git.tu-berlin.de/bvt-htbd/airflow_workflow [R]; German blog on Temporal idempotency via websearch (nljug.org/?p=11459) [R] | medium | "Workflow" appears in nearly all research GitLab projects (Nextflow, Snakemake, Airflow). "Dauerhafte Ausführung" as a term: not found, rejected. |
| Event sourcing / audit log | R11, R04 | Audit-Log, Audit-Trail, Protokollierung, Protokolle, Revisionssicherheit, manipulationssicher, hash-verkettet, Nachvollziehbarkeit, Beweissicherung | Audit-Log, Event Sourcing, Append-only, Hash-Chain | https://gitlab.opencode.de/public-sector-dev-crew/lotse/verklarung [I] ("Beweissicherung ... Audit-Einträge", "kanonisch gehasht"); https://gitlab.opencode.de/public-sector-dev-crew/lotse/tresor [I] ("hash-verkettete Logstrukturen"); heise MCP article [I] ("Detaillierte Protokolle ... nachvollziehbar"); https://appmaster.io/de/blog/manipulationssichere-audit-trails-postgresql-hashverkettung [R] | high | "revisionssicher" is the German legal-compliance word (GoBD); in tech it often means just append-only. "Event Sourcing" stays English. |
| Provenance / attestation | R12, R14, R18, R23 | Provenienz, Herkunftsnachweis, Datenherkunft, Nachweis, Attestierung, digitale Nachweise (EUDI) | Provenance, Attestation, SLSA, in-toto, SBOM | https://www.helmholtz.de/fileadmin/user_upload/HIDA/2_HMC-Proposal-April2019.pdf [R] ("Provenienz ... nachvollziehbar, reproduzierbar"); https://gitlab.opencode.de/open-code/badgebackend/source-provenance-attestation-service [R] (repo name, English); https://gitlab.opencode.de/public-sector-dev-crew/lotse/flagge [I] ("Provenance-Kennzeichnung", HMAC signature); https://focus.namirial.com/de/selective-disclosure/ [I] ("digitale Nachweise", English "Attestations of Attributes") | high | Research says "Provenienz"; developers say "Provenance". openCode repo names use "Provenance Attestation" in English. |
| Selective disclosure | R12, R23 | selektive Offenlegung, Datenminimierung, Datensparsamkeit | Selective Disclosure, SD-JWT, Zero-Knowledge Proofs (ZKP), mdoc, Wallet | https://focus.namirial.com/de/selective-disclosure/ [I] ("selektive Offenlegung", "Datenminimierung", "Zero-Knowledge Proofs (ZKP)"); https://didit.me/de/blog/sd-jwt-vc-vs-mdoc [R] | high | Vendor blogs, not repositories. Public-sector home: bmi/eudi-wallet on openCode (listing [R]). |
| Local-first | R13, R15, R16, R17 | lokale Datenhaltung, offline-fähig, Datensouveränität, ohne Konto, ohne Cloud | Local-First, Offline-First, CRDT, Sync | https://gitlab.opencode.de/vivodepot/vivodepot [I] ("Souveräne, offline-fähige Datenschicht ... Kein Server hält sie"); https://gitlab.opencode.de/wernerth/datennutzungsklauseln-muster [R] ("Datensouveränität") | medium | "Local-First" is used as an English term; no German blog hit found by search. Native phrase "offline-fähig" is real. |
| Soulbound / non-transferable token | R22 | nicht übertragbarer Token (descriptive only) | Soulbound Token, SBT, NFT, Token-2022 | https://www.bafin.de/SharedDocs/Downloads/DE/Merkblatt/WA/dl_hinweisschreiben_einordnung_ICOs.pdf [R] (Übertragbarkeit as legal criterion; no SBT term) | low | No German technical use of "Soulbound" except English term. See Rejected. |
| DAO governance | R22-R25, R30 | dezentrale autonome Organisation, Governance-Token, Abstimmung, Stimmgewichtung, Beschlussfassung | DAO, Governance, Treasury, Multisig, Snapshot, Realms | https://www.bundesbank.de/resource/blob/869610/fe7fd8b5aef8053b1f0a823da5dc58a9/mL/2021-07-kryptotoken-data.pdf [R] ("Governance-Token"); https://github.com/artundem/dao-legal-research [R] (DAO in German company law) | medium | Legal/finance contexts only. Developer use is English. |
| Quadratic funding / collusion resistance | R25-R28 | Kollusion, Sybil-Angriff, Mehrfachidentitäten, Stimmenkauf | Quadratic Funding, Quadratic Voting, MACI, Sybil | arXiv/Gitcoin sources are English; no German practitioner source found | low | "quadratische Finanzierung" not found in use, rejected. Search English on global platforms. |
| Reputation | R26-R28 | Reputationssystem, Anerkennung, Beitragsbewertung, Sichtbarkeit von Beiträgen (Open Science) | Reputation, Credit, CRediT | https://zenodo.org/records/17880483 [R] (webinar "Reputation und Open Science"); https://zenodo.org/records/15789374 [R] ("Akademische Reputationsspiele"); https://dl.gi.de/items/a5067ac0-d0d4-43b7-97eb-90b1839b7a21 [R] (Reputationssysteme im eCommerce) | medium | German research uses "Reputation"; for software contribution the useful German phrase is "Anerkennung von Forschungssoftware". |
| Agent framework / multi-agent | R06-R08, R29 | KI-Agent(en), Multi-Agenten-System, Agent-Orchestrator, mehrmandantenfähig, Agent Engineering | Agent, Agentic AI, Orchestrator, Tool-Call, Human-in-the-Loop, HITL, LangGraph, CrewAI | https://gitlab.opencode.de/f13/microservices/agentic-orchestrator [I] ("mehrmandantenfähiger Agent-Orchestrator ... Pre-Call-Chain aus OPA-Policy und Human-in-the-Loop"); https://gitlab.opencode.de/public-sector-dev-crew/lotse/bootsmann [I] ("Agent Engineering ... HITL-Verträge"); https://www.heise.de/tests/AutoGen-im-Test-Das-flexible-Multi-Agenten-Framework-fuer-bessere-KI-9792958.html [R] | high | Both "KI-Agent" and "Agent" are used. "Agentic" is the loanword. |
| Browser automation / extension security | R05, R19, R20, R21 | Browser-Erweiterung, Berechtigungen, Native Messaging (MDN de keeps English), Prompt Injection, KI-Browser | Browser-Automation, Prompt Injection, Extension, Manifest | https://developer.mozilla.org/de/docs/Mozilla/Add-ons/WebExtensions/Native_messaging [R]; https://www.bsi.bund.de/.../ki-agenten_node.html [I] ("Prompt Injection – Angriffe über Inhalte", "Aktionen vor der Ausführung prüfen"); https://www.heise.de/news/Weil-sie-denken-sie-waeren-in-einem-Spiel-KI-Browser-geben-Passwoerter-heraus-11351213.html [R] | high | "Browser-Automatisierung" appears in student/tutorial repos only (GitHub search, noisy). Use English "browser automation" except on BSI/heise for security phrasing. |
| MCP | R06, R07, R14 | MCP-Server, MCP-Autorisierung, MCP-Gateway, Positivliste (Allowlist), Werkzeugbeschreibung | MCP, Model Context Protocol (also "Protokoll"), Tool Poisoning, Rug Pull | heise MCP article [I]; https://gitlab.opencode.de/kern-ux/kern-labor-projekte/kern-mcp-server [R]; https://gitlab.opencode.de/f13/microservices/agentic-orchestrator [I] ("ruft Tools über MCP-Endpoints auf") | high | "MCP" never translated. Heise uses "Positivliste" for allowlist. |

Extra concepts (not among the 16, needed for requirements): secret broker (Geheimnisverwaltung, Zugangsdaten, Tresor; loanword Secrets Management, Vault) evidence: https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/Hilfsmittel/Benutzerdefinierte_BS/BS_Secrets_Management_mit_Hashicorp_Vault.pdf [R], https://m.heise.de/developer/artikel/Vault-fuer-Entwickler-Geheimnisse-in-Webanwendungen-schuetzen-4296863.html [R], https://gitlab.opencode.de/public-sector-dev-crew/lotse/tresor [I] (crypto-shredding, KMS adapter); signing/supply chain (Signierung, Lieferkette, Signatur, Nachweis) evidence: https://www.heise.de/news/Software-Supply-Chain-Security-Sigstore-ist-einsatzreif-fuer-die-Produktion-7325958.html [R], https://gitlab.opencode.de/ig-bvc/ag-sig/cosign-admissioncontroller-tests [R]; data sovereignty (Datensouveränität, digitale Souveränität, Souveränitätscheck) evidence: https://gitlab.opencode.de/zendis/kriterien-digitale-souveraenitaet [I, metadata only]; participation/voting (Beteiligungsplattform, Adhocracy, Liquid Democracy, delegierte Stimmabgabe) evidence: https://gitlab.opencode.de/smart-city-arnsberg/beteiligungsplattform-adhocracy [R], https://wiki.p2pfoundation.net/Liquid_Democracy [R].

## Table 2: search strings per requirement

Strings are untested unless marked in notes. Platform keys: OC = gitlab.opencode.de project search; HRSD = helmholtz.software; UG = university GitLabs; GH = GitHub; WEB = web search with heise/bsi/golem.

OC and the GitLab APIs match project name/description/path (README text was not matched in my probes), so use ONE keyword per query there. Multiword phrases below are for WEB/GH.

| Req | Search strings | Platforms likely to hit | Notes |
|---|---|---|---|
| R01 | `Berechtigungsmanagement Delegation Widerruf Token`; `Zugriffstoken befristet widerrufen`; `delegierte Berechtigung Zeitbegrenzung`; `capability token Delegation Widerruf`; `Macaroons Biscuit UCAN Berechtigung`; `Zugriffsrechte vergeben Agent` | WEB, GH (English parts), OC (single words: Berechtigung, Token) | BSI ORP.4 is the vocabulary anchor. Expect English tool names in German text. |
| R02 | `Sandboxing KI-Agenten Isolierung`; `Sandbox Container Isolation Prozess`; `bubblewrap Landlock Sandbox`; `Agent Sandbox Container mounts Projektverzeichnis`; `gVisor Firecracker Isolierung`; `Prozessisolation Windows AppContainer` | UG (MPCDF, GWDG), OC (Sandbox, Container), WEB heise | MPCDF "ai-cli-agents-container" and OC "agent-containers" are direct hits. |
| R03 | `Geheimnisverwaltung API-Schlüssel Proxy`; `Secrets Management Zugangsdaten Agent`; `Tresor Schlüsselverwaltung KMS`; `Vault Transit Verschlüsselung Anwendung`; `Credential Proxy LLM`; `Zugangsdaten nicht an Kindprozess` | OC (Secrets, Tresor), WEB heise/BSI | OC lotse/tresor and BSI APP.bd.6 are anchors. |
| R04 | `Überwachung Neustart Prozess Rollback`; `Supervisor Neustart Watchdog Dienst`; `Selbstheilung Wiederanlauf Wiederherstellung`; `Rollback bekannter guter Stand Hash`; `systemd Neustart Überwachung Desktop` | WEB, UG, OC (restore, Rollback) | Weak German use: "Supervisor", "Watchdog" stay English. OC has `lotse/restore-epoch-postgres` [R]. |
| R05 | `lokaler Webserver Absicherung Token Origin`; `localhost Angriff DNS-Rebinding`; `CSRF Schutz lokale API`; `Loopback Schnittstelle Authentifizierung`; `Unix-Socket Named Pipe Zugriffsrechte` | WEB heise | heise "Einfallstor Browser" and Java CSRF article are the nearest. Nothing found specific to extension-bridge. |
| R06 | `MCP Server Autorisierung Freigabe`; `Model Context Protocol Sicherheit Bestätigung Nutzer`; `MCP Gateway Positivliste Tools`; `Tool Poisoning Rug Pull`; `MCP Endpoints Human-in-the-Loop`; `MCP Server Open WebUI Berechtigung` | OC (MCP), WEB heise, GH | OC: f13/agentic-orchestrator, kern-mcp-server. |
| R07 | `Agent-Orchestrator mehrmandantenfähig`; `KI-Agenten Laufzeit austauschen Adapter`; `Multi-Agenten-System Framework`; `Agent-to-Agent Protokoll A2A`; `Agent Engineering Übergabevertrag Handoff`; `Aufrufer Zuordnung Delegation Agent` | OC (Agent, Orchestrator), UG | OC lotse/bootsmann has "Handoff-Schema" and "HITL-Verträge". |
| R08 | `LLM Provider Failover Modellwahl`; `providerneutral LLM Adapter`; `LiteLLM Gateway selbst gehostet`; `Modell-Registry Fallback Kandidatenwahl`; `OpenAI-kompatibel Proxy lokal` | OC (LLM, litellm), WEB | OC lotse/faehre ("providerneutrale LLM-Verträge", "Modell-Registry, geordnete Kandidatenwahl") [I]; oci-community litellm-non-root [R]. |
| R09 | `Skill Beschreibung Plugin Manifest`; `Agent Skills SKILL.md`; `Plugin-Format Schema Validierung`; `Werkzeugbeschreibung Schema JSON`; `Erweiterung Manifest Signatur` | GH, WEB | Weak German vocabulary. Use English "skill", "plugin manifest". |
| R10 | `Workflow-Engine Wiederaufnahme nach Absturz`; `Durable Execution Temporal Idempotenz`; `Idempotenz-Schlüssel Wiederholung Aktivität`; `Job-Queue SQLite persistent Wiederanlauf`; `Checkpoint Replay Workflow`; `Camunda Zeebe Workflow` | WEB, UG (TU Berlin, GWDG), OC (Workflow) | "Idempotenz" is native and common. OC has spark-workflow, bmds workflows (administrative). |
| R11 | `manipulationssicheres Audit-Log Hashkette`; `Audit-Trail revisionssicher Merkle`; `Transparenzlog Rekor Trillian`; `Beweissicherung Audit-Eintrag`; `hash-verkettete Logstruktur`; `Freigabenachweis Protokoll` | OC (Audit, Verklarung), WEB | OC lotse/verklarung and lotse/tresor, f13/audit-logger [R]. |
| R12 | `Provenienz Herkunftsnachweis Attestierung`; `in-toto SLSA Provenance Nachweis`; `selektive Offenlegung SD-JWT`; `Verifiable Credentials Datenminimierung`; `Provenance-Kennzeichnung KI-Text Signatur`; `C2PA Herkunft KI-Inhalte` | OC (Provenance, Attestation, Wallet), HRSD (provenance: Alpaca, DataLad) | OC lotse/flagge = content-bound provenance watermark. HRSD hits are English. |
| R13 | `atomares Schreiben Datei Absturz`; `SQLite WAL Wiederherstellung Korruption`; `Journaling Dateisystem Absturzkonsistenz`; `JSON Datei beschädigt Wiederherstellung`; `Git-basierte Ablage Versionierung` | WEB, GH | Low German coverage. Prefer English "atomic write", "crash consistency". |
| R14 | `Wissensdatenbank Quelle KI-Ableitung getrennt`; `Freigabe Prüfung Übernahme Wissensbasis`; `Versionshistorie unveränderlich Wissen`; `Obsidian Logseq Markdown Wissensspeicher lokal`; `Mandant Wissensdatenbank`; `Quellenerhalt Provenienz Wissensgraph` | OC (datastore, Wissens), UG, HRSD (DataLad) | OC f13/microservices/datastore: "mandantenfähiger Datenspeicher für Wissensdatenbanken" [R]. |
| R15 | `verschlüsseltes Dokumentendepot offline`; `Schlüsselverwaltung portabel Wiederherstellung`; `Passwort-Tresor KeePass lokal`; `age rage Verschlüsselung Datei`; `Crypto-Shredding Schlüssel`; `Datensouveränität lokale Verschlüsselung` | OC (Tresor, offline, vivodepot), WEB | OC vivodepot: encrypted single-file offline depot, EUPL-1.2 [I]. |
| R16 | `Local-First Synchronisation Ende-zu-Ende`; `CRDT Automerge Yjs Synchronisation`; `offline-fähig mehrere Geräte Abgleich`; `Syncthing Abgleich verschlüsselt`; `Datensouveränität Sync ohne Cloud` | GH, WEB | Almost no German source; English terms dominate. |
| R17 | `lokale Suche Volltext Vektor offline`; `semantische Suche lokal Embeddings`; `SQLite FTS5 Volltextsuche`; `RAG offline Wissensbasis`; `Retrieval ohne Cloud` | OC (RAG, LLM), GH | OC has many RAG/LLM projects (LLM total=29). |
| R18 | `signierte Erweiterung Manifest Prüfsumme`; `Cosign Signaturprüfung Container Admission`; `Software-Lieferkette Signierung Nachweis`; `Sperrliste Widerruf Erweiterungen`; `TUF The Update Framework`; `SBOM Herkunft Signatur` | OC (Signatur, Attestation, DevGuard), WEB heise | OC ig-bvc/ag-sig/cosign-admissioncontroller-tests and l3montree DevGuard are strong. |
| R19 | `KI-Browser Prompt Injection Freigabe`; `Browser-Agent Berechtigung pro Seite`; `Aktionen vor Ausführung bestätigen`; `Browser-Automatisierung Agent Sicherheit`; `Playwright MCP Freigabe`; `Prompt Injection Testkorpus Angriffe` | WEB (BSI, heise), OC (Prompt-Injection: wache), GH | OC lotse/wache has "Prompt-Injection-Erkennung" [I]; BSI evasion-attacks PDF [R]. |
| R20 | `Native Messaging Host Sicherheit`; `Browser-Erweiterung Native Messaging Pairing`; `KeePassXC Browser Verbindung`; `Erweiterung localhost HTTP Token`; `Origin Bindung Erweiterung` | WEB, MDN de | MDN de page "Native Messaging" [R] keeps the English name. |
| R21 | `Plugin Isolation Erweiterung Sandbox`; `WebAssembly Plugin Extism Wasmtime`; `iframe sandbox postMessage`; `Erweiterungen Berechtigungsmodell`; `Content-Script Berechtigungen` | WEB, GH | Use English for repositories. |
| R22 | `nicht übertragbare Nachweise Wallet`; `EUDI Wallet Widerruf Nachweis`; `Token-2022 nicht übertragbar`; `Soulbound Token`; `Credential Sperrung Neuausstellung`; `Mitgliedsnachweis digital Widerruf` | OC (bmi/eudi-wallet), WEB | German public-sector credential work is EUDI wallet, not Solana. |
| R23 | `Schlüsselbesitz Nachweis Signatur Anmeldung`; `Sign-In with Ethereum Solana`; `Verifiable Credentials DID Register`; `Merkle-Wurzel Verankerung Blockchain`; `Mitgliederverzeichnis dezentral Nachweis` | OC (Wallet, Credential), WEB | EUDI trust lists: OC bmi/eudi-wallet/test-trust-lists [R]. |
| R24 | `DAO Governance Abstimmung Multisig`; `dezentrale autonome Organisation Zeitsperre`; `Governance-Token Stimmgewichtung`; `Realms Squads Multisig`; `Snapshot Abstimmung Strategie`; `Beschlussfassung digital Delegation` | WEB, GH | German hits are legal/finance (Bundesbank). Use English on GH. |
| R25 | `Sybil-Angriff Identitätsnachweis Personhood`; `Mehrfachidentitäten Abstimmung`; `Bot Mensch Unterscheidung Mitgliedschaft`; `Proof of Humanity Worldcoin`; `Datenschutz Identitätsprüfung ohne KYC` | WEB | Thin. |
| R26 | `Beitragsbewertung Wirkung mehrdimensional`; `Anerkennung Beitrag Forschungssoftware`; `Reputationssystem Mitwirkende`; `CRediT Beitragsrollen`; `Beitragsregister Begründung Einspruch` | HRSD, Zenodo, WEB | German Zenodo hits: Reputation und Open Science webinar [R]. |
| R27 | `Kollusion Reputationssystem Sybil`; `Gutachterzuweisung Interessenkonflikt`; `Stimmenkauf Verhinderung MACI`; `Einspruchsverfahren Begrenzung`; `Peer Review Zuweisung Befangenheit` | WEB, Zenodo | Mostly English papers. |
| R28 | `Zuordnung Beiträge Vorleistung Abstufung`; `Zitation Anerkennung Software abhängig`; `Abhängigkeiten Förderung Open Source`; `Attribution Kette Verfall` | WEB | Native words weak. Use English "attribution", "dependency funding". |
| R29 | `Open WebUI LibreChat selbst gehostet`; `KI-Arbeitsplatz Verwaltung Open Source`; `Agent-Plattform souverän`; `digitale Souveränität KI Plattform`; `Mandantenfähigkeit Agent`; `openDesk KI` | OC (opendesk, f13, kern), WEB | OC f13 (f13-os.de) is an agent/chat platform for German administration [R]. |
| R30 | `Beteiligungsplattform Adhocracy Decidim`; `Liquid Democracy Delegation`; `Open Collective Transparenz Haushalt`; `Git-basierte Entscheidungsfindung Beschluss`; `Transparenzlog öffentlich prüfbar`; `Abstimmung Terminfinder Beteiligung` | OC (Beteiligung, Abstimmung), WEB | OC: smart-city-arnsberg/beteiligungsplattform-adhocracy [R], dataport terminfinder (polls) [R]. |

## Rejected terms (searched, no technical usage found)

| Term | Reason |
|---|---|
| Fähigkeits-Token / Fähigkeitenbasierte Sicherheit (for capability) | Only translation-style hits; real texts keep "Capability". |
| Abschwächung (for attenuation) | Not found in any technical source; Delegation + "Einschränkung" is used instead. |
| Dauerhafte Ausführung / beständige Ausführung (durable execution) | No hits; blogs write "Durable Execution". |
| Ereignisquellenverwaltung / Ereignisprotokollierung (event sourcing) | Not found; "Event Sourcing" stays English. |
| Soulbound-Token (German phrase) / seelengebundener Token | No German technical article found; only English term appears. German "nicht übertragbarer Token" appears only descriptively. |
| quadratische Finanzierung | GitHub search: 2 irrelevant repos (real estate, an economics hobby repo); no practitioner use. Use "Quadratic Funding". |
| Selektive Preisgabe | Not found; "selektive Offenlegung" is the term in use. |
| Objekt-Fähigkeiten | Not found. |
| Zugriffstoken Widerruf Delegation (GitHub, as a phrase) | 1 irrelevant repo (derHofib/DRK). |
| Workflow-Engine ausfallsicher; Browser-Automatisierung (as technical term in German repos) | 0 results for the first; the second appears only in student/tutorial repos on GitHub, no maintained tooling. |
| Nachvollziehbarkeit as an openCode project search | 0 project hits (word is in README/doc text, not names), but valid as concept term in BSI/Helmholtz text. Do not use it as an OC project search. |
| Berechtigungskonzept, Rechteverwaltung, Widerruf, Zugriffstoken, Herkunftsnachweis, Provenienz, Browser-Automatisierung, KI-Agent, Verifiable, Reputation (as OC project-search words) | 0 project hits on openCode (names/descriptions). Concept-valid in text but not useful as OC search keywords. |
| Umlaut variants (ue/ae/oe) | Present in OC project paths: `kriterien-digitale-souveraenitaet`, `digitaleIdentitaeten`, `faehre`; none found as spelling of ß (ss). Real, so keep as URL variants, see below. |

## Spelling and URL variants (verified)

- `Souveränität` is searchable in OC; project path uses `souveraenitaet`. Verified: https://gitlab.opencode.de/zendis/kriterien-digitale-souveraenitaet [I].
- `Fähre` repo is `faehre`; `Beteiligung`, `Berechtigung` have no umlauts.
- GitLab `search=` takes UTF-8 encoded umlauts and returned results for "Souveränität" (3) and "Datensouveränität" (1). A search with ASCII "Souveraenitaet" was not tested.
- ß/ss: no verified case found; search both anyway for "Maßnahmen/Massnahmen".
- Compound nouns found in real use: Berechtigungsmanagement, Berechtigungsprofil, Protokolleintrag, Audit-Einträge, Hash-verkettet(e Logstrukturen), Mandantenfähigkeit/mehrmandantenfähig, Positivliste, Beweissicherung, Datenminimierung, Datensouveränität, Souveränitätscheck, Zugriffsrechte, Pre-Call-Chain, Human-in-the-Loop.
- Abbreviations seen in German text: HITL, MCP, OPA, KMS, EUDI, ZKP, ARF, PII, NER, DSGVO.

## Platform notes for the German language agent

### openCode.de (https://gitlab.opencode.de)
- It is a GitLab instance. Anonymous project search works: `GET /api/v4/projects?search=TERM&per_page=20&order_by=last_activity_at`. Response is JSON; header `x-total` gives total hits. No token needed. `/api/v4/version` returns 401 (not needed).
- Search matches project name, path and description. README text was not matched in my probes (e.g. "Nachvollziehbarkeit" 0 hits although used in docs). Use ONE keyword per query; short nouns work best (Agent, Audit, Workflow, Tresor, Wallet, Attestation, Provenance, Souverän).
- Useful follow-ups for each hit: `GET /api/v4/projects/<url-encoded path>` (description, last_activity_at) and `/repository/files/README.md/raw?ref=<default_branch>` (works anonymously for public projects).
- Group listing: `/api/v4/groups/<encoded path>/projects?include_subgroups=true&simple=true`.
- Many entries are mirrors ("Mirrored from https://github.com/..."); read the description. Names like `oc000172416606` are anonymised user namespaces.
- Rate limit: no 429 in about 40 requests. Not measured beyond that.
- Strong candidates already found (all 2026-10-20, listing [R] unless noted): f13/microservices/agentic-orchestrator [I], f13/microservices/audit/audit-logger, f13/microservices/datastore, public-sector-dev-crew/lotse/* [I] (bootsmann, tresor, verklarung, schott, wache, fender, flagge, faehre), vivodepot/vivodepot [I], open-code/badgebackend/source-provenance-attestation-service, ig-bvc/ag-sig/cosign-admissioncontroller-tests, l3montree/devguard-*, wuppertal/infrastructure/agent-containers, kern-ux/kern-labor-projekte/kern-mcp-server, bmi/eudi-wallet/*, oci-community/container-gov.
- The lotse packages carry maritime German names (Tresor=vault, Verklarung=audit trail, Schott=tenant separation, Wache=guardrails, Fähre=LLM transport, Flagge=provenance mark, Fender=structured output, Rigg=contracts). Search these as names, not as concepts.

### Helmholtz RSD (https://helmholtz.software)
- PostgREST API, anonymous: `GET /api/v1/software?or=(brand_name.ilike.*TERM*,short_statement.ilike.*TERM*)&select=slug,brand_name,short_statement&limit=10`. The `/api/software` path returns the HTML app, not JSON.
- Content is English. All German words I tried (Provenienz, Nachvollziehbarkeit, Sandbox, Berechtigung, Herkunft, lokal, Zugriffsrechte) returned 0. English words work: workflow 6+, provenance 3 (Alpaca, DataLad, O2A SEQUENCES), agent 6+. Query English there.
- Sort/paging: standard PostgREST `limit`, `offset`, `order`. Response header `Content-Range` gives totals.

### University and research GitLabs
- Anonymous search works: codebase.helmholtz.cloud (HZDR redirects to it), gitlab.kit.edu, gitlab.gwdg.de, git.tu-berlin.de, gitlab.mpcdf.mpg.de, gitlab.cs.fau.de, gitlab.uni-hannover.de, gitlab.com. Same endpoint shape as openCode.
- Empty (HTTP 200, `[]`) for the test term: git.gfz-potsdam.de, gitlab.dkrz.de, git.uni-jena.de, gitlab.lrz.de, gitlab.informatik.uni-bonn.de, git.ufz.de. Try other terms before concluding they are empty.
- Blocked: git.rwth-aachen.de (bot-check page, not JSON). Unreachable: git.bsi.bund.de, git.scc.kit.edu (guessed hostnames).
- Relevant hits seen: gitlab.mpcdf.mpg.de mpcdf/ai-cli-agents-container ("Sandbox AI CLI agents ... mounts only the project directory"), gitlab.gwdg.de glissmann/sandbox-agent and hsp_26wise/public/hsp-agentenworkflow, gitlab.uni-hannover.de sandboxed-pi, gitlab.cs.fau.de BPF Sandbox (all [R]).
- Keyword match is on project name/description; many projects have empty descriptions, so recall is low.

### GitHub
- Rate limit hit after about 30 search queries in one minute (secondary limit, shared across agents). Wait for reset (see `gh api rate_limit`), batch queries with sleep of 2 seconds or more.
- German phrase searches mostly return student repos; English terms are better. Exceptions found: artundem/dao-legal-research (DAO in German company law), DevwithSoul/ki-agents-sicherheit (Guardrails/Gatekeeper, German) and hieblle/ki-woerterbuch (KI glossary) [R].

### Web sources (vocabulary leads)
- BSI KI-Agenten page [I] and evasion-attacks PDF [R] are the reference for public-sector wording on agents.
- heise: MCP/A2A security article [I, partial], Sigstore GA news [R], Vault for developers [R], AI-browser security news [R].
- WebSearch returns mostly summaries; open pages for citation. heise Plus content is partly paywalled.

## Cautions

- Evidence for DAO, soulbound, quadratic-funding vocabulary in German practitioner use is weak (legal/finance only). Do not spend many queries there.
- openCode agent hits describe plans (bootsmann is "geplant", "noch nicht implementiert"). Treat as design evidence, not working systems. Licences seen: EUPL-1.2 (lotse, vivodepot). EUPL needs legal review against the MIT target.
- I did not verify that any listed project works, only that it exists with the described README text.
