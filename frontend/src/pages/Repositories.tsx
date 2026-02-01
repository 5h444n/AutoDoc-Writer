import React, { useState, useEffect } from 'react';
import { Search, Filter, GitBranch, Star, GitCommit, FileText, Eye } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/input';
import { Switch } from '@/components/ui/switch';
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
import { fetchRepositories, toggleRepoMonitoring } from '@/lib/api';
import { Repository } from '@/lib/types';
import { formatRelativeTime, getLanguageColor } from '@/lib/format';
import { useNavigate } from 'react-router-dom';
import { toast } from 'sonner';

export default function Repositories() {
  const [isLoading, setIsLoading] = useState(true);
  const [repos, setRepos] = useState<Repository[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [filter, setFilter] = useState<'all' | 'active' | 'inactive'>('all');
  const [sortBy, setSortBy] = useState<'recent' | 'name'>('recent');
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    let isMounted = true;
    fetchRepositories(true)
      .then((data) => {
        if (!isMounted) return;
        const mapped = (data.repos || []).map((repo: any) => ({
          id: String(repo.id ?? repo.full_name ?? repo.name),
          name: repo.name,
          fullName: repo.full_name ?? repo.name,
          description: repo.description || 'No description provided.',
          language: repo.language || 'Unknown',
          languageColor: getLanguageColor(repo.language),
          lastUpdated: formatRelativeTime(repo.last_updated),
          isMonitored: repo.is_active ?? false,
          stars: repo.stars ?? 0,
          commits: repo.commits ?? null,
          url: repo.url,
        }));
        setRepos(mapped);
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
  }, []);

  const toggleMonitoring = async (repo: Repository) => {
    const nextState = !repo.isMonitored;
    setRepos((prev) =>
      prev.map((item) =>
        item.id === repo.id ? { ...item, isMonitored: nextState } : item
      )
    );

    try {
      await toggleRepoMonitoring(repo.name, nextState);
      toast.success(
        nextState ? `Started monitoring ${repo.name}` : `Stopped monitoring ${repo.name}`
      );
    } catch (err) {
      setRepos((prev) =>
        prev.map((item) =>
          item.id === repo.id ? { ...item, isMonitored: !nextState } : item
        )
      );
      toast.error('Failed to update monitoring status.');
    }
  };

  const filteredRepos = repos
    .filter((repo) => {
      if (filter === 'active') return repo.isMonitored;
      if (filter === 'inactive') return !repo.isMonitored;
      return true;
    })
    .filter((repo) => {
      const description = repo.description || '';
      return (
        repo.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        description.toLowerCase().includes(searchQuery.toLowerCase())
      );
    })
    .sort((a, b) => {
      if (sortBy === 'name') return a.name.localeCompare(b.name);
      return 0;
    });

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div className="h-8 w-32 rounded shimmer" />
          <div className="h-10 w-64 rounded shimmer" />
        </div>
        <SkeletonList count={4} />
      </div>
    );
  }

  if (error) {
    return (
      <EmptyState
        icon={GitBranch}
        title="Failed to load repositories"
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
          <h1 className="text-2xl font-bold text-foreground">Repositories</h1>
          <p className="text-sm text-muted-foreground mt-1">
            {repos.filter((r) => r.isMonitored).length} of {repos.length} repositories monitored
          </p>
        </div>

        <div className="flex items-center gap-3 w-full sm:w-auto">
          <div className="relative flex-1 sm:flex-initial">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search repositories..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-9 w-full sm:w-64"
            />
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="flex items-center gap-3 flex-wrap">
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-muted-foreground" />
          <Select value={filter} onValueChange={(v) => setFilter(v as typeof filter)}>
            <SelectTrigger className="w-32 bg-card">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All</SelectItem>
              <SelectItem value="active">Active</SelectItem>
              <SelectItem value="inactive">Inactive</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <Select value={sortBy} onValueChange={(v) => setSortBy(v as typeof sortBy)}>
          <SelectTrigger className="w-40 bg-card">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="recent">Recently Updated</SelectItem>
            <SelectItem value="name">Name</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Repository List */}
      {filteredRepos.length === 0 ? (
        <EmptyState
          icon={GitBranch}
          title="No repositories found"
          description="Try adjusting your search or filter to find what you're looking for."
          action={{
            label: 'Clear filters',
            onClick: () => {
              setSearchQuery('');
              setFilter('all');
            },
          }}
        />
      ) : (
        <div className="space-y-4">
          {filteredRepos.map((repo, index) => (
            <Card
              key={repo.id}
              className="border-border bg-card card-lift overflow-hidden stagger-enter"
              style={{ animationDelay: `${index * 60}ms` }}
            >
              <CardContent className="p-0">
                <div className="p-4 flex items-start justify-between gap-4">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <h3 className="font-semibold text-foreground hover:text-primary cursor-pointer transition-colors">
                        {repo.fullName}
                      </h3>
                      <StatusBadge status={repo.isMonitored ? 'active' : 'inactive'} />
                    </div>
                    <p className="text-sm text-muted-foreground mb-3 line-clamp-1">
                      {repo.description}
                    </p>
                    <div className="flex items-center gap-4 text-xs text-muted-foreground">
                      <span className="flex items-center gap-1">
                        <span
                          className="w-3 h-3 rounded-full"
                          style={{ backgroundColor: repo.languageColor }}
                        />
                        {repo.language}
                      </span>
                      <span className="flex items-center gap-1">
                        <Star className="w-3.5 h-3.5" />
                        {repo.stars}
                      </span>
                      <span className="flex items-center gap-1">
                        <GitCommit className="w-3.5 h-3.5" />
                        {repo.commits ?? '—'} commits
                      </span>
                      <span>Updated {repo.lastUpdated}</span>
                    </div>
                  </div>

                  <div className="flex items-center gap-3">
                    <div className="flex items-center gap-2">
                      <span className="text-sm text-muted-foreground">Monitor</span>
                      <Switch
                        checked={repo.isMonitored}
                        onCheckedChange={() => toggleMonitoring(repo)}
                      />
                    </div>
                  </div>
                </div>

                {/* Quick Actions - visible on hover */}
                <div className="px-4 pb-4 flex items-center gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    className="gap-1.5"
                    onClick={() => navigate('/commits')}
                  >
                    <Eye className="w-3.5 h-3.5" />
                    View Commits
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    className="gap-1.5"
                    onClick={() => {
                      toast.success('Select a commit to generate documentation.');
                      navigate('/commits');
                    }}
                  >
                    <FileText className="w-3.5 h-3.5" />
                    Generate Latest
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
