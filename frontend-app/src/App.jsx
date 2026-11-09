import { useCallback, useState, useEffect } from 'react';
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
import { useSSE } from './hooks/useSSE';

// تعریف گره‌های اولیه روی بوم
const initialNodes = [
  { id: '1', position: { x: 250, y: 50 }, data: { label: 'گره اول' } },
  { id: '2', position: { x: 100, y: 150 }, data: { label: 'گره دوم' } },
  {
    id: '3',
    type: 'customAgent',
    position: { x: 250, y: 250 },
    data: {
      label: 'ایجنت جدید',
      status: 'idle'
    },
  }
];

// تعریف خطوط اتصال اولیه
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

  const [projectId, setProjectId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  // فراخوانی هوک SSE برای وصل شدن به جریان زنده سرور
  const { latestEvent, connectionStatus } = useSSE(projectId);

  // آپدیت کردن وضعیت گره‌ها در صورت دریافت پیام جدید از بک‌اند
  useEffect(() => {
    if (latestEvent) {
      setNodes((nds) =>
        nds.map((node) => {
          if (node.id === latestEvent.node_id) {
            return {
              ...node,
              data: { ...node.data, status: latestEvent.status },
            };
          }
          return node;
        })
      );
    }
  }, [latestEvent, setNodes]);

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges],
  );

  // ارسال درخواست برای گرفتن آیدی پروژه
  const handleStartProject = async () => {
    setIsLoading(true);
    try {
      const result = await startNewProject({ name: "پروژه تستی من", budget: 5000.0 });
      console.log("پروژه با موفقیت ساخته شد. پاسخ بک‌اند:", result);
      setProjectId(result.project_id);
    } catch (error) {
      alert("مشکلی در ارتباط با بک‌اند پیش آمد! کنسول را چک کن.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ width: '100vw', height: '100vh', display: 'flex', flexDirection: 'column' }}>
      
      {/* هدر و دکمه استارت */}
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
        
        {projectId && (
          <span style={{ marginLeft: '20px', paddingLeft: '20px', fontWeight: 'bold', color: '#28a745' }}>
            پروژه فعال شد - ID: {projectId}
          </span>
        )}
      </div>

      {/* هشدار در صورت قطع شدن اتصال اینترنت/سرور */}
      {connectionStatus === 'error' && (
        <div style={{ background: '#ffcccc', padding: '10px', textAlign: 'center', color: 'red' }}>
          ⚠️ ارتباط با سرور قطع شد! در حال تلاش خودکار برای اتصال مجدد...
        </div>
      )}

      {/* بوم گرافیکی ری‌اکت فلو */}
      <div style={{ flex: 1 }}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          nodeTypes={nodeTypes}
          onConnect={onConnect}
        >
          <Background />
          <Controls />
        </ReactFlow>
      </div>
      
    </div>
  );
}

export default App;