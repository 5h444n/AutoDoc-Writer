import React from 'react';
import {
  HelpCircle,
  ExternalLink,
  Github,
  FileText,
  Zap,
  Shield,
  Mail,
  Heart,
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/Button';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion';
import { Separator } from '@/components/ui/separator';

const faqs = [
  {
    question: 'How does AutoDoc Writer generate documentation?',
    answer: 'AutoDoc Writer analyzes your code changes, understands the context, structure, and patterns, then generates human-readable documentation using advanced AI models. It supports Plain Text, Research/Thesis style, and LaTeX formats.',
  },
  {
    question: 'Is my code secure?',
    answer: 'Absolutely. We use OAuth for authentication, meaning we never store your password. Code is processed on-demand and not stored on our servers. All generated documentation is kept locally on your device unless you choose to export it.',
  },
  {
    question: 'Can I use AutoDoc Writer offline?',
    answer: 'Yes! Previously generated documentation is cached locally and accessible offline. However, generating new documentation requires an internet connection to analyze commits.',
  },
  {
    question: 'What formats are supported?',
    answer: 'AutoDoc Writer generates documentation in three formats: Plain Text for quick reading, Research/Thesis Style for academic purposes, and LaTeX for professional scientific documents.',
  },
  {
    question: 'How do I start monitoring a repository?',
    answer: 'Navigate to the Repositories page, find the repository you want to monitor, and toggle the "Monitor" switch. AutoDoc Writer will then track new commits and allow you to generate documentation for them.',
  },
];

const features = [
  {
    icon: Github,
    title: 'GitHub Integration',
    description: 'Seamless OAuth connection with your GitHub account',
  },
  {
    icon: Zap,
    title: 'Real-time Monitoring',
    description: 'Automatic detection of new commits across repositories',
  },
  {
    icon: FileText,
    title: 'Multi-format Output',
    description: 'Plain Text, Research Style, and LaTeX documentation',
  },
  {
    icon: Shield,
    title: 'Privacy First',
    description: 'Local storage and on-demand processing only',
  },
];

export default function Help() {
  return (
    <div className="space-y-6 page-enter max-w-3xl">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-foreground">Help & About</h1>
        <p className="text-sm text-muted-foreground mt-1">
          Learn more about AutoDoc Writer and get answers to common questions
        </p>
      </div>

      {/* About Section */}
      <Card className="border-border bg-card overflow-hidden">
        <div className="bg-gradient-primary p-6 text-center">
          <div className="w-16 h-16 rounded-2xl bg-background/10 backdrop-blur flex items-center justify-center mx-auto mb-4">
            <span className="text-2xl font-bold text-primary-foreground">AD</span>
          </div>
          <h2 className="text-xl font-bold text-primary-foreground">AutoDoc Writer</h2>
          <p className="text-primary-foreground/80 text-sm mt-1">
            Turn your code into documentation—automatically
          </p>
          <p className="text-primary-foreground/60 text-xs mt-2">Version 1.0.0</p>
        </div>
        <CardContent className="p-6">
          <p className="text-sm text-muted-foreground leading-relaxed">
            AutoDoc Writer is an intelligent documentation generator that connects to your GitHub repositories, 
            monitors commits in real-time, and creates comprehensive documentation in multiple formats. 
            Whether you need quick plain text summaries, academic-style research documents, or professional 
            LaTeX papers, AutoDoc Writer has you covered.
          </p>
        </CardContent>
      </Card>

      {/* Features */}
      <Card className="border-border bg-card">
        <CardHeader>
          <CardTitle className="text-lg">Features</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid sm:grid-cols-2 gap-4">
            {features.map((feature, index) => (
              <div
                key={feature.title}
                className="flex items-start gap-3 p-3 rounded-lg bg-secondary/30 stagger-enter"
                style={{ animationDelay: `${index * 80}ms` }}
              >
                <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center shrink-0">
                  <feature.icon className="w-5 h-5 text-primary" />
                </div>
                <div>
                  <h4 className="font-medium text-foreground">{feature.title}</h4>
                  <p className="text-sm text-muted-foreground">{feature.description}</p>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* FAQ */}
      <Card className="border-border bg-card">
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <HelpCircle className="w-5 h-5" />
            Frequently Asked Questions
          </CardTitle>
        </CardHeader>
        <CardContent>
          <Accordion type="single" collapsible className="w-full">
            {faqs.map((faq, index) => (
              <AccordionItem key={index} value={`item-${index}`} className="border-border">
                <AccordionTrigger className="text-left text-foreground hover:text-foreground">
                  {faq.question}
                </AccordionTrigger>
                <AccordionContent className="text-muted-foreground">
                  {faq.answer}
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </CardContent>
      </Card>

      {/* Contact & Links */}
      <Card className="border-border bg-card">
        <CardHeader>
          <CardTitle className="text-lg">Need More Help?</CardTitle>
          <CardDescription>Get in touch or explore our resources</CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          <Button variant="outline" className="w-full justify-start gap-2">
            <Mail className="w-4 h-4" />
            Contact Support
            <ExternalLink className="w-3.5 h-3.5 ml-auto text-muted-foreground" />
          </Button>
          <Button variant="outline" className="w-full justify-start gap-2">
            <Github className="w-4 h-4" />
            View on GitHub
            <ExternalLink className="w-3.5 h-3.5 ml-auto text-muted-foreground" />
          </Button>
          <Button variant="outline" className="w-full justify-start gap-2">
            <FileText className="w-4 h-4" />
            Documentation
            <ExternalLink className="w-3.5 h-3.5 ml-auto text-muted-foreground" />
          </Button>
        </CardContent>
      </Card>

      {/* Footer */}
      <div className="text-center py-4">
        <p className="text-sm text-muted-foreground flex items-center justify-center gap-1">
          Made with <Heart className="w-4 h-4 text-destructive fill-destructive" /> by AutoDoc Team
        </p>
        <p className="text-xs text-muted-foreground mt-1">© 2024 AutoDoc Writer. All rights reserved.</p>
      </div>
    </div>
  );
}
