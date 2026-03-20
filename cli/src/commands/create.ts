// @section Create Command
/**
 * Interactive agent creation wizard.
 * Prompts for name, backend, model, tools, then generates agent.yaml.
 */

import { Command } from "commander";
import inquirer from "inquirer";
import chalk from "chalk";
import { writeFileSync, mkdirSync } from "fs";
import { join } from "path";
import { dump } from "./utils.js";

export const createCommand = new Command("create")
  .description("Create a new agent definition interactively")
  .argument("[name]", "Agent name")
  .option("-b, --backend <backend>", "Backend to use", "ollama")
  .option("-m, --model <model>", "Model name", "llama3.1")
  .action(async (name?: string, opts?: Record<string, string>) => {
    console.log(chalk.cyan("\n🤖 Agent Creation Wizard\n"));

    const answers = await inquirer.prompt([
      {
        type: "input",
        name: "name",
        message: "Agent name:",
        default: name || "my-agent",
      },
      {
        type: "input",
        name: "description",
        message: "Description:",
        default: "A standalone AI agent",
      },
      {
        type: "list",
        name: "backend_name",
        message: "Backend:",
        choices: ["ollama", "claude-code"],
        default: opts?.backend || "ollama",
      },
      {
        type: "input",
        name: "model",
        message: "Model:",
        default: opts?.model || "llama3.1",
      },
      {
        type: "editor",
        name: "system_prompt",
        message: "System prompt (opens editor):",
        default: "You are a helpful AI assistant.",
      },
      {
        type: "checkbox",
        name: "tools",
        message: "Built-in tools to include:",
        choices: ["read_file", "write_file", "shell"],
      },
    ]);

    const agentDir = join(process.cwd(), "agents", answers.name);
    mkdirSync(agentDir, { recursive: true });

    const configPath = join(agentDir, "agent.yaml");
    writeFileSync(configPath, dump(answers));

    console.log(chalk.green(`\n✅ Agent created at ${agentDir}`));
    console.log(chalk.dim(`   Config: ${configPath}`));
    console.log(chalk.dim(`   Run with: sva run ${answers.name}\n`));
  });
