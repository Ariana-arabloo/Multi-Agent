import React from 'react';
import { Handle, Position } from '@xyflow/react';

function CustomAgentNode({ data }) {
  const status = data.status || 'idle';

  let bgColor = '#ffffff'; 
  let icon = '⚪';
  
  if (status === 'processing') {
    bgColor = '#fff3cd'; 
    icon = '⏳';
  } else if (status === 'success') {
    bgColor = '#d4edda'; 
    icon = '✅';
  } else if (status === 'error') {
    bgColor = '#f8d7da'; 
    icon = '❌';
  }

  return (
    <div style={{
      padding: '15px',
      borderRadius: '8px',
      border: '2px solid #333',
      backgroundColor: bgColor,
      textAlign: 'center',
      width: '150px',
      boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
    }}>
      <Handle type="target" position={Position.Top} style={{ background: '#555' }} />

      <div style={{ fontWeight: 'bold', marginBottom: '8px' }}>
        {data.label || 'Agent'}
      </div>
      
      <div style={{ fontSize: '12px', color: '#555', display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '5px' }}>
        <span>{icon}</span> وضعیت: {status}
      </div>

      <Handle type="source" position={Position.Bottom} style={{ background: '#555' }} />
    </div>
  );
}

export default CustomAgentNode;