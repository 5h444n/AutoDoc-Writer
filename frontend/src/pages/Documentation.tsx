import React, { useEffect, useRef, useState } from 'react';
import {
  FileText,
  GraduationCap,
  Code,
  Copy,
  Download,
  RefreshCw,
  Check,
  Clock,
  GitCommit,
} from 'lucide-react';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { EmptyState } from '@/components/ui/EmptyState';
import { Documentation } from '@/lib/types';
import { generateDocs } from '@/lib/api';
import { formatRelativeTime } from '@/lib/format';
import { cn } from '@/lib/utils';
import { toast } from 'sonner';
import { useLocation, useNavigate } from 'react-router-dom';
import { useApp } from '@/context/AppContext';

type TabValue = 'plainText' | 'research' | 'latex';

const tabs = [
  { value: 'plainText' as TabValue, label: 'Plain Text', icon: FileText },
  { value: 'research' as TabValue, label: 'Research Style', icon: GraduationCap },
  { value: 'latex' as TabValue, label: 'LaTeX', icon: Code },
];

function loadStoredDocumentation() {
  const stored = localStorage.getItem('latest_documentation');
  if (!stored) {
    return null;
  }
  try {
    return JSON.parse(stored) as Documentation;
  } catch {
    return null;
  }
}

export default function Documentation() {
  const location = useLocation();
  const navigate = useNavigate();
  const { textComplexity } = useApp();
  const [doc, setDoc] = useState<Documentation | null>(() => {
    const stateDoc = (location.state as { documentation?: Documentation } | null)?.documentation;
    return stateDoc || loadStoredDocumentation();
  });
  const [isRegenerating, setIsRegenerating] = useState(false);
  const [copiedTab, setCopiedTab] = useState<TabValue | null>(null);
  const [activeTab, setActiveTab] = useState<TabValue>('plainText');
  const inkBarRef = useRef<HTMLDivElement>(null);
  const tabsRef = useRef<HTMLDivElement>(null);
  const activeTabLabel = tabs.find((tab) => tab.value === activeTab)?.label || 'Format';

  useEffect(() => {
    if (tabsRef.current && inkBarRef.current) {
      const activeTabEl = tabsRef.current.querySelector(`[data-state="active"]`);
      if (activeTabEl) {
        const { offsetLeft, offsetWidth } = activeTabEl as HTMLElement;
        inkBarRef.current.style.left = `${offsetLeft}px`;
        inkBarRef.current.style.width = `${offsetWidth}px`;
      }
    }
  }, [activeTab]);

  useEffect(() => {
    const stateDoc = (location.state as { documentation?: Documentation } | null)?.documentation;
    if (stateDoc) {
      setDoc(stateDoc);
      localStorage.setItem('latest_documentation', JSON.stringify(stateDoc));
    }
  }, [location.state]);

  const getContent = (tab: TabValue) => {
    if (!doc) return '';
    switch (tab) {
      case 'plainText':
        return doc.plainText || '';
      case 'research':
        return doc.researchStyle || '';
      case 'latex':
        return doc.latex || '';
    }
  };

  const handleCopy = async (tab: TabValue) => {
    if (!doc) return;
    await navigator.clipboard.writeText(getContent(tab));
    setCopiedTab(tab);
    toast.success('Copied to clipboard!');
    setTimeout(() => setCopiedTab(null), 2000);
  };

  const handleDownload = (tab: TabValue) => {
    if (!doc) return;
    const content = getContent(tab);
    if (!content) {
      toast.error('This format has not been generated yet.');
      return;
    }
    const extensions = { plainText: 'txt', research: 'md', latex: 'tex' };
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `documentation.${extensions[tab]}`;
    a.click();
    URL.revokeObjectURL(url);
    toast.success('Downloaded successfully!');
  };

  const handleGenerateForStyle = async (style: TabValue, force = false) => {
    if (!doc) return;
    if (!doc.repoFullName || !doc.commitFullSha) {
      toast.error('Missing commit details for regeneration.');
      return;
    }
    setIsRegenerating(true);
    try {
      const result = await generateDocs({
        repoFullName: doc.repoFullName,
        commitSha: doc.commitFullSha,
        complexity: textComplexity,
        style,
        force,
      });
      const updated: Documentation = {
        commitSha: result.commit_short_sha || doc.commitSha,
        commitFullSha: result.commit_sha,
        repoName: result.repo_name,
        repoFullName: result.repo_full_name,
        generatedAt: result.generated_at,
        plainText: result.plain_text || doc.plainText || '',
        researchStyle: result.research_style || doc.researchStyle || '',
        latex: result.latex || doc.latex || '',
      };
      localStorage.setItem('latest_documentation', JSON.stringify(updated));
      setDoc(updated);
      toast.success(force ? 'Documentation regenerated!' : 'Documentation generated!');
    } catch {
      toast.error('Failed to generate documentation.');
    } finally {
      setIsRegenerating(false);
    }
  };

  const handleRegenerate = async () => {
    await handleGenerateForStyle(activeTab, true);
  };

  if (!doc) {
    return (
      <EmptyState
        icon={FileText}
        title="No documentation generated yet"
        description="Generate documentation from a commit to view it here."
        action={{
          label: 'Browse commits',
          onClick: () => navigate('/commits'),
        }}
      />
    );
  }

  return (
    <div className="space-y-6 page-enter">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-foreground">Documentation Viewer</h1>
          <p className="text-sm text-muted-foreground mt-1">
            View, copy, and export generated documentation
          </p>
        </div>

        <Button
          variant="outline"
          className="gap-2"
          onClick={handleRegenerate}
          disabled={isRegenerating}
        >
          <RefreshCw className={cn('w-4 h-4', isRegenerating && 'animate-spin')} />
          {isRegenerating ? 'Regenerating...' : `Regenerate ${activeTabLabel}`}
        </Button>
      </div>

      {/* Commit Info Header */}
      <Card className="border-border bg-card">
        <CardContent className="p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                <GitCommit className="w-5 h-5 text-primary" />
              </div>
              <div>
                <p className="font-medium text-foreground">
                  Generated from commit <code className="text-xs bg-muted px-1.5 py-0.5 rounded font-mono">{doc.commitSha}</code>
                </p>
                <div className="flex items-center gap-2 text-sm text-muted-foreground mt-0.5">
                  <span className="text-primary">{doc.repoName}</span>
                  <span>|</span>
                  <span className="flex items-center gap-1">
                    <Clock className="w-3.5 h-3.5" />
                    {formatRelativeTime(doc.generatedAt)}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Generating State Overlay - shown when regenerating */}
      {isRegenerating && (
        <div className="fixed inset-0 bg-background/80 backdrop-blur-sm z-50 flex items-center justify-center animate-fade-in">
          <Card className="w-96 border-border bg-card scanline">
            <CardContent className="p-8 text-center">
              <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-4">
                <RefreshCw className="w-8 h-8 text-primary animate-spin" />
              </div>
              <h3 className="text-lg font-semibold text-foreground mb-2">
                Regenerating Documentation
              </h3>
              <p className="text-sm text-muted-foreground">
                Analyzing code changes and generating fresh documentation
                <span className="typing-dots" />
              </p>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={(v) => setActiveTab(v as TabValue)}>
        <div className="relative" ref={tabsRef}>
          <TabsList className="bg-muted/50 p-1 rounded-lg w-full sm:w-auto grid grid-cols-3 sm:inline-grid gap-1">
            {tabs.map((tab) => (
              <TabsTrigger
                key={tab.value}
                value={tab.value}
                className="gap-2 data-[state=active]:bg-card data-[state=active]:text-foreground data-[state=active]:shadow-sm transition-all duration-200"
              >
                <tab.icon className="w-4 h-4" />
                <span className="hidden sm:inline">{tab.label}</span>
              </TabsTrigger>
            ))}
          </TabsList>
          <div
            ref={inkBarRef}
            className="absolute bottom-0 h-0.5 bg-primary transition-all duration-300 ease-out rounded-full"
          />
        </div>

        {tabs.map((tab) => (
          <TabsContent
            key={tab.value}
            value={tab.value}
            className="mt-6 animate-fade-in"
          >
            <Card className="border-border bg-card">
              <CardHeader className="pb-2 flex flex-row items-center justify-between">
                <div className="flex items-center gap-2">
                  <tab.icon className="w-5 h-5 text-primary" />
                  <span className="font-medium text-foreground">{tab.label}</span>
                </div>
                <div className="flex items-center gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    className="gap-1.5"
                    onClick={() => handleCopy(tab.value)}
                  >
                    {copiedTab === tab.value ? (
                      <>
                        <Check className="w-3.5 h-3.5 text-accent success-check" />
                        Copied
                      </>
                    ) : (
                      <>
                        <Copy className="w-3.5 h-3.5" />
                        Copy
                      </>
                    )}
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    className="gap-1.5"
                    onClick={() => handleDownload(tab.value)}
                  >
                    <Download className="w-3.5 h-3.5" />
                    Download
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                {getContent(tab.value) ? (
                  <div className="code-block max-h-[60vh] overflow-y-auto">
                    <pre className="whitespace-pre-wrap text-foreground font-mono text-sm leading-relaxed">
                      {getContent(tab.value)}
                    </pre>
                  </div>
                ) : (
                  <div className="rounded-lg border border-dashed border-border p-6 text-center text-sm text-muted-foreground space-y-3">
                    <p>This format has not been generated yet.</p>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleGenerateForStyle(tab.value, false)}
                      disabled={isRegenerating}
                    >
                      Generate {tab.label}
                    </Button>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>
        ))}
      </Tabs>
    </div>
  );
}
