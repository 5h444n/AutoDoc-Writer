export interface User {
  username: string;
  name?: string | null;
  avatar?: string | null;
  email?: string | null;
}

export interface Repository {
  id: string;
  name: string;
  fullName?: string;
  description?: string;
  language?: string;
  languageColor?: string;
  lastUpdated?: string;
  isMonitored?: boolean;
  stars?: number;
  commits?: number | null;
  url?: string;
}

export interface CommitFile {
  filename?: string;
  additions?: number;
  deletions?: number;
}

export interface Commit {
  id: string;
  sha: string;
  fullSha?: string;
  message?: string;
  author?: string;
  authorAvatar?: string;
  repoName?: string;
  repoFullName?: string;
  timestamp?: string;
  filesChanged?: number;
  additions?: number;
  deletions?: number;
  hasDocumentation?: boolean;
  files?: CommitFile[];
}

export interface Documentation {
  commitSha: string;
  commitFullSha: string;
  repoName: string;
  repoFullName: string;
  generatedAt: string;
  plainText?: string;
  researchStyle?: string;
  latex?: string;
}
