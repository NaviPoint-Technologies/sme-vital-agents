// @section Run Command
/**
 * Run an agent by name — spawns the Python core with the agent config.
 */

import { Command } from "commander";
import chalk from "chalk";
import { spawn } from "child_process";
import { join } from "path";
import { existsSync } from "fs";

export const runCommand = new Command("run")
  .description("Run an agent by name")
  .argument("<name>", "Agent name to run")
  .option("-d, --dir <dir>", "Agents directory", "./agents")
  .action(async (name: string, opts: { dir: string }) => {
    const agentDir = join(opts.dir, name);
    const configPath = join(agentDir, "agent.yaml");

    if (!existsSync(configPath)) {
      console.error(chalk.red(`Agent '${name}' not found at ${configPath}`));
      process.exit(1);
    }

    console.log(chalk.cyan(`\n🚀 Starting agent '${name}'...\n`));

    const child = spawn("python", ["-m", "core.agents.runner", configPath], {
      stdio: "inherit",
      cwd: join(process.cwd()),
    });

    child.on("close", (code) => {
      if (code !== 0) {
        console.error(chalk.red(`\nAgent exited with code ${code}`));
      }
    });
  });
