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
  DollarSign,
  Sparkles,
  Star
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

  const getStatusCount = (status: string) => {
    return jobs.filter(job => job.status === status).length;
  };

  return (
    <Layout>
      <div className="space-y-8">
        {/* Welcome Section */}
        <div className="welcome-card relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-r from-blue-600/20 to-indigo-600/20"></div>
          <div className="relative z-10">
            <div className="flex items-center justify-between">
              <div>
                <div className="flex items-center space-x-2 mb-3">
                  <Sparkles className="h-6 w-6 text-yellow-300" />
                  <h2 className="text-3xl font-bold text-white">Welcome back!</h2>
                </div>
                <p className="text-blue-100 text-lg">Here's what's happening with your plumbing business today.</p>
              </div>
              <div className="text-right">
                <p className="text-blue-200 text-sm">Today's Date</p>
                <p className="text-2xl font-bold text-white">{new Date().toLocaleDateString()}</p>
              </div>
            </div>
          </div>
          <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-white/10 to-transparent rounded-full -translate-y-16 translate-x-16"></div>
          <div className="absolute bottom-0 left-0 w-24 h-24 bg-gradient-to-tr from-white/5 to-transparent rounded-full translate-y-12 -translate-x-12"></div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="stats-card group">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="p-3 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl text-white">
                  <Clock className="h-8 w-8" />
                </div>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Pending Jobs</p>
                <p className="text-3xl font-bold text-gray-900 group-hover:text-blue-600 transition-colors">{getStatusCount('pending')}</p>
              </div>
            </div>
          </div>
          <div className="stats-card group">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="p-3 bg-gradient-to-br from-yellow-500 to-orange-500 rounded-xl text-white">
                  <Wrench className="h-8 w-8" />
                </div>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">In Progress</p>
                <p className="text-3xl font-bold text-gray-900 group-hover:text-yellow-600 transition-colors">{getStatusCount('in-progress')}</p>
              </div>
            </div>
          </div>
          <div className="stats-card group">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="p-3 bg-gradient-to-br from-green-500 to-emerald-500 rounded-xl text-white">
                  <CheckCircle className="h-8 w-8" />
                </div>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Completed Today</p>
                <p className="text-3xl font-bold text-gray-900 group-hover:text-green-600 transition-colors">15</p>
              </div>
            </div>
          </div>
          <div className="stats-card group">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="p-3 bg-gradient-to-br from-purple-500 to-indigo-500 rounded-xl text-white">
                  <User className="h-8 w-8" />
                </div>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Active Technicians</p>
                <p className="text-3xl font-bold text-gray-900 group-hover:text-purple-600 transition-colors">6</p>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Link href="/jobs" className="card-gradient group cursor-pointer">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="p-3 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl text-white group-hover:scale-110 transition-transform">
                  <BarChart3 className="h-8 w-8" />
                </div>
              </div>
              <div className="ml-4">
                <h3 className="text-xl font-semibold text-gray-900 group-hover:text-blue-600 transition-colors">Manage Jobs</h3>
                <p className="text-gray-600">View and manage all plumbing jobs</p>
              </div>
            </div>
          </Link>
          <Link href="/technicians" className="card-gradient group cursor-pointer">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="p-3 bg-gradient-to-br from-green-500 to-emerald-500 rounded-xl text-white group-hover:scale-110 transition-transform">
                  <User className="h-8 w-8" />
                </div>
              </div>
              <div className="ml-4">
                <h3 className="text-xl font-semibold text-gray-900 group-hover:text-green-600 transition-colors">Technicians</h3>
                <p className="text-gray-600">Manage your team and assignments</p>
              </div>
            </div>
          </Link>
          <Link href="/reports" className="card-gradient group cursor-pointer">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="p-3 bg-gradient-to-br from-purple-500 to-indigo-500 rounded-xl text-white group-hover:scale-110 transition-transform">
                  <TrendingUp className="h-8 w-8" />
                </div>
              </div>
              <div className="ml-4">
                <h3 className="text-xl font-semibold text-gray-900 group-hover:text-purple-600 transition-colors">Reports</h3>
                <p className="text-gray-600">View analytics and performance</p>
              </div>
            </div>
          </Link>
        </div>

        {/* Recent Jobs */}
        <div className="card">
          <div className="flex items-center justify-between mb-8">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg">
                <BarChart3 className="h-5 w-5 text-white" />
              </div>
              <h2 className="text-2xl font-bold text-gray-900">Recent Jobs</h2>
            </div>
            <Link href="/jobs" className="btn-secondary flex items-center space-x-2">
              <Filter className="h-4 w-4" />
              <span>View All</span>
            </Link>
          </div>
          <div className="overflow-hidden rounded-xl border border-gray-100">
            <table className="min-w-full divide-y divide-gray-200">
              <thead>
                <tr className="bg-gradient-to-r from-gray-50 to-gray-100">
                  <th className="table-header">
                    Customer
                  </th>
                  <th className="table-header">
                    Issue
                  </th>
                  <th className="table-header">
                    Status
                  </th>
                  <th className="table-header">
                    Severity
                  </th>
                  <th className="table-header">
                    Assigned To
                  </th>
                  <th className="table-header">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {jobs.map((job) => (
                  <tr key={job.id} className="table-row">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm font-semibold text-gray-900">{job.customerName}</div>
                        <div className="text-sm text-gray-500">{job.phone}</div>
                        <div className="text-sm text-gray-500 flex items-center">
                          <MapPin className="h-3 w-3 mr-1" />
                          {job.address}
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm font-medium text-gray-900">{job.issue}</div>
                        <div className="text-sm text-gray-500">{job.category}</div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`status-badge border ${getStatusColor(job.status)}`}>
                        {job.status.replace('-', ' ')}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`severity-badge border ${getSeverityColor(job.severity)}`}>
                        {job.severity}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      <div className="flex items-center">
                        <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                        {job.assignedTo || 'Unassigned'}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <button className="text-blue-600 hover:text-blue-900 mr-3 transition-colors">View</button>
                      <button className="text-green-600 hover:text-green-900 transition-colors">Update</button>
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
