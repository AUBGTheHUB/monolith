import * as React from 'react';
import { X, ChevronDown, Check } from 'lucide-react';
import { cn } from '@/lib/utils';

interface MultiSelectProps {
    options: string[];
    selected: string[];
    onChange: (selected: string[]) => void;
    placeholder?: string;
    className?: string;
}

export function MultiSelect({
    options,
    selected,
    onChange,
    placeholder = 'Select options...',
    className,
}: MultiSelectProps) {
    const [open, setOpen] = React.useState(false);
    const [searchQuery, setSearchQuery] = React.useState('');
    const dropdownRef = React.useRef<HTMLDivElement>(null);

    // Close dropdown when clicking outside
    React.useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
                setOpen(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    const filteredOptions = options.filter((option) => option.toLowerCase().includes(searchQuery.toLowerCase()));

    const handleToggle = (option: string) => {
        if (selected.includes(option)) {
            onChange(selected.filter((item) => item !== option));
        } else {
            onChange([...selected, option]);
        }
    };

    const handleRemove = (option: string, e: React.MouseEvent) => {
        e.stopPropagation();
        onChange(selected.filter((item) => item !== option));
    };

    const handleSelectAll = () => {
        if (selected.length === options.length) {
            onChange([]);
        } else {
            onChange([...options]);
        }
    };

    return (
        <div className="relative w-full" ref={dropdownRef}>
            {/* Trigger Button */}
            <button
                type="button"
                onClick={() => setOpen(!open)}
                className={cn(
                    'flex w-full min-h-10 items-center justify-between rounded-md border border-input bg-white px-3 py-2 text-sm text-black ring-offset-background focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
                    className,
                )}
            >
                <div className="flex flex-wrap gap-1 flex-1">
                    {selected.length === 0 ? (
                        <span className="text-gray-400">{placeholder}</span>
                    ) : (
                        selected.map((item) => (
                            <span
                                key={item}
                                className="inline-flex items-center gap-1 rounded-full bg-blue-50 px-2 py-1 text-xs font-medium text-blue-700 border border-blue-200"
                            >
                                {item}
                                <X
                                    className="h-3 w-3 cursor-pointer hover:text-blue-900"
                                    onClick={(e) => handleRemove(item, e)}
                                />
                            </span>
                        ))
                    )}
                </div>
                <ChevronDown
                    className={cn('h-4 w-4 shrink-0 opacity-50 transition-transform text-black', open && 'rotate-180')}
                />
            </button>

            {/* Dropdown Content */}
            {open && (
                <div className="absolute z-50 mt-2 w-full rounded-md border border-gray-200 bg-white text-black shadow-xl">
                    <div className="p-3">
                        {/* Search Input */}
                        <input
                            type="text"
                            placeholder="Search options..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            className="flex h-9 w-full rounded-md border border-input bg-white px-3 py-1 text-sm text-black shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring mb-2"
                        />

                        {/* Select All */}
                        <label className="flex items-center space-x-2 rounded-sm p-2 hover:bg-gray-100 cursor-pointer">
                            <input
                                type="checkbox"
                                checked={selected.length === options.length && options.length > 0}
                                onChange={handleSelectAll}
                                className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                            />
                            <span className="text-sm font-medium !text-black">(Select All)</span>
                        </label>

                        {/* Options List */}
                        <div className="max-h-64 overflow-y-auto">
                            {filteredOptions.length === 0 ? (
                                <div className="py-6 text-center text-sm text-gray-500">No options found.</div>
                            ) : (
                                filteredOptions.map((option) => {
                                    const isSelected = selected.includes(option);
                                    return (
                                        <label
                                            key={option}
                                            className="flex items-center space-x-2 rounded-sm p-2 hover:bg-gray-100 cursor-pointer"
                                        >
                                            <input
                                                type="checkbox"
                                                checked={isSelected}
                                                onChange={() => handleToggle(option)}
                                                className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                                            />
                                            <span className="text-sm flex-1 !text-black">{option}</span>
                                            {isSelected && <Check className="h-4 w-4 text-blue-600" />}
                                        </label>
                                    );
                                })
                            )}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
