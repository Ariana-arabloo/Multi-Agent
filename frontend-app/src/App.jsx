import { useCallback , useState } from 'react';
import {
  ReactFlow,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import CustomAgentNode from './CustomAgentNode';
import { startNewProject } from './services/api';
const initialNodes = [
  { id: '1', position: { x: 250, y: 50 }, data: { label: 'گره اول' } },
  { id: '2', position: { x: 100, y: 150 }, data: { label: 'گره دوم' } },
  { 
    id: '3', 
    type: 'customAgent', 
    position: { x: 250, y: 250 }, 
    data: { 
      label: 'ایجنت جدید', 
      status: 'processing' 
    },
  }
];

const initialEdges = [

  {
    id: 'edge-1-3',
    source: '1',
    target: '3',
    animated: true,
    style: { stroke: '#f59e0b', strokeWidth: 2 }
  }

];

const nodeTypes = {
  customAgent: CustomAgentNode, 
};

function App() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  // استیت‌های جدید برای مدیریت آیدی پروژه و وضعیت لودینگ دکمه
  const [projectId, setProjectId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges],
  );

  // تابعی که با کلیک روی دکمه، درخواست POST را به بک‌اند می‌فرستد
  const handleStartProject = async () => {
    setIsLoading(true);
    try {
      const result = await startNewProject({
        name: "پروژه تستی من" ,
        budget: 5000.0
        });
      console.log("پروژه با موفقیت ساخته شد. پاسخ بک‌اند:", result);
      setProjectId(result.project_id); // ذخیره آیدی در استیت
    } catch (error) {
      alert("مشکلی در ارتباط با بک‌اند پیش آمد! کنسول را چک کن.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    // تغییر استایل به flex برای قرار دادن هدر در بالا و بوم در پایین
    <div style={{ width: '100vw', height: '100vh', display: 'flex', flexDirection: 'column' }}>
      
      {/* بخش هدر (محل قرارگیری دکمه) */}
      <div style={{ padding: '15px', background: '#f8f9fa', borderBottom: '1px solid #ddd', display: 'flex', alignItems: 'center' }}>
        <button 
          onClick={handleStartProject} 
          disabled={isLoading}
          style={{ 
            padding: '10px 20px', 
            cursor: isLoading ? 'wait' : 'pointer',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            fontSize: '16px'
          }}
        >
          {isLoading ? 'در حال ساخت...' : '🚀 استارت پروژه'}
        </button>
        
        {/* اگر آیدی پروژه با موفقیت دریافت شد، اینجا نمایش داده می‌شود */}
        {projectId && (
          <span style={{ marginLeft: '20px', paddingLeft: '20px', fontWeight: 'bold', color: '#28a745' }}>
            پروژه فعال شد - ID: {projectId}
          </span>
        )}
      </div>

      {/* بخش بوم گرافیکی React Flow */}
      <div style={{ flex: 1 }}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          nodeTypes={nodeTypes}
        >
          <Background />
          <Controls />
        </ReactFlow>
      </div>
      
    </div>
  );
}

export default App;