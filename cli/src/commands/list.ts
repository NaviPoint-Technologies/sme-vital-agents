// @section List Command
/**
 * List all defined agents in the agents directory.
 */

import { Command } from "commander";
import chalk from "chalk";
import { readdirSync, readFileSync, existsSync } from "fs";
import { join } from "path";

export const listCommand = new Command("list")
  .description("List all defined agents")
  .option("-d, --dir <dir>", "Agents directory", "./agents")
  .action((opts: { dir: string }) => {
    if (!existsSync(opts.dir)) {
      console.log(chalk.yellow("No agents directory found. Run 'sva create' first."));
      return;
    }

    const entries = readdirSync(opts.dir, { withFileTypes: true });
    const agents = entries.filter((e) => e.isDirectory());

    if (agents.length === 0) {
      console.log(chalk.yellow("No agents found."));
      return;
    }

    console.log(chalk.cyan(`\n📋 Agents (${agents.length}):\n`));

    for (const agent of agents) {
      const configPath = join(opts.dir, agent.name, "agent.yaml");
      let desc = "";
      if (existsSync(configPath)) {
        const content = readFileSync(configPath, "utf-8");
        const match = content.match(/description:\s*(.+)/);
        desc = match ? match[1] : "";
      }
      console.log(`  ${chalk.green(agent.name)}  ${chalk.dim(desc)}`);
    }
    console.log();
  });
