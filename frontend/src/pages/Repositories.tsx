import { Button } from "../components/ui/Button";
import { Plus } from "lucide-react";

export default function RepositoriesPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Repositories</h1>
          <p className="mt-1 text-sm text-slate-400">Manage your documented projects.</p>
        </div>
        <div className="w-auto">
            {/* Reusing your high-end button, but overriding width */}
            <Button className="w-auto gap-2 px-4">
                <Plus className="h-4 w-4" />
                Add Repository
            </Button>
        </div>
      </div>

      {/* Empty State Placeholder */}
      <div className="rounded-2xl border border-dashed border-white/10 bg-white/5 p-12 text-center">
        <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-white/5">
            <Plus className="h-6 w-6 text-slate-500" />
        </div>
        <h3 className="text-lg font-medium text-white">No repositories found</h3>
        <p className="mt-2 text-sm text-slate-400">
          Connect a GitHub repository to start generating documentation.
        </p>
      </div>
    </div>
  );
}