# CONTRACT_ID Derivation + Identity Discipline

<!-- Generated from references/full-pack.txt (pack v2.6) by scripts/split.py. Do not edit; edit the pack and re-split. -->

```
0.1a CONTRACT_ID DERIVATION  (owned by the Target Profiler, not the operator)
----------------------------------------------------------------------

The operator should not have to name the system before looking at it. A
hand-picked slug is also unstable: the same system named twice by hand produces
two different slugs, and the second run silently forks the contract.

So the agent derives it. But the slug must be fixed BEFORE the first artifact is
written, and at that moment the agent knows almost nothing. Resolve this with a
cheap IDENTITY PROBE, not with full discovery.

STEP 1 - IDENTITY PROBE (max 3 operations, no data profiling)

Take the first name that the target itself asserts. Precedence, highest first:

  DATA_API     OpenAPI/GraphQL info.title  ->  /  root or health payload name
               ->  the vendor+product in the docs  ->  the API hostname
  DATABASE     the database name  ->  the primary schema name  ->  the host role
  MCP_SERVER   serverInfo.name from the initialize handshake  ->  the package
               name in the server command  ->  the binary name
  CODEBASE     the repo name  ->  package.json / pyproject / go.mod module name
               ->  the directory name
  DATA_FILE    the dataset identifier in the URL path  ->  a title in the
               structural metadata beside the file  ->  vendor + dataset code
               NOTE: rank a Content-Disposition filename LAST, or not at all.
               It frequently encodes the REQUEST rather than the dataset - a
               filtered download names itself "..._filtered", so two requests
               for one dataset would fork the slug.

Prefer what the SYSTEM calls itself over what the operator calls it. The
system's own name is stable across runs and across operators; a nickname is not.

STEP 2 - NORMALIZE (deterministic; same input must always give same output)

  lowercase
  non-alphanumeric -> _
  collapse repeated _ and strip leading/trailing _
  drop generic noise tokens anywhere in the name:
      api, service, svc, server, mcp, db, database, data, platform, system,
      the, official, public, rest, graphql, v1, v2, v3, prod, production
  drop a trailing TLD when the name was taken from a domain or a page title:
      the final dot-separated label of the domain, whatever it is — gTLD or
      ccTLD. Do not work from an enumerated list; .no, .se and .br are TLDs
      exactly as much as .com is, and a list will always be missing one.
      (a system that names itself after its domain asserts the brand, not the
       registrar; keeping the TLD forks the slug the moment another run reads
       the brand from a different surface)
  drop version numbers and dates entirely
  if a vendor/org prefix is present and the product name alone is ambiguous,
      keep both:  usda_quickstats, not quickstats
  target 2-3 tokens, hard cap 32 characters
  if the result is empty or a single generic token, fall back to
      <vendor>_<host-first-label> from TARGET_LOCATION

Examples:
  "USDA/NASS QuickStats API"           -> usda_nass_quickstats
     (three tokens, not two: "nass" is not a noise token, so it survives.
      This example was hand-written as usda_quickstats until the pack was
      actually run against the system, which produced the longer form. Worked
      examples in a spec drift from the spec unless somebody executes them.)
  serverInfo.name "github-mcp-server"  -> github
  postgres db "orders_prod" on rds     -> orders
  repo "acme/billing-service"          -> acme_billing

STEP 3 - COLLISION CHECK (mandatory)

Read ~/contracts/INDEX.md. Then:

  no match                      -> adopt the slug
  match, SAME system            -> this is a refresh. Reuse the existing slug
                                   verbatim. Never mint a second one.
                                   Read .contract_id from the existing folder;
                                   it wins over anything you just derived.
  match, DIFFERENT system       -> both need a discriminator. Append the ONE
                                   attribute that actually distinguishes them,
                                   in this order of preference:
                                     vendor  ->  tenant  ->  environment  ->  region
                                   Rewrite BOTH slugs if the incumbent is now
                                   ambiguous, and record the rename in its
                                   CHANGELOG.md with an alias line.
                                   orders -> orders_prod / orders_staging

Add a discriminator only when a collision exists. A slug carrying an
environment token when there is only one environment is noise that will outlive
the reason for it.

STEP 4 - ESCALATE ONLY IF GENUINELY AMBIGUOUS

Ask the operator only when:
  - two candidate names are equally well-attested and mean different things, or
  - the collision is with a contract you cannot inspect, or
  - the system asserts no name at all and TARGET_LOCATION is opaque.

Present at most 3 candidates with one line each on where the name came from.
Do not ask when a defensible slug exists. The point of this section is that the
operator does not have to decide.

STEP 5 - FREEZE

Write the slug to <CONTRACT_DIR>/.contract_id and to TARGET.md, then treat it as
immutable. A slug is an identity, not a label.

To rename later: create the new contract, add an alias line to the old
CHANGELOG.md pointing at it, and keep the old folder until every downstream
consumer has moved. Never rename in place. Downstream agents and stored
provenance records hold the old id, and in-place renaming turns those into
unattributed fragments, which is exactly the failure 0.1b exists to prevent.

A refresh run (section 12) NEVER re-derives the slug. It reads .contract_id.

----------------------------------------------------------------------
0.1b IDENTITY DISCIPLINE  (applies to every agent, every artifact)
----------------------------------------------------------------------

An operator will eventually hold several contracts at once. The failure this
prevents is not a filesystem collision. It is an agent applying system A's
authority rule, unit convention, or "latest" semantics to system B, and
returning a plausible number with no error. That is SILENT_WRONG by
construction, and it is the exact failure this whole pack exists to stop.

A folder name alone does not prevent it, because agents quote CONTENT, not
paths. A METRICS.md fragment pasted into a context window with no system marker
is indistinguishable from any other system's METRICS.md.

CONTRACT_ID must therefore appear in four places:

1. THE FOLDER
   data_contract_<CONTRACT_ID>/
   Self-identifying no matter how it is referenced or copied.

2. EVERY GENERATED FILE, first line, before any other content:

     <!-- CONTRACT: <CONTRACT_ID> | FILE: METRICS.md | VERIFIED: <date> -->

   Non-negotiable. This is the line that survives being quoted out of context,
   and it is the cheapest safeguard in the entire pack. Any agent that reads a
   fragment without this header must treat it as unattributed and refuse to act
   on it.

3. THE CODE NAMESPACE
   The package is data_contract_<CONTRACT_ID>, so two contracts can be imported
   into the same process without shadowing each other:

     from data_contract_usda_quickstats.code import client as usda
     from data_contract_conab_pgdb.code   import client as conab

   A bare `from data_contract.code import client` is forbidden. It resolves to
   whichever contract happens to be first on the path, silently.

4. THE CENTRAL REGISTRY
   ~/contracts/INDEX.md, one row per contract:

     | CONTRACT_ID | TARGET_TYPE | answers questions about | path | last_verified_at | status |

   This is how a downstream agent chooses WHICH contract to load. Without it,
   an agent holding several contracts guesses, and guessing is the failure mode.

Every runtime object that crosses a contract boundary carries its origin.
Provenance records, validator exceptions, and returned values all include
contract_id. When two contracts describe the same real-world fact, that field
is the only thing that makes the conflict visible instead of silent.

----------------------------------------------------------------------
```
