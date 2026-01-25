import React, { useState } from 'react';
import {
  User,
  Github,
  FileText,
  Bell,
  Moon,
  Sun,
  Database,
  Trash2,
  LogOut,
  Shield,
  Lock,
  Eye,
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Switch } from '@/components/ui/switch';
import { Slider } from '@/components/ui/slider';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Separator } from '@/components/ui/separator';
import { useAuth } from '@/context/AuthContext';
import { useApp } from '@/context/AppContext';
import { useNavigate } from 'react-router-dom';
import { toast } from 'sonner';

export default function Settings() {
  const { user, logout } = useAuth();
  const {
    isDarkMode,
    toggleDarkMode,
    defaultFormat,
    setDefaultFormat,
    textComplexity,
    setTextComplexity,
    notificationsEnabled,
    setNotificationsEnabled,
    cacheEnabled,
    setCacheEnabled,
  } = useApp();
  const navigate = useNavigate();

  const [disconnectDialogOpen, setDisconnectDialogOpen] = useState(false);
  const [clearCacheDialogOpen, setClearCacheDialogOpen] = useState(false);
  const fallbackUsername = user?.username || localStorage.getItem('username') || 'unknown';
  const displayName = user?.name || fallbackUsername;
  const displayEmail = user?.email || 'Email not available';

  const handleDisconnect = () => {
    setDisconnectDialogOpen(false);
    logout();
    navigate('/');
    toast.success('GitHub account disconnected');
  };

  const handleClearCache = () => {
    setClearCacheDialogOpen(false);
    localStorage.removeItem('latest_documentation');
    toast.success('Local cache cleared successfully');
  };

  return (
    <div className="space-y-6 page-enter max-w-3xl">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-foreground">Settings</h1>
        <p className="text-sm text-muted-foreground mt-1">
          Manage your account and preferences
        </p>
      </div>

      {/* Profile Section */}
      <Card className="border-border bg-card">
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <User className="w-5 h-5" />
            Profile
          </CardTitle>
          <CardDescription>Your connected GitHub account</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Avatar className="w-16 h-16 ring-2 ring-border">
                <AvatarImage src={user?.avatar} />
                <AvatarFallback className="text-lg">{displayName.charAt(0)}</AvatarFallback>
              </Avatar>
              <div>
                <h3 className="font-semibold text-foreground">{displayName}</h3>
                <p className="text-sm text-muted-foreground">@{fallbackUsername}</p>
                <p className="text-sm text-muted-foreground">{displayEmail}</p>
              </div>
            </div>
            <div className="flex items-center gap-2 text-accent">
              <Github className="w-5 h-5" />
              <span className="text-sm font-medium">Connected</span>
            </div>
          </div>
          <Separator />
          <Button
            variant="outline"
            className="text-destructive hover:text-destructive hover:bg-destructive/10"
            onClick={() => setDisconnectDialogOpen(true)}
          >
            <LogOut className="w-4 h-4 mr-2" />
            Disconnect GitHub
          </Button>
        </CardContent>
      </Card>

      {/* Documentation Settings */}
      <Card className="border-border bg-card">
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <FileText className="w-5 h-5" />
            Documentation Settings
          </CardTitle>
          <CardDescription>Customize how documentation is generated</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h4 className="font-medium text-foreground">Default Output Format</h4>
              <p className="text-sm text-muted-foreground">Choose your preferred format</p>
            </div>
            <Select value={defaultFormat} onValueChange={(v) => setDefaultFormat(v as typeof defaultFormat)}>
              <SelectTrigger className="w-40">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="plainText">Plain Text</SelectItem>
                <SelectItem value="research">Research Style</SelectItem>
                <SelectItem value="latex">LaTeX</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <Separator />

          <div>
            <div className="flex items-center justify-between mb-3">
              <div>
                <h4 className="font-medium text-foreground">Text Complexity</h4>
                <p className="text-sm text-muted-foreground">Adjust the technical depth of generated docs</p>
              </div>
              <span className="text-sm font-medium text-primary">{textComplexity}%</span>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-xs text-muted-foreground">Simple</span>
              <Slider
                value={[textComplexity]}
                onValueChange={([v]) => setTextComplexity(v)}
                max={100}
                step={10}
                className="flex-1"
              />
              <span className="text-xs text-muted-foreground">Technical</span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Appearance & Notifications */}
      <Card className="border-border bg-card">
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <Bell className="w-5 h-5" />
            Appearance & Notifications
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              {isDarkMode ? <Moon className="w-5 h-5 text-primary" /> : <Sun className="w-5 h-5 text-primary" />}
              <div>
                <h4 className="font-medium text-foreground">Dark Mode</h4>
                <p className="text-sm text-muted-foreground">Toggle between light and dark themes</p>
              </div>
            </div>
            <Switch checked={isDarkMode} onCheckedChange={toggleDarkMode} />
          </div>

          <Separator />

          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Bell className="w-5 h-5 text-muted-foreground" />
              <div>
                <h4 className="font-medium text-foreground">Push Notifications</h4>
                <p className="text-sm text-muted-foreground">Get notified when docs are ready</p>
              </div>
            </div>
            <Switch checked={notificationsEnabled} onCheckedChange={setNotificationsEnabled} />
          </div>
        </CardContent>
      </Card>

      {/* Offline & Cache */}
      <Card className="border-border bg-card">
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <Database className="w-5 h-5" />
            Offline & Caching
          </CardTitle>
          <CardDescription>Control local data storage</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h4 className="font-medium text-foreground">Use Cached Outputs When Offline</h4>
              <p className="text-sm text-muted-foreground">Access previously generated docs without internet</p>
            </div>
            <Switch checked={cacheEnabled} onCheckedChange={setCacheEnabled} />
          </div>

          <Separator />

          <div className="flex items-center justify-between">
            <div>
              <h4 className="font-medium text-foreground">Clear Local Cache</h4>
              <p className="text-sm text-muted-foreground">Remove all locally stored documentation</p>
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setClearCacheDialogOpen(true)}
            >
              <Trash2 className="w-4 h-4 mr-2" />
              Clear Cache
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Security & Privacy */}
      <Card className="border-border bg-card">
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <Shield className="w-5 h-5" />
            Security & Privacy
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="space-y-3 text-sm">
            <li className="flex items-start gap-3">
              <Lock className="w-4 h-4 text-accent mt-0.5 shrink-0" />
              <span className="text-muted-foreground">OAuth-based login—no passwords stored on our servers</span>
            </li>
            <li className="flex items-start gap-3">
              <Eye className="w-4 h-4 text-accent mt-0.5 shrink-0" />
              <span className="text-muted-foreground">Data is processed only on user request</span>
            </li>
            <li className="flex items-start gap-3">
              <Database className="w-4 h-4 text-accent mt-0.5 shrink-0" />
              <span className="text-muted-foreground">Generated outputs are stored locally on your device</span>
            </li>
          </ul>
        </CardContent>
      </Card>

      {/* Disconnect Dialog */}
      <Dialog open={disconnectDialogOpen} onOpenChange={setDisconnectDialogOpen}>
        <DialogContent className="bg-card border-border">
          <DialogHeader>
            <DialogTitle>Disconnect GitHub?</DialogTitle>
            <DialogDescription>
              You will be signed out and will need to reconnect your GitHub account to continue using AutoDoc Writer.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="outline" onClick={() => setDisconnectDialogOpen(false)}>
              Cancel
            </Button>
            <Button variant="destructive" onClick={handleDisconnect}>
              Disconnect
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Clear Cache Dialog */}
      <Dialog open={clearCacheDialogOpen} onOpenChange={setClearCacheDialogOpen}>
        <DialogContent className="bg-card border-border">
          <DialogHeader>
            <DialogTitle>Clear Local Cache?</DialogTitle>
            <DialogDescription>
              This will remove all locally stored documentation. You'll need to regenerate them if needed offline.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="outline" onClick={() => setClearCacheDialogOpen(false)}>
              Cancel
            </Button>
            <Button onClick={handleClearCache}>
              Clear Cache
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
