'use client';

import { MapPin, Phone, Clock, User, AlertTriangle } from 'lucide-react';

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
      case 'completed': return 'bg-green-100 text-green-800';
      case 'in-progress': return 'bg-blue-100 text-blue-800';
      case 'assigned': return 'bg-yellow-100 text-yellow-800';
      case 'pending': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high': return 'bg-red-100 text-red-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'low': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getUrgencyIcon = (urgency: string) => {
    if (urgency === 'high') return <AlertTriangle className="h-4 w-4 text-red-500" />;
    return null;
  };

  return (
    <div className="card hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start mb-4">
        <div className="flex-1">
          <div className="flex items-center space-x-2 mb-2">
            <h3 className="text-lg font-semibold text-gray-900">{job.customerName}</h3>
            {getUrgencyIcon(job.urgency)}
          </div>
          <div className="flex items-center text-sm text-gray-500 mb-1">
            <Phone className="h-4 w-4 mr-1" />
            {job.phone}
          </div>
          <div className="flex items-center text-sm text-gray-500 mb-3">
            <MapPin className="h-4 w-4 mr-1" />
            {job.address}
          </div>
        </div>
        <div className="flex flex-col items-end space-y-2">
          <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(job.status)}`}>
            {job.status.replace('-', ' ')}
          </span>
          <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getSeverityColor(job.severity)}`}>
            {job.severity}
          </span>
        </div>
      </div>

      <div className="mb-4">
        <h4 className="font-medium text-gray-900 mb-1">{job.issue}</h4>
        <p className="text-sm text-gray-500">{job.category}</p>
      </div>

      <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
        <div className="flex items-center">
          <User className="h-4 w-4 mr-1" />
          <span>{job.assignedTo || 'Unassigned'}</span>
        </div>
        {job.estimatedTime && (
          <div className="flex items-center">
            <Clock className="h-4 w-4 mr-1" />
            <span>{job.estimatedTime}</span>
          </div>
        )}
      </div>

      <div className="flex space-x-2">
        <button
          onClick={() => onView?.(job.id)}
          className="flex-1 btn-secondary text-sm"
        >
          View Details
        </button>
        <button
          onClick={() => onUpdate?.(job.id)}
          className="flex-1 btn-primary text-sm"
        >
          Update Status
        </button>
      </div>
    </div>
  );
} 