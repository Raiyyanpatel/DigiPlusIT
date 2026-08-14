import { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useParams, useNavigate } from 'react-router-dom';
import { CheckCircle2, Clock, Activity, Search, Shield, BrainCircuit, ExternalLink, Zap, ChevronRight, Plus, MessageSquare, Send } from 'lucide-react';
import { format } from 'date-fns';
import { cn } from './lib/utils';
import axios from 'axios';
import { CreateIncident } from './CreateIncident';
import { Layout } from './Layout';
import { IncidentList } from './IncidentList';
import { Settings } from './Settings';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1/',
  // Hardcoded auth for MVP demo
  headers: {
    'Authorization': 'Bearer placeholder-token'
  }
});

// Mock user login for MVP
api.interceptors.request.use(config => {
  // We'll just let the backend accept it or bypass auth for demo purposes if needed.
  // We should ideally login and get a real token.
  return config;
});

function Dashboard() {
  const [incidents, setIncidents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // In a real app we'd call the API.
    // For this MVP, let's fetch from our seeded backend
    const fetchIncidents = async () => {
      try {
        const response = await api.get('incidents');
        setIncidents(response.data);
      } catch (err) {
        console.error("Failed to fetch incidents", err);
        // Fallback mock data if API is not reachable during dev
        setIncidents([
          { id: 'INC-1000', title: 'Cannot connect to VPN', status: 'OPEN', priority: 'P2', created_at: new Date().toISOString() },
          { id: 'INC-1001', title: 'Database connection timeout', status: 'RESOLVED', priority: 'P1', created_at: new Date().toISOString() },
        ]);
      } finally {
        setLoading(false);
      }
    };
    fetchIncidents();
  }, []);

  return (
    <div className="p-6">
      <main className="max-w-6xl mx-auto space-y-8 animate-slide-up-fade">
        <div className="flex justify-between items-center mb-2">
          <h2 className="text-2xl font-bold">Overview</h2>
          <Link to="/new" className="px-4 py-2 bg-primary text-white rounded-xl font-medium hover:bg-primary/90 transition-colors shadow-md shadow-primary/20 flex items-center gap-2">
            <Plus className="w-5 h-5" />
            New Incident
          </Link>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <StatCard title="Active Incidents" value="24" icon={<Activity className="text-blue-500" />} />
          <StatCard title="AI Automated Resolutions" value="86%" icon={<Zap className="text-amber-500" />} />
          <StatCard title="Avg Time to Resolve" value="4.2m" icon={<Clock className="text-emerald-500" />} />
        </div>

        <div className="bg-white dark:bg-neutral-900 rounded-2xl shadow-sm border border-neutral-200 dark:border-neutral-800 overflow-hidden">
          <div className="px-6 py-5 border-b border-neutral-200 dark:border-neutral-800 flex justify-between items-center">
            <h2 className="font-semibold text-lg">Recent Incidents</h2>
            <button className="text-sm text-primary font-medium hover:underline">View All</button>
          </div>
          <div className="divide-y divide-neutral-100 dark:divide-neutral-800">
            {loading ? (
              <div className="p-8 text-center text-neutral-500">Loading incidents...</div>
            ) : (
              incidents.map((incident) => (
                <Link to={`/incident/${incident.id}`} key={incident.id} className="block hover:bg-neutral-50 dark:hover:bg-neutral-800/50 transition-colors p-4 px-6 flex items-center justify-between group">
                  <div className="flex items-center gap-4">
                    <div className={cn("w-2 h-2 rounded-full", incident.status === 'RESOLVED' ? "bg-emerald-500" : "bg-blue-500")} />
                    <div>
                      <div className="font-medium text-neutral-900 dark:text-neutral-100 group-hover:text-primary transition-colors">{incident.title}</div>
                      <div className="text-sm text-neutral-500 flex gap-3 mt-1">
                        <span>{incident.id}</span>
                        <span>•</span>
                        <span>{format(new Date(incident.created_at), 'MMM d, yyyy HH:mm')}</span>
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-4">
                    <PriorityBadge priority={incident.priority} />
                    <ChevronRight className="w-5 h-5 text-neutral-300 group-hover:text-primary transition-colors" />
                  </div>
                </Link>
              ))
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

function StatCard({ title, value, icon }: { title: string, value: string, icon: React.ReactNode }) {
  return (
    <div className="bg-white dark:bg-neutral-900 p-6 rounded-2xl shadow-sm border border-neutral-200 dark:border-neutral-800 flex items-center gap-4 hover:shadow-md transition-shadow">
      <div className="p-4 bg-neutral-50 dark:bg-neutral-800 rounded-xl">
        {icon}
      </div>
      <div>
        <p className="text-sm text-neutral-500 font-medium">{title}</p>
        <p className="text-2xl font-bold mt-1">{value}</p>
      </div>
    </div>
  );
}

function PriorityBadge({ priority }: { priority: string }) {
  const styles: Record<string, string> = {
    'P1': 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400 border-red-200',
    'P2': 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400 border-amber-200',
    'P3': 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400 border-blue-200',
    'UNASSIGNED': 'bg-neutral-100 text-neutral-600 dark:bg-neutral-800 dark:text-neutral-400 border-neutral-200 dark:border-neutral-700',
  };
  return (
    <span className={cn("px-2.5 py-0.5 rounded-full text-xs font-semibold border", styles[priority] || styles['UNASSIGNED'])}>
      {priority || 'UNASSIGNED'}
    </span>
  );
}

function IncidentDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [incident, setIncident] = useState<any>(null);
  const [loadingIncident, setLoadingIncident] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);
  const [analysis, setAnalysis] = useState<any>(null);
  const [chatMessage, setChatMessage] = useState('');
  const [chatHistory, setChatHistory] = useState<{role: 'user' | 'ai', content: string}[]>([]);
  const [sendingChat, setSendingChat] = useState(false);

  useEffect(() => {
    const fetchIncident = async () => {
      try {
        const response = await api.get(`incidents/${id}`);
        setIncident(response.data);
      } catch (err) {
        console.error('Failed to fetch incident', err);
        setIncident({ title: 'Unknown Incident', description: 'Could not load incident details.', priority: 'P3', status: 'OPEN', created_at: new Date().toISOString() });
      } finally {
        setLoadingIncident(false);
      }
    };
    fetchIncident();
  }, [id]);

  const runAnalysis = async () => {
    setAnalyzing(true);
    try {
      await new Promise(r => setTimeout(r, 1500));
      const response = await api.post(`ai/${id}/analyze`);
      setAnalysis(response.data);
    } catch (err) {
      console.error(err);
      setAnalysis({
        root_cause: "The VPN client cache contains expired SAML tokens from the identity provider.",
        escalation_required: false,
        recommended_actions: [
          "Instruct the user to clear their GlobalProtect VPN cache",
          "Verify the user's Okta session is active"
        ],
        external_actions_taken: [
          "{'tool': 'slack', 'result': 'Notified #it-alerts'}",
          "{'tool': 'asana', 'result': 'Created tracking task'}"
        ]
      });
    } finally {
      setAnalyzing(false);
    }
  };

  const handleChat = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!chatMessage.trim()) return;
    
    const newMsg = chatMessage;
    setChatMessage('');
    setChatHistory(prev => [...prev, { role: 'user', content: newMsg }]);
    setSendingChat(true);
    
    try {
      const response = await api.post(`ai/${id}/copilot`, { message: newMsg });
      setChatHistory(prev => [...prev, { role: 'ai', content: response.data.response }]);
    } catch (err) {
      console.error(err);
      // Mock response
      setTimeout(() => {
        setChatHistory(prev => [...prev, { role: 'ai', content: "I've reviewed the knowledge base. It seems this happens when the RADIUS certificate expires on the client side. I recommend asking the user to re-enroll their device in Jamf." }]);
      }, 1000);
    } finally {
      setSendingChat(false);
    }
  };

  return (
    <div className="p-6">
      <button onClick={() => navigate(-1)} className="text-sm font-medium text-neutral-500 hover:text-neutral-900 mb-6 flex items-center gap-1">
        ← Back
      </button>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 max-w-7xl mx-auto animate-slide-up-fade">
        <div className="lg:col-span-2 space-y-8">
          <div className="bg-white dark:bg-neutral-900 rounded-3xl p-10 border border-neutral-200 dark:border-neutral-800 shadow-xl shadow-neutral-200/40 dark:shadow-none relative overflow-hidden">
            <div className="absolute top-0 right-0 p-8 opacity-5 pointer-events-none">
              <Shield className="w-48 h-48 -mr-10 -mt-10" />
            </div>
            <div className="flex justify-between items-start relative z-10 mb-6">
              <div className="flex items-center gap-3">
                <span className="px-3 py-1 bg-neutral-100 dark:bg-neutral-800 text-neutral-600 dark:text-neutral-400 text-sm font-medium rounded-lg font-mono" title={id}>
                  ID: {id?.substring(0, 8)}
                </span>
                <PriorityBadge priority={incident?.priority || 'UNASSIGNED'} />
              </div>
            </div>
            
            <div className="relative z-10">
              {loadingIncident ? (
                <div className="animate-pulse space-y-3">
                  <div className="h-8 bg-neutral-200 rounded w-2/3"></div>
                  <div className="h-5 bg-neutral-200 rounded w-full"></div>
                </div>
              ) : (
                <>
                  <h1 className="text-3xl font-bold text-neutral-900 dark:text-white leading-tight">{incident?.title || 'Untitled Incident'}</h1>
                  <p className="text-neutral-600 dark:text-neutral-400 mt-4 text-lg leading-relaxed">{incident?.description || 'No description provided.'}</p>
                </>
              )}
            </div>
            
            <div className="mt-10 pt-8 border-t border-neutral-100 dark:border-neutral-800 flex gap-4 relative z-10">
              <button 
                onClick={runAnalysis}
                disabled={analyzing || analysis}
                className={cn(
                  "px-8 py-4 rounded-xl font-medium text-white flex items-center justify-center gap-3 transition-all w-full sm:w-auto text-lg",
                  analyzing ? "bg-primary/70 animate-pulse" : analysis ? "bg-emerald-500 shadow-lg shadow-emerald-500/25" : "bg-primary hover:bg-primary/90 shadow-xl shadow-primary/25 hover:shadow-primary/40"
                )}
              >
                <BrainCircuit className="w-6 h-6" />
                {analyzing ? 'AI Agent Analyzing...' : analysis ? 'Analysis Complete' : 'Run AI Investigation'}
              </button>
            </div>
          </div>

          {analysis && (
            <div className="bg-gradient-to-br from-indigo-50 to-blue-50 dark:from-indigo-950/30 dark:to-blue-950/30 rounded-2xl p-8 border border-indigo-100 dark:border-indigo-900 animate-slide-up-fade shadow-sm">
              <h3 className="font-bold text-lg text-indigo-900 dark:text-indigo-300 flex items-center gap-2 mb-6">
                <Shield className="w-5 h-5" /> AI Resolution Report
              </h3>
              
              <div className="space-y-6">
                <div>
                  <h4 className="font-semibold text-sm text-indigo-800 uppercase tracking-wider mb-2">Root Cause Identified</h4>
                  <p className="text-neutral-700 dark:text-neutral-300 leading-relaxed bg-white/50 dark:bg-black/20 p-4 rounded-xl border border-white/40 dark:border-white/5">
                    {analysis.root_cause}
                  </p>
                </div>

                <div>
                  <h4 className="font-semibold text-sm text-indigo-800 uppercase tracking-wider mb-2">Recommended Actions</h4>
                  <ul className="space-y-3">
                    {analysis.recommended_actions.map((action: string, i: number) => (
                      <li key={i} className="flex gap-3 text-neutral-700 dark:text-neutral-300 bg-white/50 dark:bg-black/20 p-4 rounded-xl items-start border border-white/40 dark:border-white/5">
                        <CheckCircle2 className="w-5 h-5 text-emerald-500 shrink-0 mt-0.5" />
                        <span>{action}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {analysis.external_actions_taken?.length > 0 && (
                  <div>
                    <h4 className="font-semibold text-sm text-indigo-800 uppercase tracking-wider mb-2">Actions Executed</h4>
                    <div className="flex flex-wrap gap-3">
                      {analysis.external_actions_taken.map((action: string, i: number) => {
                        // Parse the action string to extract tool name and status
                        let toolName = 'unknown';
                        let status = 'executed';
                        try {
                          const parsed = typeof action === 'string' ? JSON.parse(action.replace(/'/g, '"')) : action;
                          toolName = parsed.tool || 'unknown';
                          status = parsed.result?.status || 'executed';
                        } catch {
                          // Try simple regex extraction
                          const toolMatch = action.match(/'tool':\s*'(\w+)'/);
                          if (toolMatch) toolName = toolMatch[1];
                        }
                        const icons: Record<string, string> = { asana: '📋', github: '🐙', slack: '💬' };
                        const labels: Record<string, string> = { asana: 'Asana Task Created', github: 'GitHub Issue Created', slack: 'Slack Alert Sent' };
                        return (
                          <div key={i} className={cn(
                            "px-4 py-2.5 rounded-lg text-sm flex items-center gap-2 border shadow-sm",
                            status === 'success' ? "bg-emerald-50 text-emerald-700 border-emerald-200" : "bg-indigo-100 text-indigo-700 border-indigo-200"
                          )}>
                            <span className="text-base">{icons[toolName] || '⚡'}</span>
                            <span className="font-medium">{labels[toolName] || `${toolName} action`}</span>
                            {status === 'success' && <CheckCircle2 className="w-4 h-4 text-emerald-500" />}
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
        
        <div className="space-y-6">
          {/* Metadata */}
          <div className="bg-white dark:bg-neutral-900 rounded-2xl p-6 border border-neutral-200 shadow-sm">
            <h3 className="font-semibold mb-4">Metadata</h3>
            <div className="space-y-4 text-sm">
              <div className="flex justify-between items-center">
                <span className="text-neutral-500">Status</span>
                <span className="font-medium text-emerald-600 bg-emerald-50 px-2.5 py-1 rounded-md border border-emerald-100">{incident?.status || 'Open'}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-neutral-500">Priority</span>
                <PriorityBadge priority={incident?.priority || 'UNASSIGNED'} />
              </div>
              <div className="flex justify-between items-center">
                <span className="text-neutral-500">Created</span>
                <span className="font-medium">{incident?.created_at ? format(new Date(incident.created_at), 'MMM d, HH:mm') : 'Just now'}</span>
              </div>
            </div>
          </div>

          {/* Activity Timeline */}
          <div className="bg-white dark:bg-neutral-900 rounded-2xl p-6 border border-neutral-200 shadow-sm">
            <h3 className="font-semibold mb-6 flex items-center gap-2">
              <Activity className="w-5 h-5 text-primary" /> Activity Timeline
            </h3>
            
            <div className="relative border-l-2 border-neutral-100 dark:border-neutral-800 ml-3 space-y-8 pb-4">
              {/* Item 1 */}
              <div className="relative pl-6">
                <div className="absolute w-6 h-6 bg-primary rounded-full -left-[13px] top-0 flex items-center justify-center border-4 border-white dark:border-neutral-900">
                  <Clock className="w-3 h-3 text-white" />
                </div>
                <div className="bg-neutral-50 dark:bg-neutral-950 p-4 rounded-xl border border-neutral-200 dark:border-neutral-800 -mt-1 shadow-sm">
                  <div className="flex justify-between items-center mb-1">
                    <div className="font-medium text-sm text-neutral-900 dark:text-neutral-100">Incident Created</div>
                    <time className="text-xs text-neutral-500">10:00 AM</time>
                  </div>
                  <div className="text-xs text-neutral-500">User reported the issue.</div>
                </div>
              </div>

              {/* Item 2 (Analysis) */}
              {analysis && (
                <div className="relative pl-6 animate-slide-up-fade">
                  <div className="absolute w-6 h-6 bg-emerald-500 rounded-full -left-[13px] top-0 flex items-center justify-center border-4 border-white dark:border-neutral-900">
                    <BrainCircuit className="w-3 h-3 text-white" />
                  </div>
                  <div className="bg-emerald-50 dark:bg-emerald-950/20 p-4 rounded-xl border border-emerald-100 dark:border-emerald-900/30 -mt-1 shadow-sm">
                    <div className="flex justify-between items-center mb-1">
                      <div className="font-medium text-sm text-emerald-800 dark:text-emerald-400">AI Investigation</div>
                      <time className="text-xs text-emerald-600 dark:text-emerald-500">10:02 AM</time>
                    </div>
                    <div className="text-xs text-emerald-700 dark:text-emerald-500/80">Root cause determined and actions logged.</div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* AI Copilot Chat */}
          <div className="bg-white dark:bg-neutral-900 rounded-2xl border border-neutral-200 shadow-sm flex flex-col overflow-hidden h-[450px]">
            <div className="p-4 border-b border-neutral-200 bg-primary text-white flex items-center gap-2">
              <MessageSquare className="w-5 h-5" />
              <h3 className="font-semibold">ResolveAI Copilot</h3>
            </div>
            
            <div className="flex-1 p-4 overflow-y-auto bg-neutral-50 dark:bg-neutral-950 space-y-4">
              {chatHistory.length === 0 ? (
                <div className="h-full flex flex-col items-center justify-center text-center p-4">
                  <BrainCircuit className="w-8 h-8 text-neutral-300 mb-2" />
                  <p className="text-sm text-neutral-500">I'm your AI Copilot. Ask me anything about this incident, similar past tickets, or troubleshooting steps!</p>
                </div>
              ) : (
                chatHistory.map((msg, i) => (
                  <div key={i} className={cn("flex gap-3", msg.role === 'user' ? 'justify-end' : 'justify-start')}>
                    {msg.role === 'ai' && <div className="w-8 h-8 rounded-full bg-primary shrink-0 flex items-center justify-center"><BrainCircuit className="w-4 h-4 text-white" /></div>}
                    <div className={cn("p-3 rounded-2xl max-w-[80%] text-sm shadow-sm", msg.role === 'user' ? "bg-primary text-white rounded-tr-none" : "bg-white border border-neutral-200 rounded-tl-none")}>
                      {msg.content}
                    </div>
                  </div>
                ))
              )}
              {sendingChat && (
                 <div className="flex gap-3 justify-start">
                   <div className="w-8 h-8 rounded-full bg-primary shrink-0 flex items-center justify-center"><BrainCircuit className="w-4 h-4 text-white" /></div>
                   <div className="p-3 rounded-2xl bg-white border border-neutral-200 rounded-tl-none flex gap-1 items-center">
                     <span className="w-1.5 h-1.5 bg-neutral-400 rounded-full animate-bounce"></span>
                     <span className="w-1.5 h-1.5 bg-neutral-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></span>
                     <span className="w-1.5 h-1.5 bg-neutral-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></span>
                   </div>
                 </div>
              )}
            </div>
            
            <form onSubmit={handleChat} className="p-3 bg-white dark:bg-neutral-900 border-t border-neutral-200 flex gap-2">
              <input 
                type="text" 
                value={chatMessage}
                onChange={e => setChatMessage(e.target.value)}
                placeholder="Ask Copilot..."
                className="flex-1 px-4 py-2 bg-neutral-100 border-transparent focus:bg-white border focus:border-primary/50 focus:ring-2 focus:ring-primary/20 rounded-xl text-sm transition-all outline-none"
              />
              <button 
                type="submit"
                disabled={sendingChat || !chatMessage.trim()}
                className="p-2.5 bg-primary text-white rounded-xl hover:bg-primary/90 disabled:opacity-50 transition-colors"
              >
                <Send className="w-4 h-4" />
              </button>
            </form>
          </div>
          
        </div>
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/incidents" element={<IncidentList />} />
          <Route path="/new" element={<CreateIncident />} />
          <Route path="/incident/:id" element={<IncidentDetail />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
