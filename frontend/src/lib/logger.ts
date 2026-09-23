type Level = "info" | "warn" | "error";

function formatContext(context: object): string | object {
  try {
    return JSON.stringify(context);
  } catch (error) {
    return context;
  }
}

function log(level: Level, message: string, context?: object): void {
  if (process.env.NODE_ENV === "production") return;

  const prefix = `[${level.toUpperCase()}]`;
  if (context) {
    console[level](prefix, message, formatContext(context));
  } else {
    console[level](prefix, message);
  }
}

export const logger = {
  info: (message: string, context?: object) => log("info", message, context),
  warn: (message: string, context?: object) => log("warn", message, context),
  error: (message: string, context?: object) => log("error", message, context),
};
