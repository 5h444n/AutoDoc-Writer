import React, { useState } from 'react';
import {
  FileText,
  FileCode,
  FileType,
  Download,
  Copy,
  Check,
  Mail,
  Clock,
} from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/Button';
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip';
import { EmptyState } from '@/components/ui/EmptyState';
import { Documentation } from '@/lib/types';
import { formatRelativeTime } from '@/lib/format';
import { toast } from 'sonner';
import { useNavigate } from 'react-router-dom';
import { cn } from '@/lib/utils';

const exportFormats = [
  {
    id: 'pdf',
    name: 'PDF Document',
    icon: FileText,
    extension: '.pdf',
    description: 'Formatted document with styling',
    available: true,
  },
  {
    id: 'markdown',
    name: 'Markdown',
    icon: FileType,
    extension: '.md',
    description: 'Plain text with formatting syntax',
    available: true,
  },
  {
    id: 'latex',
    name: 'LaTeX',
    icon: FileCode,
    extension: '.tex',
    description: 'Academic/scientific document format',
    available: true,
  },
  {
    id: 'txt',
    name: 'Plain Text',
    icon: FileText,
    extension: '.txt',
    description: 'Simple unformatted text',
    available: true,
  },
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

export default function Export() {
  const [copiedFormat, setCopiedFormat] = useState<string | null>(null);
  const [downloadingFormat, setDownloadingFormat] = useState<string | null>(null);
  const navigate = useNavigate();
  const doc = loadStoredDocumentation();

  if (!doc) {
    return (
      <EmptyState
        icon={FileText}
        title="No documentation to export"
        description="Generate documentation from a commit to enable exports."
        action={{
          label: 'Browse commits',
          onClick: () => navigate('/commits'),
        }}
      />
    );
  }

  const contentForFormat = (formatId: string) => {
    if (formatId === 'latex') return doc.latex || '';
    if (formatId === 'markdown') return doc.researchStyle || '';
    return doc.plainText || '';
  };

  const handleCopy = async (formatId: string) => {
    const content = contentForFormat(formatId);
    if (!content) {
      toast.error('This format has not been generated yet.');
      return;
    }
    await navigator.clipboard.writeText(content);
    setCopiedFormat(formatId);
    toast.success('Copied to clipboard!');
    setTimeout(() => setCopiedFormat(null), 2000);
  };

  const handleDownload = async (formatId: string) => {
    setDownloadingFormat(formatId);
    await new Promise((resolve) => setTimeout(resolve, 600));

    const content = contentForFormat(formatId);
    if (!content) {
      setDownloadingFormat(null);
      toast.error('This format has not been generated yet.');
      return;
    }
    const format = exportFormats.find((f) => f.id === formatId)!;
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `documentation${format.extension}`;
    a.click();
    URL.revokeObjectURL(url);

    setDownloadingFormat(null);
    toast.success(`Downloaded as ${format.name}!`);
  };

  return (
    <div className="space-y-6 page-enter">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-foreground">Export & Sharing</h1>
        <p className="text-sm text-muted-foreground mt-1">
          Download or share your documentation in various formats
        </p>
      </div>

      {/* Document Info */}
      <Card className="border-border bg-card">
        <CardContent className="p-4">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center">
              <FileText className="w-6 h-6 text-primary" />
            </div>
            <div className="flex-1">
              <h3 className="font-medium text-foreground">Generated Documentation</h3>
              <p className="text-sm text-muted-foreground">
                Generated from <code className="text-xs bg-muted px-1.5 py-0.5 rounded font-mono">{doc.commitSha}</code> in{' '}
                <span className="text-primary">{doc.repoName}</span>
              </p>
            </div>
            <div className="flex items-center gap-1 text-sm text-muted-foreground">
              <Clock className="w-4 h-4" />
              <span>{formatRelativeTime(doc.generatedAt)}</span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Export Formats */}
      <div className="grid sm:grid-cols-2 gap-4">
        {exportFormats.map((format, index) => (
          <Card
            key={format.id}
            className="border-border bg-card card-lift stagger-enter"
            style={{ animationDelay: `${index * 80}ms` }}
          >
            <CardContent className="p-4">
              <div className="flex items-start gap-4">
                <div className={cn(
                  'w-12 h-12 rounded-lg flex items-center justify-center transition-colors',
                  'bg-secondary text-secondary-foreground'
                )}>
                  <format.icon className="w-6 h-6" />
                </div>
                <div className="flex-1">
                  <h3 className="font-medium text-foreground">{format.name}</h3>
                  <p className="text-sm text-muted-foreground mb-3">{format.description}</p>
                  <div className="flex items-center gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      className="gap-1.5"
                      onClick={() => handleCopy(format.id)}
                    >
                      {copiedFormat === format.id ? (
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
                      size="sm"
                      className="gap-1.5"
                      onClick={() => handleDownload(format.id)}
                      disabled={downloadingFormat === format.id}
                    >
                      {downloadingFormat === format.id ? (
                        <>
                          <div className="w-3.5 h-3.5 border-2 border-primary-foreground/30 border-t-primary-foreground rounded-full animate-spin" />
                          Preparing...
                        </>
                      ) : (
                        <>
                          <Download className="w-3.5 h-3.5" />
                          Download {format.extension}
                        </>
                      )}
                    </Button>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Email Sharing (Coming Soon) */}
      <Card className="border-border bg-card opacity-75">
        <CardContent className="p-4">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-lg bg-muted flex items-center justify-center">
              <Mail className="w-6 h-6 text-muted-foreground" />
            </div>
            <div className="flex-1">
              <h3 className="font-medium text-foreground">Send to Email</h3>
              <p className="text-sm text-muted-foreground">Share documentation directly via email</p>
            </div>
            <Tooltip>
              <TooltipTrigger asChild>
                <Button variant="outline" size="sm" disabled className="gap-1.5">
                  <Mail className="w-3.5 h-3.5" />
                  Coming Soon
                </Button>
              </TooltipTrigger>
              <TooltipContent>
                <p>This feature is planned for a future update</p>
              </TooltipContent>
            </Tooltip>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
