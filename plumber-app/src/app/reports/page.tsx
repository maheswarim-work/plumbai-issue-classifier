'use client';

import { useState } from 'react';
import { BarChart3, TrendingUp, Clock, DollarSign, Users, Calendar, Filter } from 'lucide-react';
import Layout from '@/components/Layout';

interface ReportData {
  period: string;
  totalJobs: number;
  completedJobs: number;
  revenue: number;
  avgResponseTime: number;
  customerSatisfaction: number;
}

export default function ReportsPage() {
  const [timeRange, setTimeRange] = useState('30d');

  const reportData: ReportData[] = [
    {
      period: 'Jan 2024',
      totalJobs: 145,
      completedJobs: 138,
      revenue: 28450,
      avgResponseTime: 2.3,
      customerSatisfaction: 4.7
    },
    {
      period: 'Dec 2023',
      totalJobs: 132,
      completedJobs: 128,
      revenue: 26100,
      avgResponseTime: 2.1,
      customerSatisfaction: 4.6
    },
    {
      period: 'Nov 2023',
      totalJobs: 118,
      completedJobs: 115,
      revenue: 23100,
      avgResponseTime: 2.5,
      customerSatisfaction: 4.8
    }
  ];

  const categoryData = [
    { category: 'Faucet Repair', jobs: 45, revenue: 8900 },
    { category: 'Drain Cleaning', jobs: 38, revenue: 7600 },
    { category: 'Water Heater', jobs: 22, revenue: 13200 },
    { category: 'Toilet Repair', jobs: 28, revenue: 4200 },
    { category: 'Pipe Installation', jobs: 12, revenue: 9600 }
  ];

  const technicianPerformance = [
    { name: 'Mike Johnson', jobs: 45, rating: 4.8, revenue: 8900 },
    { name: 'Tom Davis', jobs: 52, rating: 4.9, revenue: 10200 },
    { name: 'Alex Wilson', jobs: 38, rating: 4.7, revenue: 7200 },
    { name: 'Sarah Miller', jobs: 41, rating: 4.6, revenue: 8100 },
    { name: 'Chris Rodriguez', jobs: 29, rating: 4.5, revenue: 5800 }
  ];

  const currentMonth = reportData[0];

  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Reports & Analytics</h1>
            <p className="text-gray-500">Track performance and business metrics</p>
          </div>
          <div className="flex items-center space-x-2">
            <select
              value={timeRange}
              onChange={(e) => setTimeRange(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="7d">Last 7 days</option>
              <option value="30d">Last 30 days</option>
              <option value="90d">Last 90 days</option>
              <option value="1y">Last year</option>
            </select>
            <button className="btn-secondary flex items-center space-x-2">
              <Filter className="h-4 w-4" />
              <span>Export</span>
            </button>
          </div>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="card">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <BarChart3 className="h-8 w-8 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Total Jobs</p>
                <p className="text-2xl font-semibold text-gray-900">{currentMonth.totalJobs}</p>
                <p className="text-xs text-green-600">+9.8% from last month</p>
              </div>
            </div>
          </div>
          <div className="card">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <TrendingUp className="h-8 w-8 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Completion Rate</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {Math.round((currentMonth.completedJobs / currentMonth.totalJobs) * 100)}%
                </p>
                <p className="text-xs text-green-600">+2.1% from last month</p>
              </div>
            </div>
          </div>
          <div className="card">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <DollarSign className="h-8 w-8 text-yellow-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Revenue</p>
                <p className="text-2xl font-semibold text-gray-900">${currentMonth.revenue.toLocaleString()}</p>
                <p className="text-xs text-green-600">+9.0% from last month</p>
              </div>
            </div>
          </div>
          <div className="card">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Clock className="h-8 w-8 text-purple-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Avg Response Time</p>
                <p className="text-2xl font-semibold text-gray-900">{currentMonth.avgResponseTime}h</p>
                <p className="text-xs text-red-600">+0.2h from last month</p>
              </div>
            </div>
          </div>
        </div>

        {/* Charts and Tables */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Job Categories */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Jobs by Category</h3>
            <div className="space-y-3">
              {categoryData.map((category, index) => (
                <div key={index} className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm font-medium text-gray-900">{category.category}</span>
                      <span className="text-sm text-gray-500">{category.jobs} jobs</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-blue-600 h-2 rounded-full"
                        style={{ width: `${(category.jobs / Math.max(...categoryData.map(c => c.jobs))) * 100}%` }}
                      ></div>
                    </div>
                  </div>
                  <div className="ml-4 text-right">
                    <p className="text-sm font-medium text-gray-900">${category.revenue.toLocaleString()}</p>
                    <p className="text-xs text-gray-500">revenue</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Technician Performance */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Technician Performance</h3>
            <div className="space-y-4">
              {technicianPerformance.map((tech, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                      <Users className="h-4 w-4 text-blue-600" />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-gray-900">{tech.name}</p>
                      <p className="text-xs text-gray-500">{tech.jobs} jobs completed</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="flex items-center space-x-2">
                      <span className="text-yellow-500">★</span>
                      <span className="text-sm font-medium text-gray-900">{tech.rating}</span>
                    </div>
                    <p className="text-xs text-gray-500">${tech.revenue.toLocaleString()}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Monthly Trends */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Monthly Trends</h3>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Period
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Total Jobs
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Completed
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Revenue
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Avg Response (h)
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Satisfaction
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {reportData.map((data, index) => (
                  <tr key={index} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {data.period}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {data.totalJobs}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {data.completedJobs}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      ${data.revenue.toLocaleString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {data.avgResponseTime}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      <div className="flex items-center">
                        <span className="text-yellow-500 mr-1">★</span>
                        {data.customerSatisfaction}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Customer Satisfaction */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Customer Satisfaction</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="text-center p-4 bg-green-50 rounded-lg">
              <div className="text-3xl font-bold text-green-600">4.7</div>
              <div className="text-sm text-green-600 font-medium">Average Rating</div>
              <div className="text-xs text-gray-500 mt-1">Out of 5 stars</div>
            </div>
            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <div className="text-3xl font-bold text-blue-600">94%</div>
              <div className="text-sm text-blue-600 font-medium">Satisfied Customers</div>
              <div className="text-xs text-gray-500 mt-1">Would recommend</div>
            </div>
            <div className="text-center p-4 bg-yellow-50 rounded-lg">
              <div className="text-3xl font-bold text-yellow-600">2.3h</div>
              <div className="text-sm text-yellow-600 font-medium">Average Response</div>
              <div className="text-xs text-gray-500 mt-1">Time to arrival</div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
} 