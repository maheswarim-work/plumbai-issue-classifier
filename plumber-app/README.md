# Plumber Workflow - Next.js App

A modern, responsive web application for managing plumbing business operations. Built with Next.js, TypeScript, and Tailwind CSS.

## Features

### 🏠 Dashboard
- Real-time overview of business metrics
- Quick access to key functions
- Recent jobs overview
- Performance statistics

### 📋 Job Management
- Comprehensive job tracking system
- Filter and search capabilities
- Status management (pending, assigned, in-progress, completed)
- Severity and urgency classification
- Customer information management

### 👥 Technician Management
- Technician profiles and specialties
- Real-time status tracking (available, busy, offline)
- Performance metrics and ratings
- Current job assignments
- Contact information

### 📊 Reports & Analytics
- Business performance metrics
- Revenue tracking
- Customer satisfaction scores
- Technician performance analysis
- Job category breakdowns
- Monthly trends and comparisons

## Tech Stack

- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **UI Components**: Custom components with Tailwind

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd plumber-app
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
plumber-app/
├── src/
│   ├── app/
│   │   ├── jobs/
│   │   │   └── page.tsx          # Job management page
│   │   ├── technicians/
│   │   │   └── page.tsx          # Technician management page
│   │   ├── reports/
│   │   │   └── page.tsx          # Reports and analytics page
│   │   ├── globals.css           # Global styles
│   │   ├── layout.tsx            # Root layout
│   │   └── page.tsx              # Dashboard page
│   ├── components/
│   │   ├── Layout.tsx            # Shared layout component
│   │   └── JobCard.tsx           # Job card component
│   └── ...
├── public/                        # Static assets
├── package.json
└── README.md
```

## Key Components

### Layout Component
- Consistent header and navigation
- Responsive design
- Active page highlighting

### JobCard Component
- Reusable job display component
- Status and severity indicators
- Action buttons for job management

### Dashboard
- Welcome section with current date
- Key metrics cards
- Quick action links
- Recent jobs table

## Features in Detail

### Job Management
- **Search & Filter**: Find jobs by customer, issue, or address
- **Status Tracking**: Monitor job progress from pending to completed
- **Severity Classification**: High, medium, low priority levels
- **Assignment**: Track which technician is assigned to each job
- **Time Estimates**: Estimated completion times for jobs

### Technician Management
- **Profile Management**: Contact info, specialties, ratings
- **Status Tracking**: Real-time availability status
- **Performance Metrics**: Jobs completed, ratings, revenue generated
- **Current Assignments**: See what each technician is working on

### Analytics & Reporting
- **Business Metrics**: Total jobs, completion rates, revenue
- **Performance Trends**: Monthly comparisons and growth
- **Customer Satisfaction**: Ratings and response times
- **Category Analysis**: Breakdown by job type and revenue

## Customization

### Styling
The app uses Tailwind CSS for styling. Custom styles can be added in:
- `src/app/globals.css` for global styles
- Component-specific styles using Tailwind classes

### Data
Currently using mock data. To integrate with a real API:
1. Replace mock data in components with API calls
2. Add state management (e.g., React Query, SWR)
3. Implement error handling and loading states

### Adding New Features
1. Create new page in `src/app/`
2. Add navigation link in `src/components/Layout.tsx`
3. Follow existing component patterns

## Deployment

### Vercel (Recommended)
1. Push code to GitHub
2. Connect repository to Vercel
3. Deploy automatically

### Other Platforms
- Build: `npm run build`
- Start: `npm start`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support or questions, please open an issue in the repository.
