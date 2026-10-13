#!/usr/bin/env bash
# restore-agent.sh — Recreate the us-market OpenClaw agent configuration
#
# IMPORTANT: This script does NOT start or enable any scheduled tasks.
# You must explicitly enable cron jobs via the OpenClaw gateway after reviewing
# restore/restore-cron-jobs.sh. All tasks start disabled by default.
#
# PREREQUISITES:
#   - OpenClaw installed and running (openclaw status)
#   - Claude CLI authenticated: claude auth login
#   - OpenAI OAuth configured (optional fallback): openclaw configure
#   - Webull API credentials configured in .webull.env (copy from .env.example)
#   - WORKSPACE_PATH set to the absolute path of this directory

set -euo pipefail

WORKSPACE_PATH="${WORKSPACE_PATH:-$(cd "$(dirname "$0")/.." && pwd)}"
AGENT_ID="us-market"

echo "=== us-stock-monitor: Agent Restore ==="
echo "Workspace: $WORKSPACE_PATH"
echo ""

# Verify OpenClaw is available
if ! command -v openclaw &>/dev/null; then
  echo "ERROR: openclaw not found. Install OpenClaw first: https://github.com/openclaw/openclaw"
  exit 1
fi

# Verify Claude auth
echo "[1/4] Checking Claude CLI authentication..."
if ! claude -p "." --output-format text &>/dev/null 2>&1; then
  echo "  WARNING: Claude CLI auth check failed or not available."
  echo "  Run: claude auth login"
  echo "  (Required for the us-market agent to make AI calls)"
else
  echo "  Claude CLI: OK"
fi

# Check workspace structure
echo "[2/4] Verifying workspace structure..."
REQUIRED_DIRS=("scripts" "research/cron_prompts" "reports" "research/logs")
for d in "${REQUIRED_DIRS[@]}"; do
  if [ ! -d "$WORKSPACE_PATH/$d" ]; then
    mkdir -p "$WORKSPACE_PATH/$d"
    echo "  Created: $d"
  fi
done

# Check .webull.env
echo "[3/4] Checking Webull credentials..."
if [ ! -f "$WORKSPACE_PATH/.webull.env" ]; then
  echo "  WARNING: .webull.env not found."
  echo "  Copy .env.example to .webull.env and fill in your Webull API credentials."
  echo "  The agent will fall back to PORTFOLIO_STATE.md if Webull API is unavailable."
else
  echo "  .webull.env found."
fi

# Install Python dependencies
echo "[4/4] Installing Python dependencies..."
if command -v pip3 &>/dev/null; then
  pip3 install -r "$WORKSPACE_PATH/requirements-webull.txt" --quiet
  echo "  Python dependencies installed."
else
  echo "  WARNING: pip3 not found. Install manually: pip install webull-openapi-python-sdk"
fi

echo ""
echo "=== Agent configuration ==="
echo "To register the us-market agent in OpenClaw, add this to your openclaw.json agents.list:"
echo ""
cat <<EOF
{
  "id": "us-market",
  "name": "us-market",
  "workspace": "$WORKSPACE_PATH",
  "model": {
    "primary": "anthropic/claude-opus-4-8",
    "fallbacks": ["openai/gpt-5.5"]
  },
  "thinkingDefault": "high"
}
EOF
echo ""
echo "Or use: openclaw gateway config.patch to add the agent programmatically."
echo ""
echo "NEXT STEP: Run restore/restore-cron-jobs.sh to review and optionally enable scheduled tasks."
echo "All tasks are disabled by default and will NOT run until you explicitly enable them."
