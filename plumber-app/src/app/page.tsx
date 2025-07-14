'use client';

import { useState } from 'react';
import Link from 'next/link';
import { 
  Wrench, 
  Clock, 
  MapPin, 
  User, 
  Phone, 
  AlertTriangle, 
  CheckCircle, 
  XCircle,
  Plus,
  Search,
  Filter,
  BarChart3,
  TrendingUp,
  DollarSign
} from 'lucide-react';
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

export default function Dashboard() {
  const [jobs, setJobs] = useState<Job[]>([
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
    }
  ]);

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

  const getStatusCount = (status: string) => {
    return jobs.filter(job => job.status === status).length;
  };

  return (
    <Layout>
      <div className="space-y-6">
        {/* Welcome Section */}
        <div className="card bg-gradient-to-r from-blue-50 to-indigo-50 border-blue-200">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Welcome back!</h2>
              <p className="text-gray-600">Here's what's happening with your plumbing business today.</p>
            </div>
            <div className="text-right">
              <p className="text-sm text-gray-500">Today's Date</p>
              <p className="text-lg font-semibold text-gray-900">{new Date().toLocaleDateString()}</p>
            </div>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="card">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Clock className="h-8 w-8 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Pending Jobs</p>
                <p className="text-2xl font-semibold text-gray-900">{getStatusCount('pending')}</p>
              </div>
            </div>
          </div>
          <div className="card">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Wrench className="h-8 w-8 text-yellow-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">In Progress</p>
                <p className="text-2xl font-semibold text-gray-900">{getStatusCount('in-progress')}</p>
              </div>
            </div>
          </div>
          <div className="card">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <CheckCircle className="h-8 w-8 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Completed Today</p>
                <p className="text-2xl font-semibold text-gray-900">15</p>
              </div>
            </div>
          </div>
          <div className="card">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <User className="h-8 w-8 text-purple-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Active Technicians</p>
                <p className="text-2xl font-semibold text-gray-900">6</p>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Link href="/jobs" className="card hover:shadow-md transition-shadow cursor-pointer">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <BarChart3 className="h-8 w-8 text-blue-600" />
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-semibold text-gray-900">Manage Jobs</h3>
                <p className="text-sm text-gray-500">View and manage all plumbing jobs</p>
              </div>
            </div>
          </Link>
          <Link href="/technicians" className="card hover:shadow-md transition-shadow cursor-pointer">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <User className="h-8 w-8 text-green-600" />
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-semibold text-gray-900">Technicians</h3>
                <p className="text-sm text-gray-500">Manage your team and assignments</p>
              </div>
            </div>
          </Link>
          <Link href="/reports" className="card hover:shadow-md transition-shadow cursor-pointer">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <TrendingUp className="h-8 w-8 text-purple-600" />
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-semibold text-gray-900">Reports</h3>
                <p className="text-sm text-gray-500">View analytics and performance</p>
              </div>
            </div>
          </Link>
        </div>

        {/* Recent Jobs */}
        <div className="card">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-semibold text-gray-900">Recent Jobs</h2>
            <Link href="/jobs" className="btn-secondary flex items-center space-x-2">
              <Filter className="h-4 w-4" />
              <span>View All</span>
            </Link>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Customer
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Issue
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Severity
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Assigned To
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {jobs.map((job) => (
                  <tr key={job.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm font-medium text-gray-900">{job.customerName}</div>
                        <div className="text-sm text-gray-500">{job.phone}</div>
                        <div className="text-sm text-gray-500 flex items-center">
                          <MapPin className="h-3 w-3 mr-1" />
                          {job.address}
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm text-gray-900">{job.issue}</div>
                        <div className="text-sm text-gray-500">{job.category}</div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(job.status)}`}>
                        {job.status.replace('-', ' ')}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getSeverityColor(job.severity)}`}>
                        {job.severity}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {job.assignedTo || 'Unassigned'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <button className="text-blue-600 hover:text-blue-900 mr-3">View</button>
                      <button className="text-green-600 hover:text-green-900">Update</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </Layout>
  );
}
