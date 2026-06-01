import { Tab, useStatus } from '../App'

interface SidebarProps {
  activeTab: Tab
  setActiveTab: (tab: Tab) => void
}

const tabs: { id: Tab; label: string; icon: string }[] = [
  { id: 'dashboard', label: 'Dashboard', icon: '📊' },
  { id: 'send-message', label: 'Send Message', icon: '💬' },
  { id: 'send-dm', label: 'Send DM', icon: '📨' },
  { id: 'members', label: 'Channel Members', icon: '👥' },
  { id: 'feedback', label: 'Feedback', icon: '📝' },
]

function Sidebar({ activeTab, setActiveTab }: SidebarProps) {
  const status = useStatus()

  return (
    <aside className="w-64 bg-white shadow-md flex flex-col">
      <div className="p-6 border-b">
        <h1 className="text-xl font-bold text-gray-800">Slack Bot Demo</h1>
        <p className="text-sm text-gray-500 mt-1">Go + React</p>
      </div>

      {/* Status Indicator */}
      <div className={`mx-4 mt-4 p-3 rounded-lg ${status.ready ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'}`}>
        <div className="flex items-center gap-2">
          <span className={`w-2.5 h-2.5 rounded-full ${status.ready ? 'bg-green-500' : 'bg-red-500'}`} />
          <span className={`text-sm font-medium ${status.ready ? 'text-green-800' : 'text-red-800'}`}>
            {status.ready ? 'Connected' : 'Not Connected'}
          </span>
        </div>
        <p className={`text-xs mt-1 ${status.ready ? 'text-green-600' : 'text-red-600'}`}>
          {status.message}
        </p>
      </div>

      <nav className="flex-1 p-4">
        <ul className="space-y-2">
          {tabs.map((tab) => (
            <li key={tab.id}>
              <button
                onClick={() => setActiveTab(tab.id)}
                className={`w-full text-left px-4 py-3 rounded-lg transition-colors ${
                  activeTab === tab.id
                    ? 'bg-blue-100 text-blue-700 font-medium'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                <span className="mr-3">{tab.icon}</span>
                {tab.label}
              </button>
            </li>
          ))}
        </ul>
      </nav>
      <div className="p-4 border-t bg-gray-50">
        <p className="text-xs text-gray-500 font-medium mb-2">
          Webhook Endpoints:
        </p>
        <code className="text-xs text-gray-600 block">/slack/events</code>
        <code className="text-xs text-gray-600 block">/slack/commands</code>
        <code className="text-xs text-gray-600 block">/slack/interactions</code>
      </div>
    </aside>
  )
}

export default Sidebar
