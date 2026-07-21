import React from 'react';

export default function TemplateDashboard({ sidebar, children }) {
  return (
    <div className="flex h-screen bg-[#0f1419]">
      {/* Barra Lateral */}
      <aside className="w-64 flex-shrink-0">
        {sidebar}
      </aside>

      {/* Conteúdo Principal */}
      <main className="flex-1 overflow-auto">
        {children}
      </main>
    </div>
  );
}