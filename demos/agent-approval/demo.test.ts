import { expect, test } from "bun:test";

for (const [flag, expected] of [["", "WAITING: action proposed; executions=0"], ["--approve", "APPROVED: executions=1"], ["--deny", "DENIED: executions=0"]]) {
  test(`approval boundary ${flag || "pending"}`, () => {
    const result = Bun.spawnSync([process.execPath, "run", "demo.ts", ...(flag ? [flag] : [])], { cwd: import.meta.dir });
    expect(result.exitCode).toBe(0);
    expect(result.stdout.toString()).toContain(expected);
  });
}
