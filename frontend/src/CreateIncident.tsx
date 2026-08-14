import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ShieldAlert, Send } from 'lucide-react';
import axios from 'axios';
import { cn } from './lib/utils';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Authorization': 'Bearer placeholder-token'
  }
});

export function CreateIncident() {
  const navigate = useNavigate();
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError('');
    
    try {
      const res = await api.post('/incidents/', {
        title,
        description,
        priority: 'UNASSIGNED',
        category: 'General'
      });
      // Redirect to the new incident detail page
      navigate(`/incident/${res.data.id}`);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create incident');
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-neutral-50 dark:bg-neutral-950 p-6 flex items-center justify-center">
      <div className="w-full max-w-xl animate-slide-up-fade">
        <button onClick={() => navigate(-1)} className="text-sm font-medium text-neutral-500 hover:text-neutral-900 mb-6 flex items-center gap-1">
          ← Back to Dashboard
        </button>

        <div className="bg-white dark:bg-neutral-900 rounded-2xl p-8 border border-neutral-200 shadow-xl">
          <div className="flex items-center gap-3 mb-8">
            <div className="p-3 bg-primary/10 text-primary rounded-xl">
              <ShieldAlert className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold">Report an Incident</h1>
              <p className="text-neutral-500 text-sm">Provide details so our AI can triage your issue instantly.</p>
            </div>
          </div>

          {error && (
            <div className="mb-6 p-4 bg-red-50 text-red-700 border border-red-200 rounded-xl text-sm font-medium">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-semibold mb-2">Issue Title</label>
              <input
                type="text"
                required
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="e.g. Cannot access staging database"
                className="w-full px-4 py-3 bg-neutral-50 dark:bg-neutral-800 border border-neutral-200 dark:border-neutral-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold mb-2">Description</label>
              <textarea
                required
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Please describe the issue in detail, including error messages and steps to reproduce..."
                rows={5}
                className="w-full px-4 py-3 bg-neutral-50 dark:bg-neutral-800 border border-neutral-200 dark:border-neutral-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all resize-none"
              />
            </div>

            <button
              type="submit"
              disabled={submitting || !title || !description}
              className={cn(
                "w-full py-4 rounded-xl font-medium text-white flex items-center justify-center gap-2 transition-all",
                submitting ? "bg-primary/70 animate-pulse" : "bg-primary hover:bg-primary/90 shadow-lg shadow-primary/25 hover:shadow-primary/40"
              )}
            >
              {submitting ? 'Submitting & Triaging...' : 'Submit Incident'}
              {!submitting && <Send className="w-5 h-5" />}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
