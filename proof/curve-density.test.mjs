import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { mkdtemp, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { promisify } from "node:util";
import test from "node:test";

const execute = promisify(execFile);
for (const [name, path, x, y] of [
  ["cubic between fixed samples", "M20 400C20 20 480 20 480 400", 25.166015625, 333.203125],
  ["quadratic between fixed samples", "M20 400Q250 20 480 400", 58.33333333333333, 341.94444444444446],
]) test(`native SVG ${name} roots an attached line`, async () => {
  const directory = await mkdtemp(join(tmpdir(), "anatomy-curve-density-"));
  try {
    const file = join(directory, "figure.html");
    await writeFile(file, `<!doctype html><div class="iso-plate"><svg width="520" height="440" viewBox="0 0 520 440"><path id="curve" fill="none" stroke="black" d="${path}"/><path class="iso-line" data-free="start" fill="none" stroke="black" d="M${x} 10L${x} ${y}"/></svg></div>`);
    const actions = JSON.stringify([["eval", `document.querySelector('#curve').isPointInStroke(new DOMPoint(${x},${y}))`], ["lines"]]);
    let result;
    try { result = { code: 0, ...await execute(process.execPath, ["scripts/drive.mjs", file, actions], { timeout: 30000 }) }; }
    catch (error) { result = { code: error.code, stdout: error.stdout, stderr: error.stderr }; }
    assert.match(result.stdout, /eval: true/);
    assert.match(result.stdout, /line ends: (?:0|1) of 1/);
    assert.equal(result.code, 0, `native audit exit expected 0 received ${result.code}\n${result.stdout}`);
    assert.match(result.stdout, /line ends: 0 of 1/);
  } finally { await rm(directory, { recursive: true, force: true }); }
});
