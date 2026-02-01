import React, { useEffect, useState } from 'react';
import {
  GitBranch,
  GitCommit,
  Clock,
  TrendingUp,
  FileText,
  ArrowRight,
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/Button';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { AnimatedCounter } from '@/components/ui/AnimatedCounter';
import { StatusBadge } from '@/components/ui/StatusBadge';
import { SkeletonCard } from '@/components/ui/SkeletonCard';
import { EmptyState } from '@/components/ui/EmptyState';
import { fetchCommits, fetchRepositories } from '@/lib/api';
import { Commit, Repository } from '@/lib/types';
import { formatRelativeTime, getLanguageColor } from '@/lib/format';
import { useNavigate } from 'react-router-dom';
import { cn } from '@/lib/utils';

export default function Dashboard() {
  const [isLoading, setIsLoading] = useState(true);
  const [lastUpdated, setLastUpdated] = useState(0);
  const [repos, setRepos] = useState<Repository[]>([]);
  const [commits, setCommits] = useState<Commit[]>([]);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const interval = setInterval(() => {
      setLastUpdated((prev) => prev + 1);
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    let isMounted = true;
    setIsLoading(true);

    Promise.all([fetchRepositories(false), fetchCommits(undefined, 10, false)])
      .then(([reposData, commitsData]) => {
        if (!isMounted) return;
        const mappedRepos = (reposData.repos || []).map((repo: any) => ({
          id: String(repo.id ?? repo.full_name ?? repo.name),
          name: repo.name,
          fullName: repo.full_name ?? repo.name,
          language: repo.language || 'Unknown',
          languageColor: getLanguageColor(repo.language),
          lastUpdated: formatRelativeTime(repo.last_updated),
          isMonitored: repo.is_active ?? false,
        }));
        const mappedCommits = (commitsData.commits || []).map((commit: any) => ({
          id: commit.id || commit.full_sha,
          sha: commit.sha || (commit.full_sha || '').slice(0, 7),
          fullSha: commit.full_sha || commit.id,
          message: commit.message || '',
          author: commit.author || 'Unknown',
          authorAvatar: commit.author_avatar || undefined,
          repoName: commit.repo_name || (commit.repo_full_name || '').split('/').pop() || '',
          repoFullName: commit.repo_full_name || '',
          timestamp: formatRelativeTime(commit.timestamp),
          hasDocumentation: commit.has_documentation ?? false,
        }));
        setRepos(mappedRepos);
        setCommits(mappedCommits);
        setError(null);
      })
      .catch((err: Error) => {
        if (!isMounted) return;
        setError(err.message || 'Failed to load dashboard data.');
      })
      .finally(() => {
        if (!isMounted) return;
        setIsLoading(false);
      });

    return () => {
      isMounted = false;
    };
  }, []);

  const activeRepos = repos.filter((r) => r.isMonitored).length;
  const totalCommits = commits.length;
  const recentCommits = commits.slice(0, 5);

  const stats = [
    {
      label: 'Connected Repos',
      value: repos.length,
      icon: GitBranch,
      color: 'text-primary',
    },
    {
      label: 'Active Monitoring',
      value: activeRepos,
      icon: TrendingUp,
      color: 'text-accent',
    },
    {
      label: 'Recent Commits',
      value: totalCommits,
      icon: GitCommit,
      color: 'text-primary',
    },
    {
      label: 'Docs Generated',
      value: commits.filter((c) => c.hasDocumentation).length,
      icon: FileText,
      color: 'text-accent',
    },
  ];

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {[1, 2, 3, 4].map((i) => (
            <Card key={i} className="animate-fade-in" style={{ animationDelay: `${i * 50}ms` }}>
              <CardContent className="p-4">
                <div className="h-4 w-20 rounded shimmer mb-2" />
                <div className="h-8 w-16 rounded shimmer" />
              </CardContent>
            </Card>
          ))}
        </div>
        <div className="grid lg:grid-cols-2 gap-6">
          <SkeletonCard lines={4} />
          <SkeletonCard lines={4} />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <EmptyState
        icon={GitBranch}
        title="Unable to load dashboard"
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
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-foreground">Dashboard</h1>
          <p className="text-sm text-muted-foreground flex items-center gap-1 mt-1">
            <Clock className="w-3.5 h-3.5" />
            <span>Last updated {lastUpdated} seconds ago</span>
            <span className="w-1.5 h-1.5 rounded-full bg-accent ml-1 pulse-dot" />
          </p>
        </div>
        <Button onClick={() => navigate('/repositories')} className="gap-2">
          <span>View All Repos</span>
          <ArrowRight className="w-4 h-4" />
        </Button>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat, index) => (
          <Card
            key={stat.label}
            className="card-lift animate-fade-in border-border bg-card"
            style={{ animationDelay: `${index * 100}ms` }}
          >
            <CardContent className="p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-muted-foreground">{stat.label}</span>
                <stat.icon className={cn('w-5 h-5', stat.color)} />
              </div>
              <div className="text-3xl font-bold text-foreground">
                <AnimatedCounter value={stat.value} duration={1500} />
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        {/* Monitoring Status */}
        <Card className="border-border bg-card">
          <CardHeader className="pb-3">
            <CardTitle className="text-lg font-semibold flex items-center justify-between">
              <span>Monitoring Status</span>
              <Button variant="ghost" size="sm" onClick={() => navigate('/repositories')}>
                View all
              </Button>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {repos.slice(0, 4).map((repo, index) => (
              <div
                key={repo.id}
                className="flex items-center justify-between p-3 rounded-lg bg-secondary/30 hover:bg-secondary/50 transition-all duration-200 cursor-pointer card-lift stagger-enter"
                style={{ animationDelay: `${index * 80}ms` }}
                onClick={() => navigate('/repositories')}
              >
                <div className="flex items-center gap-3">
                  <div
                    className="w-3 h-3 rounded-full"
                    style={{ backgroundColor: repo.languageColor }}
                  />
                  <div>
                    <p className="font-medium text-foreground text-sm">{repo.name}</p>
                    <p className="text-xs text-muted-foreground">{repo.lastUpdated}</p>
                  </div>
                </div>
                <StatusBadge status={repo.isMonitored ? 'active' : 'inactive'} />
              </div>
            ))}
          </CardContent>
        </Card>

        {/* Commit Activity Feed */}
        <Card className="border-border bg-card">
          <CardHeader className="pb-3">
            <CardTitle className="text-lg font-semibold flex items-center justify-between">
              <span>Commit Activity</span>
              <Button variant="ghost" size="sm" onClick={() => navigate('/commits')}>
                View all
              </Button>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {recentCommits.map((commit, index) => (
              <div
                key={commit.id}
                className="flex items-start gap-3 p-3 rounded-lg bg-secondary/30 hover:bg-secondary/50 transition-all duration-200 cursor-pointer card-lift stagger-enter"
                style={{ animationDelay: `${index * 80}ms` }}
                onClick={() => navigate('/commits')}
              >
                <Avatar className="w-8 h-8">
                  <AvatarImage src={commit.authorAvatar} />
                  <AvatarFallback>{commit.author.charAt(0)}</AvatarFallback>
                </Avatar>
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-foreground font-medium truncate">
                    {commit.message}
                  </p>
                  <div className="flex items-center gap-2 mt-1">
                    <span className="text-xs text-primary font-medium">{commit.repoName}</span>
                    <span className="text-xs text-muted-foreground">|</span>
                    <span className="text-xs text-muted-foreground">{commit.timestamp}</span>
                  </div>
                </div>
                {commit.hasDocumentation && (
                  <FileText className="w-4 h-4 text-accent shrink-0" />
                )}
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
