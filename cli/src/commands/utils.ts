// @section CLI Utilities

/**
 * Simple YAML serializer for agent configs.
 * Avoids a full yaml dependency in the CLI.
 */
export function dump(obj: Record<string, unknown>, indent = 0): string {
  const prefix = "  ".repeat(indent);
  const lines: string[] = [];

  for (const [key, value] of Object.entries(obj)) {
    if (Array.isArray(value)) {
      if (value.length === 0) {
        lines.push(`${prefix}${key}: []`);
      } else {
        lines.push(`${prefix}${key}:`);
        for (const item of value) {
          lines.push(`${prefix}  - ${item}`);
        }
      }
    } else if (typeof value === "object" && value !== null) {
      lines.push(`${prefix}${key}:`);
      lines.push(dump(value as Record<string, unknown>, indent + 1));
    } else if (typeof value === "string" && value.includes("\n")) {
      lines.push(`${prefix}${key}: |`);
      for (const line of value.split("\n")) {
        lines.push(`${prefix}  ${line}`);
      }
    } else {
      lines.push(`${prefix}${key}: ${value}`);
    }
  }

  return lines.join("\n");
}
