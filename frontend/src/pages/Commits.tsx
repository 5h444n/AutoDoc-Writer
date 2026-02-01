import React, { useEffect, useState } from 'react';
import {
  Search,
  Filter,
  GitCommit,
  FileText,
  Plus,
  Minus,
  FileCode,
  Sparkles,
} from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/input';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { StatusBadge } from '@/components/ui/StatusBadge';
import { SkeletonList } from '@/components/ui/SkeletonCard';
import { EmptyState } from '@/components/ui/EmptyState';
import { fetchCommits, fetchRepositories, generateDocs } from '@/lib/api';
import { Commit, Documentation, Repository } from '@/lib/types';
import { formatRelativeTime } from '@/lib/format';
import { useApp } from '@/context/AppContext';
import { useNavigate } from 'react-router-dom';
import { toast } from 'sonner';

export default function Commits() {
  const [isLoading, setIsLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [repoFilter, setRepoFilter] = useState<string>('all');
  const [selectedCommit, setSelectedCommit] = useState<Commit | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [repos, setRepos] = useState<Repository[]>([]);
  const [commits, setCommits] = useState<Commit[]>([]);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();
  const { textComplexity, defaultFormat } = useApp();

  useEffect(() => {
    let isMounted = true;
    fetchRepositories(false)
      .then((data) => {
        if (!isMounted) return;
        const mapped = (data.repos || []).map((repo: any) => ({
          id: String(repo.id ?? repo.full_name ?? repo.name),
          name: repo.name,
          fullName: repo.full_name ?? repo.name,
          isMonitored: repo.is_active ?? false,
        }));
        setRepos(mapped);
      })
      .catch((err: Error) => {
        if (!isMounted) return;
        setError(err.message);
      });

    return () => {
      isMounted = false;
    };
  }, []);

  useEffect(() => {
    let isMounted = true;
    setIsLoading(true);
    setError(null);

    const repoName = repoFilter === 'all' ? undefined : repoFilter;
    const includeStats = repoFilter !== 'all';
    fetchCommits(repoName, 25, includeStats)
      .then((data) => {
        if (!isMounted) return;
        const mapped = (data.commits || []).map((commit: any) => ({
          id: commit.id || commit.full_sha,
          sha: commit.sha || (commit.full_sha || '').slice(0, 7),
          fullSha: commit.full_sha || commit.id,
          message: commit.message || '',
          author: commit.author || 'Unknown',
          authorAvatar: commit.author_avatar || undefined,
          repoName: commit.repo_name || (commit.repo_full_name || '').split('/').pop() || '',
          repoFullName: commit.repo_full_name || repoFilter,
          timestamp: formatRelativeTime(commit.timestamp),
          filesChanged: commit.files_changed ?? 0,
          additions: commit.additions ?? 0,
          deletions: commit.deletions ?? 0,
          hasDocumentation: commit.has_documentation ?? false,
          files: commit.files || [],
        }));
        setCommits(mapped);
      })
      .catch((err: Error) => {
        if (!isMounted) return;
        setError(err.message);
      })
      .finally(() => {
        if (!isMounted) return;
        setIsLoading(false);
      });

    return () => {
      isMounted = false;
    };
  }, [repoFilter]);

  const formatLabel =
    defaultFormat === 'plainText' ? 'Plain Text' : defaultFormat === 'research' ? 'Research Style' : 'LaTeX';

  const handleGenerate = async (commit: Commit) => {
    if (!commit.repoFullName || !commit.fullSha) {
      toast.error('Missing repository or commit details.');
      return;
    }
    setIsGenerating(true);
    toast.loading('Generating documentation...', { id: 'generate' });

    try {
      const result = await generateDocs({
        repoFullName: commit.repoFullName,
        commitSha: commit.fullSha,
        complexity: textComplexity,
        style: defaultFormat,
      });

      const stored = localStorage.getItem('latest_documentation');
      const existing = stored ? (JSON.parse(stored) as Documentation) : null;
      const isSameDoc =
        existing?.commitFullSha === result.commit_sha &&
        existing?.repoFullName === result.repo_full_name;

      const documentation: Documentation = {
        commitSha: result.commit_short_sha || commit.sha,
        commitFullSha: result.commit_sha,
        repoName: result.repo_name,
        repoFullName: result.repo_full_name,
        generatedAt: result.generated_at,
        plainText: result.plain_text || (isSameDoc ? existing?.plainText : '') || '',
        researchStyle: result.research_style || (isSameDoc ? existing?.researchStyle : '') || '',
        latex: result.latex || (isSameDoc ? existing?.latex : '') || '',
      };

      localStorage.setItem('latest_documentation', JSON.stringify(documentation));
      setCommits((prev) =>
        prev.map((item) =>
          item.id === commit.id ? { ...item, hasDocumentation: true } : item
        )
      );
      toast.success('Documentation generated successfully!', { id: 'generate' });
      setSelectedCommit(null);
      navigate('/documentation', { state: { documentation } });
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Documentation generation failed.';
      toast.error(message, { id: 'generate' });
    } finally {
      setIsGenerating(false);
    }
  };

  const filteredCommits = commits.filter((commit) => {
    if (repoFilter !== 'all' && commit.repoFullName !== repoFilter) return false;
    if (searchQuery) {
      return (
        commit.message.toLowerCase().includes(searchQuery.toLowerCase()) ||
        commit.sha.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }
    return true;
  });

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div className="h-8 w-32 rounded shimmer" />
          <div className="h-10 w-64 rounded shimmer" />
        </div>
        <SkeletonList count={5} />
      </div>
    );
  }

  if (error) {
    return (
      <EmptyState
        icon={GitCommit}
        title="Failed to load commits"
        description={error}
        action={{
          label: 'Retry',
          onClick: () => window.location.reload(),
        }}
      />
    );
  }

  return (
    <div className="space-y-6 page-enter">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-foreground">Commits</h1>
          <p className="text-sm text-muted-foreground mt-1">
            {commits.filter((c) => c.hasDocumentation).length} of {commits.length} commits have documentation
          </p>
        </div>

        <div className="flex items-center gap-3 w-full sm:w-auto">
          <div className="relative flex-1 sm:flex-initial">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search commits..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-9 w-full sm:w-64"
            />
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="flex items-center gap-3">
        <Filter className="w-4 h-4 text-muted-foreground" />
        <Select value={repoFilter} onValueChange={setRepoFilter}>
          <SelectTrigger className="w-48 bg-card">
            <SelectValue placeholder="All repositories" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All repositories</SelectItem>
            {repos.map((repo) => (
              <SelectItem key={repo.id} value={repo.fullName || repo.name}>
                {repo.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {/* Commit List */}
      {filteredCommits.length === 0 ? (
        <EmptyState
          icon={GitCommit}
          title="No commits found"
          description="Try adjusting your search or filter to find what you're looking for."
          action={{
            label: 'Clear filters',
            onClick: () => {
              setSearchQuery('');
              setRepoFilter('all');
            },
          }}
        />
      ) : (
        <div className="space-y-3">
          {filteredCommits.map((commit, index) => (
            <Card
              key={commit.id}
              className="border-border bg-card card-lift cursor-pointer stagger-enter"
              style={{ animationDelay: `${index * 50}ms` }}
              onClick={() => setSelectedCommit(commit)}
            >
              <CardContent className="p-4">
                <div className="flex items-start gap-4">
                  <Avatar className="w-10 h-10 shrink-0">
                    <AvatarImage src={commit.authorAvatar} />
                    <AvatarFallback>{commit.author.charAt(0)}</AvatarFallback>
                  </Avatar>

                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <h3 className="font-medium text-foreground mb-1">
                          {commit.message}
                        </h3>
                        <div className="flex items-center gap-3 text-sm text-muted-foreground">
                          <span className="text-primary font-medium">{commit.repoName}</span>
                          <span>|</span>
                          <code className="text-xs bg-muted px-1.5 py-0.5 rounded font-mono">
                            {commit.sha}
                          </code>
                          <span>|</span>
                          <span>{commit.timestamp}</span>
                        </div>
                      </div>

                      <div className="flex items-center gap-2 shrink-0">
                        {commit.hasDocumentation ? (
                          <StatusBadge status="success" label="Documented" />
                        ) : (
                          <Button
                            size="sm"
                            className="gap-1.5"
                            onClick={(e) => {
                              e.stopPropagation();
                              handleGenerate(commit);
                            }}
                          >
                            <FileText className="w-3.5 h-3.5" />
                            Generate
                          </Button>
                        )}
                      </div>
                    </div>

                    <div className="flex items-center gap-4 mt-3 text-xs text-muted-foreground">
                      <span className="flex items-center gap-1">
                        <FileCode className="w-3.5 h-3.5" />
                        {commit.filesChanged ?? 0} files
                      </span>
                      <span className="flex items-center gap-1 text-accent">
                        <Plus className="w-3.5 h-3.5" />
                        {commit.additions ?? 0}
                      </span>
                      <span className="flex items-center gap-1 text-destructive">
                        <Minus className="w-3.5 h-3.5" />
                        {commit.deletions ?? 0}
                      </span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Commit Detail Modal */}
      <Dialog open={!!selectedCommit} onOpenChange={() => setSelectedCommit(null)}>
        <DialogContent className="max-w-lg bg-card border-border">
          <DialogHeader>
            <DialogTitle className="text-foreground">Commit Details</DialogTitle>
          </DialogHeader>

          {selectedCommit && (
            <div className="space-y-4">
              <div className="flex items-center gap-3">
                <Avatar className="w-10 h-10">
                  <AvatarImage src={selectedCommit.authorAvatar} />
                  <AvatarFallback>{selectedCommit.author.charAt(0)}</AvatarFallback>
                </Avatar>
                <div>
                  <p className="font-medium text-foreground">{selectedCommit.author}</p>
                  <p className="text-sm text-muted-foreground">{selectedCommit.timestamp}</p>
                </div>
              </div>

              <div className="p-3 rounded-lg bg-secondary/50 border border-border">
                <p className="text-sm text-foreground">{selectedCommit.message}</p>
                <div className="flex items-center gap-2 mt-2">
                  <code className="text-xs bg-muted px-1.5 py-0.5 rounded font-mono text-muted-foreground">
                    {selectedCommit.sha}
                  </code>
                  <span className="text-xs text-primary">{selectedCommit.repoName}</span>
                </div>
              </div>

              <div>
                <h4 className="text-sm font-medium text-foreground mb-2">Changed Files</h4>
                <div className="space-y-1.5 max-h-40 overflow-y-auto">
                  {selectedCommit.files && selectedCommit.files.length > 0 ? (
                    selectedCommit.files.map((file, index) => {
                      const filename = file.filename || `file-${index}`;
                      return (
                        <div
                          key={filename}
                          className="flex items-center justify-between p-2 rounded bg-muted/50 text-sm"
                        >
                          <span className="font-mono text-xs text-foreground">{filename}</span>
                          <span className="text-xs text-muted-foreground">
                            +{file.additions} -{file.deletions}
                          </span>
                        </div>
                      );
                    })
                  ) : (
                    <div className="p-2 rounded bg-muted/50 text-sm text-muted-foreground">
                      No file details available.
                    </div>
                  )}
                </div>
              </div>

              <div className="flex items-center gap-4 pt-2 border-t border-border text-sm text-muted-foreground">
                <span className="flex items-center gap-1">
                  <FileCode className="w-4 h-4" />
                  {selectedCommit.filesChanged ?? 0} files changed
                </span>
                <span className="flex items-center gap-1 text-accent">
                  <Plus className="w-4 h-4" />
                  {selectedCommit.additions ?? 0} additions
                </span>
                <span className="flex items-center gap-1 text-destructive">
                  <Minus className="w-4 h-4" />
                  {selectedCommit.deletions ?? 0} deletions
                </span>
              </div>

              <Button
                className="w-full gap-2"
                onClick={() => handleGenerate(selectedCommit)}
                disabled={isGenerating}
              >
                {isGenerating ? (
                  <>
                    <Sparkles className="w-4 h-4 animate-spin" />
                    <span>Generating</span>
                    <span className="typing-dots" />
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4" />
                    Generate Documentation ({formatLabel})
                  </>
                )}
              </Button>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}
