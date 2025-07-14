'use client';

import { useState } from 'react';
import { Search, Phone, MapPin, Clock, User, CheckCircle, XCircle, AlertTriangle } from 'lucide-react';
import Layout from '@/components/Layout';

interface Technician {
  id: string;
  name: string;
  phone: string;
  email: string;
  specialties: string[];
  status: 'available' | 'busy' | 'offline';
  currentJob?: string;
  rating: number;
  completedJobs: number;
  location: string;
  lastActive: string;
}

export default function TechniciansPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');

  const technicians: Technician[] = [
    {
      id: '1',
      name: 'Mike Johnson',
      phone: '+1 (555) 123-4567',
      email: 'mike.johnson@plumberco.com',
      specialties: ['Faucet Repair', 'Drain Cleaning', 'Pipe Installation'],
      status: 'available',
      rating: 4.8,
      completedJobs: 156,
      location: 'Downtown Area',
      lastActive: '2 minutes ago'
    },
    {
      id: '2',
      name: 'Tom Davis',
      phone: '+1 (555) 987-6543',
      email: 'tom.davis@plumberco.com',
      specialties: ['Water Heater', 'Emergency Repairs', 'Gas Lines'],
      status: 'busy',
      currentJob: 'Water heater replacement - Sarah Wilson',
      rating: 4.9,
      completedJobs: 203,
      location: 'North District',
      lastActive: '5 minutes ago'
    },
    {
      id: '3',
      name: 'Alex Wilson',
      phone: '+1 (555) 456-7890',
      email: 'alex.wilson@plumberco.com',
      specialties: ['Toilet Repair', 'Sewer Lines', 'Backflow Prevention'],
      status: 'available',
      rating: 4.7,
      completedJobs: 89,
      location: 'South District',
      lastActive: '1 minute ago'
    },
    {
      id: '4',
      name: 'Sarah Miller',
      phone: '+1 (555) 321-6540',
      email: 'sarah.miller@plumberco.com',
      specialties: ['Water Pressure', 'Pipe Leaks', 'Fixture Installation'],
      status: 'busy',
      currentJob: 'Low pressure diagnosis - David Lee',
      rating: 4.6,
      completedJobs: 134,
      location: 'East District',
      lastActive: '3 minutes ago'
    },
    {
      id: '5',
      name: 'Chris Rodriguez',
      phone: '+1 (555) 789-0123',
      email: 'chris.rodriguez@plumberco.com',
      specialties: ['Commercial Plumbing', 'HVAC Integration', 'Preventive Maintenance'],
      status: 'offline',
      rating: 4.5,
      completedJobs: 67,
      location: 'West District',
      lastActive: '2 hours ago'
    }
  ];

  const filteredTechnicians = technicians.filter(tech => {
    const matchesSearch = tech.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         tech.specialties.some(s => s.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesStatus = statusFilter === 'all' || tech.status === statusFilter;
    
    return matchesSearch && matchesStatus;
  });

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'available': return 'bg-green-100 text-green-800';
      case 'busy': return 'bg-yellow-100 text-yellow-800';
      case 'offline': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'available': return <CheckCircle className="h-4 w-4" />;
      case 'busy': return <AlertTriangle className="h-4 w-4" />;
      case 'offline': return <XCircle className="h-4 w-4" />;
      default: return <User className="h-4 w-4" />;
    }
  };

  const getStatusCount = (status: string) => {
    return technicians.filter(tech => tech.status === status).length;
  };

  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Technician Management</h1>
            <p className="text-gray-500">Manage your team of plumbing technicians</p>
          </div>
          <button className="btn-primary">
            Add Technician
          </button>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="card">
            <div className="text-center">
              <p className="text-2xl font-bold text-green-600">{getStatusCount('available')}</p>
              <p className="text-sm text-gray-500">Available</p>
            </div>
          </div>
          <div className="card">
            <div className="text-center">
              <p className="text-2xl font-bold text-yellow-600">{getStatusCount('busy')}</p>
              <p className="text-sm text-gray-500">Busy</p>
            </div>
          </div>
          <div className="card">
            <div className="text-center">
              <p className="text-2xl font-bold text-gray-600">{getStatusCount('offline')}</p>
              <p className="text-sm text-gray-500">Offline</p>
            </div>
          </div>
          <div className="card">
            <div className="text-center">
              <p className="text-2xl font-bold text-blue-600">{technicians.length}</p>
              <p className="text-sm text-gray-500">Total</p>
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
                  placeholder="Search technicians by name or specialty..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="all">All Status</option>
              <option value="available">Available</option>
              <option value="busy">Busy</option>
              <option value="offline">Offline</option>
            </select>
          </div>
        </div>

        {/* Technicians Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredTechnicians.map((tech) => (
            <div key={tech.id} className="card hover:shadow-md transition-shadow">
              <div className="flex justify-between items-start mb-4">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-2">
                    <h3 className="text-lg font-semibold text-gray-900">{tech.name}</h3>
                    <span className={`inline-flex items-center px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(tech.status)}`}>
                      {getStatusIcon(tech.status)}
                      <span className="ml-1">{tech.status}</span>
                    </span>
                  </div>
                  <div className="flex items-center text-sm text-gray-500 mb-1">
                    <Phone className="h-4 w-4 mr-1" />
                    {tech.phone}
                  </div>
                  <div className="flex items-center text-sm text-gray-500 mb-3">
                    <MapPin className="h-4 w-4 mr-1" />
                    {tech.location}
                  </div>
                </div>
                <div className="text-right">
                  <div className="flex items-center text-sm text-gray-500">
                    <span className="text-yellow-500">★</span>
                    <span className="ml-1">{tech.rating}</span>
                  </div>
                  <div className="text-xs text-gray-400 mt-1">
                    {tech.completedJobs} jobs completed
                  </div>
                </div>
              </div>

              <div className="mb-4">
                <h4 className="font-medium text-gray-900 mb-2">Specialties</h4>
                <div className="flex flex-wrap gap-1">
                  {tech.specialties.map((specialty, index) => (
                    <span
                      key={index}
                      className="inline-flex px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full"
                    >
                      {specialty}
                    </span>
                  ))}
                </div>
              </div>

              {tech.currentJob && (
                <div className="mb-4 p-3 bg-yellow-50 rounded-lg">
                  <div className="flex items-center text-sm text-yellow-800">
                    <Clock className="h-4 w-4 mr-1" />
                    <span className="font-medium">Current Job:</span>
                  </div>
                  <p className="text-sm text-yellow-700 mt-1">{tech.currentJob}</p>
                </div>
              )}

              <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                <span>Last active: {tech.lastActive}</span>
              </div>

              <div className="flex space-x-2">
                <button className="flex-1 btn-secondary text-sm">
                  View Profile
                </button>
                <button className="flex-1 btn-primary text-sm">
                  Contact
                </button>
              </div>
            </div>
          ))}
        </div>

        {filteredTechnicians.length === 0 && (
          <div className="text-center py-12">
            <div className="text-gray-400 mb-4">
              <User className="h-12 w-12 mx-auto" />
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No technicians found</h3>
            <p className="text-gray-500">Try adjusting your search or filter criteria</p>
          </div>
        )}
      </div>
    </Layout>
  );
} 