import type { User } from "./types";

const API_BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

function getAuthToken(): string | null {
  return localStorage.getItem("auth_token");
}

function buildHeaders(extra?: HeadersInit): HeadersInit {
  const token = getAuthToken();
  return {
    Accept: "application/json",
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...(extra || {}),
  };
}

async function handleResponse<T>(response: Response): Promise<T> {
  const contentType = response.headers.get("content-type") || "";
  const isJson = contentType.includes("application/json");
  const data = isJson ? await response.json().catch(() => null) : await response.text().catch(() => "");

  if (!response.ok) {
    const message =
      (data && typeof data === "object" && (data.detail || data.message)) ||
      (typeof data === "string" && data) ||
      response.statusText ||
      "Request failed";
    throw new Error(message);
  }

  return data as T;
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: buildHeaders(options.headers),
  });
  return handleResponse<T>(response);
}

export function loginWithGitHub() {
  window.location.href = `${API_BASE_URL}/api/v1/auth/login`;
}

export async function fetchCurrentUser(): Promise<User> {
  return request<User>("/api/v1/auth/me");
}

export async function fetchRepositories(includeCommitCount = false) {
  const params = new URLSearchParams();
  if (includeCommitCount) {
    params.set("include_commit_count", "true");
  }
  const query = params.toString();
  return request<{ total_repos: number; repos: any[] }>(
    `/api/v1/repos${query ? `?${query}` : ""}`,
  );
}

export async function toggleRepoMonitoring(repoName: string, isActive: boolean) {
  return request(`/api/v1/repos/${encodeURIComponent(repoName)}/toggle`, {
    method: "PATCH",
    body: JSON.stringify({ is_active: isActive }),
  });
}

export async function fetchCommits(
  repoFullName?: string,
  perPage = 20,
  includeStats = true,
) {
  const params = new URLSearchParams();
  if (repoFullName) {
    params.set("repo_full_name", repoFullName);
  }
  params.set("per_page", String(perPage));
  params.set("include_stats", String(includeStats));

  return request<{ commits: any[] }>(`/api/v1/commits?${params.toString()}`);
}

export type GenerateDocsInput = {
  repoFullName: string;
  commitSha: string;
  style?: "plainText" | "research" | "latex";
  complexity?: number;
  force?: boolean;
};

export async function generateDocs(input: GenerateDocsInput) {
  return request("/api/v1/docs/generate", {
    method: "POST",
    body: JSON.stringify({
      repo_full_name: input.repoFullName,
      commit_sha: input.commitSha,
      style: input.style,
      complexity: input.complexity,
      force: input.force ?? false,
    }),
  });
}
