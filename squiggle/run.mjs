// run.mjs — run every generated worldview model and print its ranking + EV.
//
// The models in worldviews/ are STANDALONE: the assumption chain is composed in
// Python (assumptions/worldviews.py) before the Squiggle is rendered, so there
// are no imports to resolve — each file runs on its own, here, in the online
// playground, or published to Squiggle Hub unchanged.
//
//   cd squiggle && npm install && node run.mjs
//   node run.mjs worldviews/w1_2_5.squiggle      # just one

import { SqProject, SqModule } from "@quri/squiggle-lang";
import { readFileSync, readdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));

async function rank(file) {
  const code = readFileSync(file, "utf8");
  const project = new SqProject({});
  project.setHead("root", { module: new SqModule({ name: "main", code }) });
  const output = await project.waitForOutput("root");
  const bindings = output.getBindings();
  if (!bindings.ok) throw new Error(bindings.value.toString());
  const arr = bindings.value.get("ranking").value.getValues();
  return {
    ev: bindings.value.get("worldviewEv").value,
    ranking: arr.map((v) => ({
      name: v.value.get("name").value,
      wdalyPerUsd: v.value.get("wdalyPerUsd").value,
    })),
  };
}

const args = process.argv.slice(2);
const files = args.length
  ? args
  : readdirSync(join(HERE, "worldviews")).sort()
      .filter((f) => f.endsWith(".squiggle"))
      .map((f) => join(HERE, "worldviews", f));

for (const file of files) {
  const { ev, ranking } = await rank(file);
  const name = file.split("/").pop();
  console.log(`\n${name}   worldviewEv = ${ev}`);
  ranking.forEach((r, i) =>
    console.log(`  ${i === 0 ? "→" : " "} ${String(r.name).padEnd(34)} ${r.wdalyPerUsd}`)
  );
}
