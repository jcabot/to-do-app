import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";

const Task: React.FC = () => {
  return (
    <div id="page-task-0">
    <div id="iuq6w" style={{"display": "flex", "height": "100vh", "fontFamily": "Arial, sans-serif", "--chart-color-palette": "default"}}>
      <nav id="idd3t" style={{"width": "250px", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "padding": "20px", "overflowY": "auto", "display": "flex", "flexDirection": "column", "--chart-color-palette": "default"}}>
        <h2 id="iz05t" style={{"marginTop": "0", "fontSize": "24px", "marginBottom": "30px", "fontWeight": "bold", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="ir7nh" style={{"display": "flex", "flexDirection": "column", "flex": "1", "--chart-color-palette": "default"}}>
          <a id="ixhv4" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "rgba(255,255,255,0.2)", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/task">{"Task"}</a>
          <a id="ifb0z" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/tasklist">{"TaskList"}</a>
        </div>
        <p id="izbeo" style={{"marginTop": "auto", "paddingTop": "20px", "borderTop": "1px solid rgba(255,255,255,0.2)", "fontSize": "11px", "opacity": "0.8", "textAlign": "center", "--chart-color-palette": "default"}}>{"© 2025 BESSER. All rights reserved."}</p>
      </nav>
      <main id="i8pid" style={{"flex": "1", "padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default"}}>
        <h1 id="imif1" style={{"marginTop": "0", "color": "#333", "fontSize": "32px", "marginBottom": "10px", "--chart-color-palette": "default"}}>{"Task"}</h1>
        <p id="iodm6" style={{"color": "#666", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"Manage Task data"}</p>
        <TableBlock id="table-task-0" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Task List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "TaskId", "column_type": "field", "field": "taskId", "type": "int", "required": true}, {"label": "Title", "column_type": "field", "field": "title", "type": "str", "required": true}, {"label": "Description", "column_type": "field", "field": "description", "type": "str", "required": true}, {"label": "DueDate", "column_type": "field", "field": "dueDate", "type": "date", "required": true}, {"label": "Status", "column_type": "field", "field": "status", "type": "str", "required": true}, {"label": "CompletionDate", "column_type": "field", "field": "completionDate", "type": "date", "required": true}, {"label": "Urgent", "column_type": "field", "field": "urgent", "type": "bool", "required": true}, {"label": "Important", "column_type": "field", "field": "important", "type": "bool", "required": true}], "formColumns": [{"column_type": "field", "field": "taskId", "label": "taskId", "type": "int", "required": true}, {"column_type": "field", "field": "urgent", "label": "urgent", "type": "bool", "required": true}, {"column_type": "field", "field": "important", "label": "important", "type": "bool", "required": true}, {"column_type": "field", "field": "title", "label": "title", "type": "str", "required": true}, {"column_type": "field", "field": "description", "label": "description", "type": "str", "required": true}, {"column_type": "field", "field": "dueDate", "label": "dueDate", "type": "date", "required": true}, {"column_type": "field", "field": "status", "label": "status", "type": "str", "required": true}, {"column_type": "field", "field": "completionDate", "label": "completionDate", "type": "date", "required": true}, {"column_type": "lookup", "path": "tasklist", "field": "tasklist", "lookup_field": "listId", "entity": "TaskList", "type": "str", "required": true}]}} dataBinding={{"entity": "Task", "endpoint": "/task/"}} />
      </main>
    </div>    </div>
  );
};

export default Task;
