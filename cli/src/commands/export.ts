// @section Export Command
/**
 * Export an agent as a standalone package (Python + Docker).
 */

import { Command } from "commander";
import chalk from "chalk";
import { spawn } from "child_process";
import { join } from "path";
import { existsSync } from "fs";

export const exportCommand = new Command("export")
  .description("Export an agent as a standalone package")
  .argument("<name>", "Agent name to export")
  .option("-o, --output <dir>", "Output directory", "./exported-agents")
  .option("-d, --dir <dir>", "Agents directory", "./agents")
  .action(async (name: string, opts: { output: string; dir: string }) => {
    const configPath = join(opts.dir, name, "agent.yaml");

    if (!existsSync(configPath)) {
      console.error(chalk.red(`Agent '${name}' not found at ${configPath}`));
      process.exit(1);
    }

    console.log(chalk.cyan(`\n📦 Exporting agent '${name}'...\n`));

    const child = spawn(
      "python",
      ["-m", "core.agents.exporter", configPath, opts.output],
      { stdio: "inherit", cwd: process.cwd() }
    );

    child.on("close", (code) => {
      if (code === 0) {
        console.log(chalk.green(`\n✅ Agent exported to ${join(opts.output, name)}`));
        console.log(chalk.dim("   Run standalone: cd exported-agents/" + name + " && python main.py"));
        console.log(chalk.dim("   Or with Docker: docker build -t " + name + " . && docker run -it " + name + "\n"));
      } else {
        console.error(chalk.red(`\nExport failed with code ${code}`));
      }
    });
  });
