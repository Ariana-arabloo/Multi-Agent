import { useCallback } from 'react';
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

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges],
  );

  return (
    <div style={{ width: '100vw', height: '100vh' }}>
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
  );
}

export default App;