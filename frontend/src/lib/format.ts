import { formatDistanceToNowStrict, isValid, parseISO } from "date-fns";

const LANGUAGE_COLORS: Record<string, string> = {
  typescript: "#3178c6",
  javascript: "#f1e05a",
  python: "#3572A5",
  java: "#b07219",
  "c#": "#178600",
  "c++": "#f34b7d",
  go: "#00ADD8",
  rust: "#dea584",
  php: "#4F5D95",
  ruby: "#701516",
  swift: "#F05138",
  kotlin: "#A97BFF",
  html: "#e34c26",
  css: "#563d7c",
  shell: "#89e051",
  dockerfile: "#384d54",
  "jupyter notebook": "#DA5B0B",
  vue: "#41b883",
  svelte: "#ff3e00",
};

export function formatRelativeTime(value?: string | number | Date | null): string {
  if (!value) return "Unknown";

  let date: Date;
  if (value instanceof Date) {
    date = value;
  } else if (typeof value === "number") {
    date = new Date(value);
  } else {
    const parsed = parseISO(value);
    date = isValid(parsed) ? parsed : new Date(value);
  }

  if (!isValid(date)) {
    return String(value);
  }

  return formatDistanceToNowStrict(date, { addSuffix: true });
}

export function getLanguageColor(language?: string | null): string {
  if (!language) return "#94a3b8";
  const key = language.trim().toLowerCase();
  return LANGUAGE_COLORS[key] || "#94a3b8";
}
