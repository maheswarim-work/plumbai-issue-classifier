'use client';

import { MapPin, Phone, Clock, User, AlertTriangle, Star } from 'lucide-react';

interface JobCardProps {
  job: {
    id: string;
    customerName: string;
    phone: string;
    address: string;
    issue: string;
    category: string;
    severity: 'low' | 'medium' | 'high';
    urgency: 'low' | 'medium' | 'high';
    status: 'pending' | 'assigned' | 'in-progress' | 'completed';
    assignedTo?: string;
    createdAt: string;
    estimatedTime?: string;
  };
  onView?: (id: string) => void;
  onUpdate?: (id: string) => void;
}

export default function JobCard({ job, onView, onUpdate }: JobCardProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-gradient-to-r from-green-100 to-emerald-100 text-green-800 border-green-200';
      case 'in-progress': return 'bg-gradient-to-r from-blue-100 to-cyan-100 text-blue-800 border-blue-200';
      case 'assigned': return 'bg-gradient-to-r from-yellow-100 to-amber-100 text-yellow-800 border-yellow-200';
      case 'pending': return 'bg-gradient-to-r from-gray-100 to-slate-100 text-gray-800 border-gray-200';
      default: return 'bg-gradient-to-r from-gray-100 to-slate-100 text-gray-800 border-gray-200';
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high': return 'bg-gradient-to-r from-red-100 to-pink-100 text-red-800 border-red-200';
      case 'medium': return 'bg-gradient-to-r from-yellow-100 to-orange-100 text-yellow-800 border-yellow-200';
      case 'low': return 'bg-gradient-to-r from-green-100 to-emerald-100 text-green-800 border-green-200';
      default: return 'bg-gradient-to-r from-gray-100 to-slate-100 text-gray-800 border-gray-200';
    }
  };

  const getUrgencyIcon = (urgency: string) => {
    if (urgency === 'high') return <AlertTriangle className="h-4 w-4 text-red-500 animate-pulse" />;
    return null;
  };

  return (
    <div className="card-gradient group hover:scale-105 transition-all duration-300 cursor-pointer">
      <div className="flex justify-between items-start mb-6">
        <div className="flex-1">
          <div className="flex items-center space-x-2 mb-3">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center text-white font-semibold text-sm">
              {job.customerName.split(' ').map(n => n[0]).join('')}
            </div>
            <div>
              <h3 className="text-lg font-bold text-gray-900 group-hover:text-blue-600 transition-colors">{job.customerName}</h3>
              <div className="flex items-center space-x-2">
                {getUrgencyIcon(job.urgency)}
                <span className="text-xs text-gray-500">Job #{job.id}</span>
              </div>
            </div>
          </div>
          <div className="space-y-2">
            <div className="flex items-center text-sm text-gray-600">
              <Phone className="h-4 w-4 mr-2 text-blue-500" />
              {job.phone}
            </div>
            <div className="flex items-center text-sm text-gray-600">
              <MapPin className="h-4 w-4 mr-2 text-green-500" />
              <span className="truncate">{job.address}</span>
            </div>
          </div>
        </div>
        <div className="flex flex-col items-end space-y-2">
          <span className={`status-badge border ${getStatusColor(job.status)}`}>
            {job.status.replace('-', ' ')}
          </span>
          <span className={`severity-badge border ${getSeverityColor(job.severity)}`}>
            {job.severity}
          </span>
        </div>
      </div>

      <div className="mb-6">
        <h4 className="font-bold text-gray-900 mb-2 text-lg">{job.issue}</h4>
        <div className="flex items-center space-x-2">
          <span className="inline-flex px-3 py-1 text-xs font-semibold bg-gradient-to-r from-blue-100 to-indigo-100 text-blue-800 rounded-full border border-blue-200">
            {job.category}
          </span>
        </div>
      </div>

      <div className="flex items-center justify-between text-sm text-gray-600 mb-6">
        <div className="flex items-center">
          <div className="w-8 h-8 bg-gradient-to-br from-green-500 to-emerald-500 rounded-full flex items-center justify-center mr-2">
            <User className="h-4 w-4 text-white" />
          </div>
          <span className="font-medium">{job.assignedTo || 'Unassigned'}</span>
        </div>
        {job.estimatedTime && (
          <div className="flex items-center">
            <Clock className="h-4 w-4 mr-1 text-purple-500" />
            <span className="font-medium">{job.estimatedTime}</span>
          </div>
        )}
      </div>

      <div className="flex space-x-3">
        <button
          onClick={() => onView?.(job.id)}
          className="flex-1 btn-secondary text-sm group"
        >
          <span className="group-hover:scale-105 transition-transform">View Details</span>
        </button>
        <button
          onClick={() => onUpdate?.(job.id)}
          className="flex-1 btn-primary text-sm group"
        >
          <span className="group-hover:scale-105 transition-transform">Update Status</span>
        </button>
      </div>
    </div>
  );
} 