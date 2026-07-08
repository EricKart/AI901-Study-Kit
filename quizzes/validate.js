// Validate all question banks: run with `node validate.js` from the quizzes folder.
const fs = require("fs");
const path = require("path");

global.window = {};
const files = fs.readdirSync(__dirname).filter(f => /^(q\d[ab]|final\d)\.js$/.test(f)).sort();
for (const f of files) eval(fs.readFileSync(path.join(__dirname, f), "utf8"));

let fail = 0;
const banks = global.window.BANKS;
for (const [id, bank] of Object.entries(banks)) {
  const qs = bank.questions;
  const expected = id.startsWith("final") ? 45 : 30;
  const diff = { 1: 0, 2: 0, 3: 0 };
  const problems = [];
  if (qs.length !== expected) problems.push(`count=${qs.length}, expected ${expected}`);
  qs.forEach((q, i) => {
    if (!q.q || !q.x) problems.push(`Q${i + 1}: missing text/explanation`);
    if (!Array.isArray(q.o) || q.o.length !== 4) problems.push(`Q${i + 1}: ${q.o ? q.o.length : 0} options`);
    if (!(Number.isInteger(q.a) && q.a >= 0 && q.a < q.o.length)) problems.push(`Q${i + 1}: bad answer index ${q.a}`);
    if (![1, 2, 3].includes(q.d)) problems.push(`Q${i + 1}: bad difficulty ${q.d}`);
    else diff[q.d]++;
    if (new Set(q.o).size !== q.o.length) problems.push(`Q${i + 1}: duplicate options`);
  });
  const tag = problems.length ? "FAIL" : "ok  ";
  if (problems.length) fail++;
  console.log(`${tag} ${id.padEnd(7)} ${String(qs.length).padStart(2)} Q  easy=${diff[1]} mod=${diff[2]} hard=${diff[3]}  ${bank.minutes}min` +
    (problems.length ? "\n     " + problems.join("\n     ") : ""));
}
console.log(fail ? `\n${fail} bank(s) failed` : "\nall banks valid");
process.exit(fail ? 1 : 0);
