import { Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, ListTodo, Settings, HelpCircle, BrainCircuit } from 'lucide-react';
import { cn } from './lib/utils';

export function Layout({ children }: { children: React.ReactNode }) {
  const location = useLocation();
  
  const navItems = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard },
    { name: 'Incidents', path: '/incidents', icon: ListTodo },
    { name: 'Settings', path: '/settings', icon: Settings },
  ];

  return (
    <div className="flex h-screen bg-neutral-50 dark:bg-neutral-950 overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 glass-panel border-r border-neutral-200/50 dark:border-neutral-800/50 flex flex-col z-20">
        <div className="p-6 flex items-center gap-2 text-primary">
          <BrainCircuit className="w-8 h-8" />
          <h1 className="text-2xl font-bold tracking-tight">ResolveAI</h1>
        </div>
        
        <nav className="flex-1 px-4 py-4 space-y-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path || (item.path !== '/' && location.pathname.startsWith(item.path));
            return (
              <Link
                key={item.name}
                to={item.path}
                className={cn(
                  "flex items-center gap-3 px-4 py-3 rounded-xl transition-all font-medium",
                  isActive 
                    ? "bg-primary text-white shadow-md shadow-primary/20" 
                    : "text-neutral-600 dark:text-neutral-400 hover:bg-neutral-100 dark:hover:bg-neutral-800/50 hover:text-neutral-900 dark:hover:text-neutral-100"
                )}
              >
                <Icon className="w-5 h-5" />
                {item.name}
              </Link>
            );
          })}
        </nav>
        
        <div className="p-4 border-t border-neutral-200/50 dark:border-neutral-800/50">
          <button className="flex items-center gap-3 px-4 py-3 w-full rounded-xl text-neutral-600 dark:text-neutral-400 hover:bg-neutral-100 dark:hover:bg-neutral-800/50 transition-all font-medium">
            <HelpCircle className="w-5 h-5" />
            Help & Support
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 overflow-y-auto relative scroll-smooth">
        <div className="absolute top-4 right-6 z-30">
           <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-primary to-blue-400 text-white flex items-center justify-center font-semibold shadow-md border-2 border-white dark:border-neutral-900 cursor-pointer hover:scale-105 transition-transform">
             AD
           </div>
        </div>
        {children}
      </main>
    </div>
  );
}
