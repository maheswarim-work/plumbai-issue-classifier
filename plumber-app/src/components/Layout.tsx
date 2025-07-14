'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Wrench, Plus, Search, Sparkles } from 'lucide-react';

interface LayoutProps {
  children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  const pathname = usePathname();

  const navigation = [
    { name: 'Dashboard', href: '/', current: pathname === '/' },
    { name: 'Jobs', href: '/jobs', current: pathname === '/jobs' },
    { name: 'Technicians', href: '/technicians', current: pathname === '/technicians' },
    { name: 'Reports', href: '/reports', current: pathname === '/reports' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50/30 to-indigo-50/30">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md shadow-lg border-b border-gray-200/50 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl shadow-lg">
                <Wrench className="h-8 w-8 text-white" />
              </div>
              <Link href="/" className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent hover:from-blue-700 hover:to-indigo-700 transition-all duration-200">
                Plumber Workflow
              </Link>
            </div>
            <div className="flex items-center space-x-4">
              <button className="btn-primary flex items-center space-x-2 group">
                <Plus className="h-4 w-4 group-hover:rotate-90 transition-transform duration-200" />
                <span>New Job</span>
              </button>
              <div className="relative">
                <Search className="h-5 w-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search jobs..."
                  className="search-field"
                />
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white/60 backdrop-blur-md border-b border-gray-200/50 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            {navigation.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className={`nav-link ${
                  item.current ? 'nav-link-active' : ''
                }`}
              >
                {item.current && (
                  <div className="absolute bottom-0 left-0 w-full h-0.5 bg-gradient-to-r from-blue-500 to-indigo-500 rounded-full"></div>
                )}
                {item.name}
              </Link>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>

      {/* Decorative Elements */}
      <div className="fixed top-20 left-10 w-32 h-32 bg-gradient-to-br from-blue-200/20 to-indigo-200/20 rounded-full blur-3xl pointer-events-none"></div>
      <div className="fixed bottom-20 right-10 w-40 h-40 bg-gradient-to-br from-purple-200/20 to-pink-200/20 rounded-full blur-3xl pointer-events-none"></div>
    </div>
  );
} 