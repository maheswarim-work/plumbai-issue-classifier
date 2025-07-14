'use client';

import { useState } from 'react';
import { Search, Filter, Plus, MapPin, Phone, Clock, User } from 'lucide-react';
import JobCard from '@/components/JobCard';
import Layout from '@/components/Layout';

interface Job {
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
}

export default function JobsPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [severityFilter, setSeverityFilter] = useState('all');

  const jobs: Job[] = [
    {
      id: '1',
      customerName: 'John Smith',
      phone: '+1 (555) 123-4567',
      address: '123 Main St, Anytown, USA',
      issue: 'Leaking faucet in kitchen',
      category: 'Faucet Repair',
      severity: 'medium',
      urgency: 'medium',
      status: 'assigned',
      assignedTo: 'Mike Johnson',
      createdAt: '2024-01-15T10:30:00Z',
      estimatedTime: '2 hours'
    },
    {
      id: '2',
      customerName: 'Sarah Wilson',
      phone: '+1 (555) 987-6543',
      address: '456 Oak Ave, Somewhere, USA',
      issue: 'Clogged drain in bathroom',
      category: 'Drain Cleaning',
      severity: 'high',
      urgency: 'high',
      status: 'in-progress',
      assignedTo: 'Tom Davis',
      createdAt: '2024-01-15T09:15:00Z',
      estimatedTime: '1.5 hours'
    },
    {
      id: '3',
      customerName: 'Robert Chen',
      phone: '+1 (555) 456-7890',
      address: '789 Pine Rd, Elsewhere, USA',
      issue: 'Water heater not working',
      category: 'Water Heater',
      severity: 'high',
      urgency: 'high',
      status: 'pending',
      createdAt: '2024-01-15T11:45:00Z',
      estimatedTime: '3 hours'
    },
    {
      id: '4',
      customerName: 'Emily Brown',
      phone: '+1 (555) 321-6540',
      address: '321 Elm St, Downtown, USA',
      issue: 'Toilet running continuously',
      category: 'Toilet Repair',
      severity: 'low',
      urgency: 'medium',
      status: 'completed',
      assignedTo: 'Alex Wilson',
      createdAt: '2024-01-14T14:20:00Z',
      estimatedTime: '1 hour'
    },
    {
      id: '5',
      customerName: 'David Lee',
      phone: '+1 (555) 789-0123',
      address: '654 Maple Dr, Suburb, USA',
      issue: 'Low water pressure throughout house',
      category: 'Water Pressure',
      severity: 'medium',
      urgency: 'low',
      status: 'assigned',
      assignedTo: 'Sarah Miller',
      createdAt: '2024-01-15T08:00:00Z',
      estimatedTime: '2.5 hours'
    }
  ];

  const filteredJobs = jobs.filter(job => {
    const matchesSearch = job.customerName.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         job.issue.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         job.address.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'all' || job.status === statusFilter;
    const matchesSeverity = severityFilter === 'all' || job.severity === severityFilter;
    
    return matchesSearch && matchesStatus && matchesSeverity;
  });

  const handleViewJob = (id: string) => {
    console.log('View job:', id);
    // TODO: Navigate to job details page
  };

  const handleUpdateJob = (id: string) => {
    console.log('Update job:', id);
    // TODO: Open update modal
  };

  const getStatusCount = (status: string) => {
    return jobs.filter(job => job.status === status).length;
  };

  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Job Management</h1>
            <p className="text-gray-500">Manage and track all plumbing jobs</p>
          </div>
          <button className="btn-primary flex items-center space-x-2">
            <Plus className="h-4 w-4" />
            <span>Create New Job</span>
          </button>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="card">
            <div className="text-center">
              <p className="text-2xl font-bold text-blue-600">{getStatusCount('pending')}</p>
              <p className="text-sm text-gray-500">Pending</p>
            </div>
          </div>
          <div className="card">
            <div className="text-center">
              <p className="text-2xl font-bold text-yellow-600">{getStatusCount('assigned')}</p>
              <p className="text-sm text-gray-500">Assigned</p>
            </div>
          </div>
          <div className="card">
            <div className="text-center">
              <p className="text-2xl font-bold text-blue-600">{getStatusCount('in-progress')}</p>
              <p className="text-sm text-gray-500">In Progress</p>
            </div>
          </div>
          <div className="card">
            <div className="text-center">
              <p className="text-2xl font-bold text-green-600">{getStatusCount('completed')}</p>
              <p className="text-sm text-gray-500">Completed</p>
            </div>
          </div>
        </div>

        {/* Filters */}
        <div className="card">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="h-5 w-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search jobs by customer, issue, or address..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>
            <div className="flex gap-2">
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="all">All Status</option>
                <option value="pending">Pending</option>
                <option value="assigned">Assigned</option>
                <option value="in-progress">In Progress</option>
                <option value="completed">Completed</option>
              </select>
              <select
                value={severityFilter}
                onChange={(e) => setSeverityFilter(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="all">All Severity</option>
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>
          </div>
        </div>

        {/* Jobs Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredJobs.map((job) => (
            <JobCard
              key={job.id}
              job={job}
              onView={handleViewJob}
              onUpdate={handleUpdateJob}
            />
          ))}
        </div>

        {filteredJobs.length === 0 && (
          <div className="text-center py-12">
            <div className="text-gray-400 mb-4">
              <Search className="h-12 w-12 mx-auto" />
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No jobs found</h3>
            <p className="text-gray-500">Try adjusting your search or filter criteria</p>
          </div>
        )}
      </div>
    </Layout>
  );
} 