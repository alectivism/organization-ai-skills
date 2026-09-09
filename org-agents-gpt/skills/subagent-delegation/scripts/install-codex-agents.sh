#!/usr/bin/env bash
set -euo pipefail

org_script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
org_template_dir="${org_script_dir}/../assets/codex-agents"
org_codex_home="${CODEX_HOME:-${HOME}/.codex}"
org_target_dir="${1:-${org_codex_home}/agents}"

mkdir -p "${org_target_dir}"

org_installed=0
org_skipped=0

for org_source in "${org_template_dir}"/*.toml; do
  org_name="$(basename "${org_source}")"
  org_target="${org_target_dir}/${org_name}"
  org_staging="$(mktemp "${org_target_dir}/.${org_name}.XXXXXX")"

  if ! cp "${org_source}" "${org_staging}"; then
    rm -f "${org_staging}"
    echo "FAILED ${org_target} (could not stage template)" >&2
    exit 1
  fi

  if ! ln "${org_staging}" "${org_target}" 2>/dev/null; then
    rm -f "${org_staging}"
    echo "SKIPPED ${org_target} (already exists)"
    org_skipped=$((org_skipped + 1))
    continue
  fi

  rm -f "${org_staging}"
  echo "INSTALLED ${org_target}"
  org_installed=$((org_installed + 1))
done

echo "DONE installed=${org_installed} skipped=${org_skipped}"
echo "Restart Codex to load newly installed agents."
