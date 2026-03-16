"""
Compliance Agent
----------------
Cross-verifies outputs from all orchestrator agents and generates
a compliance report using LLM. Updates state with pass/fail status
and summary.
"""

from typing import Dict
from app.orchestrator.state import OrchestratorState
from app.llm.llm_client import llm
from app.core.logging_config import setup_logger
from app.core.exceptions import ComplianceAgentError

logger = setup_logger(__name__)


def compliance_agent(state: OrchestratorState) -> OrchestratorState:
    """
    Cross-checks outputs from all agents in the orchestrator state.

    Steps:
    1. Collect outputs from all relevant agents.
    2. Build a structured prompt summarizing all outputs.
    3. Send prompt to LLM to verify consistency.
    4. Update state with compliance_passed flag and compliance_report.

    Args:
        state (OrchestratorState): Current orchestrator state containing outputs from all agents.

    Returns:
        OrchestratorState: Updated state with:
            - "compliance_passed" (bool)
            - "compliance_report" (str)
    """
    try:
        logger.info("Compliance Agent started")

        # -------------------------------
        # 1️⃣ Collect agent outputs
        # -------------------------------
        agent_outputs: Dict[str, Dict] = {}
        agent_keys = [
            "nutrition_plan",
            "exercise_plan",
            "daily_journal",
            # Add other agent keys here as needed
        ]

        for key in agent_keys:
            output = state.get(key)
            if output:
                agent_outputs[key] = output

        if not agent_outputs:
            logger.warning("No agent outputs found in state")
            state["compliance_passed"] = False
            state["compliance_report"] = "No agent outputs available for compliance check."
            return state

        logger.debug("Collected agent outputs for compliance check: %s", list(agent_outputs.keys()))

        # -------------------------------
        # 2️⃣ Build LLM prompt
        # -------------------------------
        prompt_lines = ["You are an AI compliance officer. Verify if the outputs from all agents are consistent and logical.\n"]
        for agent_name, output in agent_outputs.items():
            prompt_lines.append(f"Agent: {agent_name}\nOutput: {output}\n")

        prompt_lines.append(
            "Instructions:\n"
            "- Check for logical consistency across all agent outputs.\n"
            "- Identify any conflicts or mismatches.\n"
            "- Provide a compliance summary.\n"
            "- Answer with 'COMPLIANCE PASSED' if all outputs are consistent, otherwise 'COMPLIANCE FAILED'.\n"
            "- Include explanation of any mismatches."
        )

        compliance_prompt = "\n".join(prompt_lines)

        # -------------------------------
        # 3️⃣ Invoke LLM
        # -------------------------------
        logger.info("Sending compliance prompt to LLM for verification")
        llm_response = llm.invoke(compliance_prompt)

        # -------------------------------
        # 4️⃣ Determine compliance_passed
        # -------------------------------
        compliance_passed = "COMPLIANCE PASSED" in llm_response.upper()

        # -------------------------------
        # 5️⃣ Update orchestrator state
        # -------------------------------
        state["compliance_passed"] = compliance_passed
        state["compliance_report"] = llm_response.strip()

        logger.info(
            "Compliance Agent completed | passed=%s", compliance_passed
        )

        return state

    except Exception as e:
        logger.exception("Compliance Agent failed")
        state["compliance_passed"] = False
        state["compliance_report"] = f"Compliance check failed due to error: {str(e)}"
        raise ComplianceAgentError(str(e)) from e
