import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { TableProvider } from "./contexts/TableContext";
import Task from "./pages/Task";
import Tasklist from "./pages/Tasklist";

function App() {
  return (
    <TableProvider>
      <div className="app-container">
        <main className="app-main">
          <Routes>
            <Route path="/task" element={<Task />} />
            <Route path="/tasklist" element={<Tasklist />} />
            <Route path="/" element={<Navigate to="/task" replace />} />
            <Route path="*" element={<Navigate to="/task" replace />} />
          </Routes>
        </main>
      </div>
    </TableProvider>
  );
}
export default App;
