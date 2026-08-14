import { useState } from 'react';
import { User, Bell, Webhook, Shield, CheckCircle2, AlertCircle } from 'lucide-react';
import { cn } from './lib/utils';

export function Settings() {
  const [activeTab, setActiveTab] = useState('integrations');

  const tabs = [
    { id: 'profile', name: 'Profile', icon: User },
    { id: 'notifications', name: 'Notifications', icon: Bell },
    { id: 'integrations', name: 'Integrations', icon: Webhook },
    { id: 'security', name: 'Security', icon: Shield },
  ];

  return (
    <div className="p-8 max-w-7xl mx-auto animate-slide-up-fade">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Settings</h1>
        <p className="text-neutral-500 mt-2">Manage your account settings and connected services.</p>
      </div>

      <div className="flex flex-col md:flex-row gap-8">
        <aside className="w-full md:w-64 shrink-0">
          <nav className="flex flex-col space-y-1">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={cn(
                    "flex items-center gap-3 px-4 py-3 rounded-xl transition-all font-medium text-left",
                    isActive
                      ? "bg-primary/10 text-primary"
                      : "text-neutral-600 dark:text-neutral-400 hover:bg-neutral-100 dark:hover:bg-neutral-800/50 hover:text-neutral-900 dark:hover:text-neutral-100"
                  )}
                >
                  <Icon className="w-5 h-5" />
                  {tab.name}
                </button>
              );
            })}
          </nav>
        </aside>

        <div className="flex-1 max-w-3xl">
          {activeTab === 'integrations' && (
            <div className="space-y-6 animate-slide-up-fade">
              <div className="bg-white dark:bg-neutral-900 p-6 rounded-2xl shadow-sm border border-neutral-200 dark:border-neutral-800">
                <h2 className="text-xl font-bold mb-1">AI Copilot Integrations</h2>
                <p className="text-neutral-500 text-sm mb-6">Connect your workspace tools so the AI can automatically investigate logs, create tasks, and alert the team.</p>
                
                <div className="space-y-4">
                  {/* Slack */}
                  <div className="flex items-center justify-between p-4 bg-neutral-50 dark:bg-neutral-950 rounded-xl border border-neutral-200 dark:border-neutral-800">
                    <div className="flex items-center gap-4">
                      <div className="w-12 h-12 bg-[#4A154B] rounded-xl flex items-center justify-center shadow-inner">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/d/d5/Slack_icon_2019.svg" alt="Slack" className="w-6 h-6 brightness-0 invert" />
                      </div>
                      <div>
                        <h3 className="font-semibold text-neutral-900 dark:text-neutral-100">Slack</h3>
                        <p className="text-sm text-neutral-500">Send alerts and AI summaries to #it-alerts</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2 text-emerald-600 bg-emerald-50 dark:bg-emerald-900/20 px-3 py-1.5 rounded-lg border border-emerald-200 dark:border-emerald-800">
                      <CheckCircle2 className="w-4 h-4" />
                      <span className="text-sm font-medium">Connected</span>
                    </div>
                  </div>

                  {/* GitHub */}
                  <div className="flex items-center justify-between p-4 bg-neutral-50 dark:bg-neutral-950 rounded-xl border border-neutral-200 dark:border-neutral-800">
                    <div className="flex items-center gap-4">
                      <div className="w-12 h-12 bg-[#24292e] rounded-xl flex items-center justify-center shadow-inner">
                        <svg viewBox="0 0 24 24" className="w-7 h-7 fill-white"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
                      </div>
                      <div>
                        <h3 className="font-semibold text-neutral-900 dark:text-neutral-100">GitHub</h3>
                        <p className="text-sm text-neutral-500">Read logs and create issues in repositories</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2 text-emerald-600 bg-emerald-50 dark:bg-emerald-900/20 px-3 py-1.5 rounded-lg border border-emerald-200 dark:border-emerald-800">
                      <CheckCircle2 className="w-4 h-4" />
                      <span className="text-sm font-medium">Connected</span>
                    </div>
                  </div>

                  {/* Asana */}
                  <div className="flex items-center justify-between p-4 bg-neutral-50 dark:bg-neutral-950 rounded-xl border border-neutral-200 dark:border-neutral-800">
                    <div className="flex items-center gap-4">
                      <div className="w-12 h-12 bg-[#F06A6A] rounded-xl flex items-center justify-center shadow-inner">
                         <span className="text-white font-bold text-xl leading-none -mt-1">●</span>
                         <span className="text-white font-bold text-xl leading-none -mt-1 -ml-1">●</span>
                         <span className="text-white font-bold text-xl leading-none -mt-1 -ml-1">●</span>
                      </div>
                      <div>
                        <h3 className="font-semibold text-neutral-900 dark:text-neutral-100">Asana</h3>
                        <p className="text-sm text-neutral-500">Create tracking tasks and follow up items</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2 text-emerald-600 bg-emerald-50 dark:bg-emerald-900/20 px-3 py-1.5 rounded-lg border border-emerald-200 dark:border-emerald-800">
                      <CheckCircle2 className="w-4 h-4" />
                      <span className="text-sm font-medium">Connected</span>
                    </div>
                  </div>

                  {/* PagerDuty (Not connected) */}
                  <div className="flex items-center justify-between p-4 bg-neutral-50/50 dark:bg-neutral-950/50 rounded-xl border border-neutral-200 border-dashed dark:border-neutral-800">
                    <div className="flex items-center gap-4 opacity-60 grayscale">
                      <div className="w-12 h-12 bg-[#06AC38] rounded-xl flex items-center justify-center shadow-inner">
                        <span className="text-white font-bold text-2xl font-serif">P</span>
                      </div>
                      <div>
                        <h3 className="font-semibold text-neutral-900 dark:text-neutral-100">PagerDuty</h3>
                        <p className="text-sm text-neutral-500">Auto-page on-call engineers for P1 incidents</p>
                      </div>
                    </div>
                    <button className="px-4 py-2 bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-700 text-sm font-medium rounded-lg hover:bg-neutral-50 transition-colors">
                      Connect
                    </button>
                  </div>
                  
                </div>
              </div>
            </div>
          )}

          {activeTab === 'profile' && (
            <div className="space-y-6 animate-slide-up-fade">
              <div className="bg-white dark:bg-neutral-900 p-6 rounded-2xl shadow-sm border border-neutral-200 dark:border-neutral-800">
                <h2 className="text-xl font-bold mb-1">Profile Settings</h2>
                <p className="text-neutral-500 text-sm mb-6">Manage your personal information and preferences.</p>
                
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-semibold mb-2 text-neutral-900 dark:text-neutral-100">Full Name</label>
                    <input type="text" defaultValue="Admin User" className="w-full px-4 py-2.5 bg-neutral-50 dark:bg-neutral-950 border border-neutral-200 dark:border-neutral-800 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all text-sm" />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold mb-2 text-neutral-900 dark:text-neutral-100">Email Address</label>
                    <input type="email" defaultValue="admin@digiplusit.com" className="w-full px-4 py-2.5 bg-neutral-50 dark:bg-neutral-950 border border-neutral-200 dark:border-neutral-800 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all text-sm" />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold mb-2 text-neutral-900 dark:text-neutral-100">Role</label>
                    <input type="text" disabled defaultValue="System Administrator" className="w-full px-4 py-2.5 bg-neutral-100 dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-xl text-neutral-500 cursor-not-allowed text-sm" />
                  </div>
                  <div className="pt-2">
                    <button className="px-5 py-2.5 bg-primary text-white text-sm font-medium rounded-xl hover:bg-primary/90 transition-colors shadow-sm">
                      Save Changes
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'notifications' && (
            <div className="space-y-6 animate-slide-up-fade">
              <div className="bg-white dark:bg-neutral-900 p-6 rounded-2xl shadow-sm border border-neutral-200 dark:border-neutral-800">
                <h2 className="text-xl font-bold mb-1">Notification Preferences</h2>
                <p className="text-neutral-500 text-sm mb-6">Choose how you want to be alerted about incidents and updates.</p>
                
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 bg-neutral-50 dark:bg-neutral-950 rounded-xl border border-neutral-200 dark:border-neutral-800">
                    <div>
                      <h3 className="font-semibold text-neutral-900 dark:text-neutral-100 text-sm">Email Alerts</h3>
                      <p className="text-xs text-neutral-500 mt-0.5">Receive an email when a P1 or P2 incident is created.</p>
                    </div>
                    <div className="relative inline-flex h-6 w-11 items-center rounded-full bg-primary">
                      <span className="inline-block h-4 w-4 translate-x-6 rounded-full bg-white transition" />
                    </div>
                  </div>
                  <div className="flex items-center justify-between p-4 bg-neutral-50 dark:bg-neutral-950 rounded-xl border border-neutral-200 dark:border-neutral-800">
                    <div>
                      <h3 className="font-semibold text-neutral-900 dark:text-neutral-100 text-sm">Slack Notifications</h3>
                      <p className="text-xs text-neutral-500 mt-0.5">Get notified in connected Slack channels for all incidents.</p>
                    </div>
                    <div className="relative inline-flex h-6 w-11 items-center rounded-full bg-primary">
                      <span className="inline-block h-4 w-4 translate-x-6 rounded-full bg-white transition" />
                    </div>
                  </div>
                  <div className="flex items-center justify-between p-4 bg-neutral-50 dark:bg-neutral-950 rounded-xl border border-neutral-200 dark:border-neutral-800 opacity-60">
                    <div>
                      <h3 className="font-semibold text-neutral-900 dark:text-neutral-100 text-sm">SMS Alerts (Coming Soon)</h3>
                      <p className="text-xs text-neutral-500 mt-0.5">Receive text messages for critical (P1) outages.</p>
                    </div>
                    <div className="relative inline-flex h-6 w-11 items-center rounded-full bg-neutral-300 dark:bg-neutral-700">
                      <span className="inline-block h-4 w-4 translate-x-1 rounded-full bg-white transition" />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'security' && (
            <div className="space-y-6 animate-slide-up-fade">
              <div className="bg-white dark:bg-neutral-900 p-6 rounded-2xl shadow-sm border border-neutral-200 dark:border-neutral-800">
                <h2 className="text-xl font-bold mb-1">Security & Access</h2>
                <p className="text-neutral-500 text-sm mb-6">Manage your password, 2FA, and active sessions.</p>
                
                <div className="space-y-6">
                  <div>
                    <h3 className="text-sm font-semibold text-neutral-900 dark:text-neutral-100 mb-3">Two-Factor Authentication</h3>
                    <div className="flex items-center justify-between p-4 bg-neutral-50 dark:bg-neutral-950 rounded-xl border border-neutral-200 dark:border-neutral-800">
                      <div>
                        <p className="text-sm text-neutral-900 dark:text-neutral-100 font-medium">Authenticator App</p>
                        <p className="text-xs text-neutral-500 mt-0.5">Use an app like Google Authenticator or Authy.</p>
                      </div>
                      <button className="px-4 py-2 bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-700 text-sm font-medium rounded-lg hover:bg-neutral-50 transition-colors">
                        Enable 2FA
                      </button>
                    </div>
                  </div>

                  <div>
                    <h3 className="text-sm font-semibold text-neutral-900 dark:text-neutral-100 mb-3">Password Management</h3>
                    <button className="px-4 py-2 bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-700 text-sm font-medium rounded-lg hover:bg-neutral-50 transition-colors">
                      Change Password
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
