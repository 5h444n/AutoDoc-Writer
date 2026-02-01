import React, { useState } from 'react';
import { Github, FileText, GitCommit, Sparkles, ArrowRight, CheckCircle } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { useAuth } from '@/context/AuthContext';
import { cn } from '@/lib/utils';

const features = [
  {
    icon: Github,
    title: 'Connect GitHub',
    description: 'Seamlessly link your repositories with OAuth',
  },
  {
    icon: GitCommit,
    title: 'Detect Commits',
    description: 'Automatic monitoring of code changes',
  },
  {
    icon: FileText,
    title: 'Generate Docs',
    description: 'Plain Text, Research, and LaTeX formats',
  },
];

export default function WelcomePage() {
  const { login, isLoading } = useAuth();
  const [hoveredFeature, setHoveredFeature] = useState<number | null>(null);

  const handleLogin = () => {
    login();
  };

  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Header */}
      <header className="p-4 flex items-center justify-between border-b border-border">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-gradient-primary flex items-center justify-center">
            <span className="text-primary-foreground font-bold text-sm">AD</span>
          </div>
          <span className="font-semibold text-foreground">AutoDoc Writer</span>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex items-center justify-center px-4 py-12">
        <div className="max-w-3xl mx-auto text-center">
          {/* Hero */}
          <div className="mb-12 animate-fade-in">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-primary/10 text-primary text-sm font-medium mb-6 animate-bounce-soft">
              <Sparkles className="w-4 h-4" />
              <span>AI-Powered Documentation</span>
            </div>
            
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-foreground mb-4 leading-tight">
              Turn your code into
              <br />
              <span className="text-gradient">documentation—automatically</span>
            </h1>
            
            <p className="text-lg text-muted-foreground max-w-xl mx-auto mb-8">
              Connect your GitHub repositories, monitor commits in real-time, and generate 
              beautiful documentation in multiple formats with a single click.
            </p>

            {/* CTA Button */}
            <Button
              size="lg"
              onClick={handleLogin}
              disabled={isLoading}
              className="h-12 px-8 text-base font-semibold gap-2 bg-gradient-primary hover:opacity-90 transition-all duration-200 shadow-glow hover:shadow-glow animate-scale-in"
            >
              {isLoading ? (
                <>
                  <div className="w-5 h-5 border-2 border-primary-foreground/30 border-t-primary-foreground rounded-full animate-spin" />
                  <span>Connecting...</span>
                </>
              ) : (
                <>
                  <Github className="w-5 h-5" />
                  <span>Sign in with GitHub</span>
                  <ArrowRight className="w-4 h-4 ml-1" />
                </>
              )}
            </Button>
          </div>

          {/* Features */}
          <div className="grid md:grid-cols-3 gap-6">
            {features.map((feature, index) => (
              <div
                key={feature.title}
                className={cn(
                  'p-6 rounded-xl border border-border bg-card transition-all duration-300 cursor-pointer',
                  hoveredFeature === index ? 'border-primary/50 shadow-glow scale-105' : 'hover:border-border hover:bg-card/80'
                )}
                style={{ animationDelay: `${index * 100 + 200}ms` }}
                onMouseEnter={() => setHoveredFeature(index)}
                onMouseLeave={() => setHoveredFeature(null)}
              >
                <div className={cn(
                  'w-12 h-12 rounded-lg flex items-center justify-center mb-4 transition-all duration-300',
                  hoveredFeature === index ? 'bg-primary text-primary-foreground scale-110' : 'bg-muted text-muted-foreground'
                )}>
                  <feature.icon className="w-6 h-6" />
                </div>
                <h3 className="text-lg font-semibold text-foreground mb-2">{feature.title}</h3>
                <p className="text-sm text-muted-foreground">{feature.description}</p>
                
                {hoveredFeature === index && (
                  <div className="mt-4 flex items-center gap-1 text-primary text-sm font-medium animate-fade-in">
                    <span>Learn more</span>
                    <ArrowRight className="w-4 h-4" />
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Output Formats */}
          <div className="mt-16 animate-fade-in" style={{ animationDelay: '600ms' }}>
            <p className="text-sm text-muted-foreground mb-4">Generate documentation in multiple formats</p>
            <div className="flex items-center justify-center gap-3 flex-wrap">
              {['Plain Text', 'Research Style', 'LaTeX'].map((format, i) => (
                <div
                  key={format}
                  className="flex items-center gap-2 px-4 py-2 rounded-lg bg-muted/50 border border-border text-sm font-medium text-foreground"
                >
                  <CheckCircle className="w-4 h-4 text-accent" />
                  {format}
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="p-4 border-t border-border text-center text-sm text-muted-foreground">
        <p>Secure OAuth authentication | No password storage | Your data stays private</p>
      </footer>
    </div>
  );
}
