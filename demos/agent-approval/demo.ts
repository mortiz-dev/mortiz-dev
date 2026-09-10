import {
  Agent,
  type LanguageModel,
  tool
} from "@zhivex-ai/agents";
import { strict as assert } from "node:assert";
import { z } from "zod";

const decision = process.argv[2];
if (decision && !["--approve", "--deny"].includes(decision)) {
  throw new Error("Use no flag, --approve, or --deny.");
}

let modelCalls = 0;
let deployments = 0;

const model: LanguageModel = {
  provider: "example",
  modelId: "approval-deterministic",
  capabilities: {
    streaming: false,
    tools: true,
    structuredOutput: false,
    jsonMode: false,
    toolChoice: true,
    parallelToolCalls: true,
    vision: false,
    files: false,
    audioInput: false,
    audioOutput: false,
    embeddings: false,
    reasoning: false,
    webSearch: false
  },
  async generate() {
    modelCalls += 1;

    if (modelCalls === 1) {
      return {
        finishReason: "tool-calls",
        messages: [{
          role: "assistant",
          parts: [{
            type: "tool-call",
            toolCall: {
              id: "deploy_demo",
              name: "deploy",
              input: { target: "staging" }
            }
          }]
        }]
      };
    }

    return {
      text: "The requested action has been processed.",
      finishReason: "stop",
      messages: [{
        role: "assistant",
        parts: [{
          type: "text",
          text: "The requested action has been processed."
        }]
      }]
    };
  }
};

const agent = new Agent({
  id: "approval-hitl-example",
  model,
  instructions: "Use the deployment tool when asked.",
  tools: {
    deploy: tool({
      name: "deploy",
      description: "Deploy an application to an environment.",
      schema: z.object({ target: z.string() }),
      requiresApproval: true,
      approvalMode: "interrupt",
      approvalVersion: "2026-07-29",
      execute({ target }) {
        deployments += 1;
        return { target, deployed: true };
      }
    })
  },
  maxSteps: 2
});

console.log("SCRIPTED MODEL · SIMULATED ACTION · NO NETWORK");
const waiting = await agent.run({
  prompt: "Deploy the application to staging."
});
assert.equal(deployments, 0, "The action must not execute before approval");
assert.equal(waiting.state.pendingApprovals.length, 1);
console.log("WAITING: action proposed; executions=0");

if (!decision) {
  console.log("Choose: bun run demo --approve OR bun run demo --deny");
} else {
  const approve = decision === "--approve";
  const resumed = await agent.resume({
    state: waiting.state,
    approvals: waiting.state.pendingApprovals.map((request) => ({
      provider: request.provider,
      approvalRequestId: request.id,
      approve,
      reason: approve ? "Approved by demo operator" : "Denied by demo operator"
    }))
  });
  assert.equal(deployments, approve ? 1 : 0);
  console.log(`${approve ? "APPROVED" : "DENIED"}: executions=${deployments}`);
  console.log(`Runtime status: ${resumed.status}`);
}
