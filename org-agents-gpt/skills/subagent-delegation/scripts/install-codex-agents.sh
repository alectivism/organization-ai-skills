#!/usr/bin/env bash
# Install the Codex agent templates into a Codex agents directory and pin
# each one to the CURRENT model for its tier, read from Codex's own model
# catalog. Nothing here names a model for long: the templates carry a
# `# codex-tier: frontier|standard|fast` tag, and the slug is resolved at install time.
#
#   install-codex-agents.sh            install missing templates (never overwrites)
#   install-codex-agents.sh --sync     also rewrite `model =` in already-installed
#                                      tier-tagged files to the current catalog
#   install-codex-agents.sh [--sync] <target-dir>
#
# Tiers resolve by model family, newest generation first: frontier = newest
# Astra (GPT-6 Astra as of 2026-09-22), standard = newest Sol, the everyday
# workhorse (GPT-6 Sol), fast = newest Luna, the cheap leaf model (GPT-6 Luna).
# Catalog priority is not used: it is OpenAI's picker order, and on 2026-09-22
# it listed GPT-6 Sol above GPT-6 Astra.
set -euo pipefail

org_sync=0
if [ "${1:-}" = "--sync" ]; then org_sync=1; shift; fi

org_script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
org_template_dir="${org_script_dir}/../assets/codex-agents"
org_codex_home="${CODEX_HOME:-${HOME}/.codex}"
org_target_dir="${1:-${org_codex_home}/agents}"
org_catalog="${org_codex_home}/models_cache.json"

mkdir -p "${org_target_dir}"

have_catalog() { command -v jq >/dev/null 2>&1 && [ -r "${org_catalog}" ] && jq -e '.models | length > 0' "${org_catalog}" >/dev/null 2>&1; }

follow_upgrade() {
  local slug="$1" next hops=0
  while :; do
    next="$(jq -r --arg s "${slug}" '.models[] | select(.slug==$s) | .upgrade
      | if type=="string" then . elif type=="object" then (.model // .slug // .target // empty) else empty end' "${org_catalog}" 2>/dev/null || true)"
    [ -n "${next}" ] && [ "${next}" != "null" ] && [ "${next}" != "${slug}" ] || break
    slug="${next}"; hops=$((hops + 1)); [ ${hops} -lt 5 ] || break
  done
  echo "${slug}"
}

# newest_in_family <family>: newest listed gpt-<version>-<family> slug by
# version number, ties broken by catalog priority. Empty if none is listed.
newest_in_family() {
  jq -r --arg f "$1" '
    [ .models[] | select(.visibility=="list")
      | select(.slug | test("^gpt-[0-9.]+-" + $f + "($|-)"))
      | . + {ver: (.slug | capture("^gpt-(?<v>[0-9.]+)-").v | split(".") | map(tonumber))} ]
    | sort_by([(.ver | map(-.)), .priority]) | .[0].slug // empty' "${org_catalog}"
}

# resolve <tier> <template-slug>: prints the slug to pin. Falls back to the
# template's slug when there is no catalog (Codex writes one on its first run)
# or when the tier's family is not listed.
resolve() {
  local tier="$1" fallback="$2" family slug
  have_catalog || { echo "${fallback}"; return; }
  case "${tier}" in
    frontier) family=astra ;;
    standard) family=sol ;;
    fast)     family=luna ;;
    *) echo "${fallback}"; return ;;
  esac
  slug="$(newest_in_family "${family}")"
  [ -n "${slug}" ] || slug="${fallback}"
  follow_upgrade "${slug}"
}

tier_of()  { grep -m1 -E '^# codex-tier:' "$1" | sed -E 's/^# codex-tier:[[:space:]]*([a-z]+).*/\1/' || true; }
model_of() { grep -m1 -E '^model[[:space:]]*=' "$1" | sed -E 's/^model[[:space:]]*=[[:space:]]*"([^"]*)".*/\1/' || true; }
pin_model() {  # pin_model <file> <slug>
  local tmp; tmp="$(mktemp)"
  sed -E "s/^(model[[:space:]]*=[[:space:]]*)\"[^\"]*\"/\1\"$2\"/" "$1" > "${tmp}" && cat "${tmp}" > "$1"; rm -f "${tmp}"
}

org_installed=0
org_skipped=0
org_synced=0

for org_source in "${org_template_dir}"/*.toml; do
  org_name="$(basename "${org_source}")"
  org_target="${org_target_dir}/${org_name}"
  org_tier="$(tier_of "${org_source}")"
  org_want="$(resolve "${org_tier}" "$(model_of "${org_source}")")"

  if [ -e "${org_target}" ]; then
    if [ ${org_sync} -eq 1 ] && [ -n "$(tier_of "${org_target}")" ] && [ "$(model_of "${org_target}")" != "${org_want}" ]; then
      pin_model "${org_target}" "${org_want}"
      echo "SYNCED ${org_target} -> ${org_want}"
      org_synced=$((org_synced + 1))
    else
      echo "SKIPPED ${org_target} (already exists)"
      org_skipped=$((org_skipped + 1))
    fi
    continue
  fi

  org_staging="$(mktemp "${org_target_dir}/.${org_name}.XXXXXX")"
  cp "${org_source}" "${org_staging}"
  pin_model "${org_staging}" "${org_want}"
  if ! ln "${org_staging}" "${org_target}" 2>/dev/null; then
    rm -f "${org_staging}"
    echo "SKIPPED ${org_target} (already exists)"
    org_skipped=$((org_skipped + 1))
    continue
  fi
  rm -f "${org_staging}"
  echo "INSTALLED ${org_target} (${org_tier:-untagged} -> ${org_want})"
  org_installed=$((org_installed + 1))
done

have_catalog || echo "NOTE: no model catalog at ${org_catalog}; templates keep their shipped slugs. Run Codex once, then rerun with --sync."
echo "DONE installed=${org_installed} skipped=${org_skipped} synced=${org_synced}"
echo "Restart Codex to load newly installed agents."
