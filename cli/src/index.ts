#!/usr/bin/env node
// @section CLI Entrypoint

import { Command } from "commander";
import { createCommand } from "./commands/create.js";
import { runCommand } from "./commands/run.js";
import { listCommand } from "./commands/list.js";
import { exportCommand } from "./commands/export.js";

const program = new Command();

program
  .name("sva")
  .description("sme-vital-agents CLI — create, run, and manage standalone agents")
  .version("0.1.0");

program.addCommand(createCommand);
program.addCommand(runCommand);
program.addCommand(listCommand);
program.addCommand(exportCommand);

program.parse();
