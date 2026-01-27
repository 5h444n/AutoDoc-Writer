import { Star, GitFork, ExternalLink } from 'lucide-react';

interface RepoCardProps {
    name: string;
    description: string | null;
    html_url: string;
    stargazers_count?: number;
    isSelected: boolean;
    onClick: () => void;
}

export function RepoCard({ name, description, html_url, stargazers_count, isSelected, onClick }: RepoCardProps) {
    return (
        <div
            onClick={onClick}
            className={`
                h-full transition-all duration-200
                ${isSelected
                    ? 'opacity-100'
                    : 'opacity-80 hover:opacity-100'
                }
            `}
        >
            <div className="flex justify-between items-start mb-2">
                <h3 className="text-lg font-bold text-white truncate pr-4" title={name}>
                    {name}
                </h3>
                <a
                    href={html_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-gray-400 hover:text-white transition-colors"
                    onClick={(e) => e.stopPropagation()}
                >
                    <ExternalLink className="w-5 h-5" />
                </a>
            </div>

            <p className="text-gray-400 text-sm mb-4 line-clamp-2 h-10">
                {description || "No description provided."}
            </p>

            <div className="flex items-center gap-4 text-gray-500 text-sm">
                <div className="flex items-center gap-1">
                    <Star className="w-4 h-4 text-yellow-500 fill-yellow-500" />
                    <span>{stargazers_count ?? 0}</span>
                </div>
                <div className="flex items-center gap-1">
                    <GitFork className="w-4 h-4" />
                    <span>0</span>
                </div>
            </div>
        </div>
    );
}
